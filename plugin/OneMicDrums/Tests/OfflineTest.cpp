// Offline-Messprogramm: rendert einen synthetischen Mono-Drumloop durch das Plugin,
// prüft Pegel/Stereo/Hall/Limiter und schreibt Hörbeispiele als WAV.
//   OneMicDrumsTest [Ausgabeordner]   → erwartet am Ende "OMD OK"
#include "../Source/PluginProcessor.h"
#include <juce_audio_formats/juce_audio_formats.h>
#include <random>
#include "../Source/PluginEditor.h"

static constexpr double SR = 48000.0;
static constexpr int BLOCK = 256;

static juce::AudioBuffer<float> makeDrumLoop (double seconds, double silenceAfter)
{
    const int n = (int) (seconds * SR), total = n + (int) (silenceAfter * SR);
    juce::AudioBuffer<float> b (1, total);
    b.clear();
    auto* d = b.getWritePointer (0);
    std::mt19937 rng (7);
    std::uniform_real_distribution<float> noise (-1.0f, 1.0f);
    const double beat = 60.0 / 100.0;   // 100 BPM
    auto add = [&] (double t0, auto fn, double len)
    {
        const int s0 = (int) (t0 * SR);
        for (int i = 0; i < (int) (len * SR) && s0 + i < n; ++i)
            d[s0 + i] += fn (i / SR);
    };
    double ph = 0;
    for (double t = 0; t < seconds; t += beat * 0.5)
    {
        const int step = (int) std::round (t / (beat * 0.5)) % 8;
        if (step == 0 || step == 5)   // Bassdrum
        {
            ph = 0;
            add (t, [&] (double x) { const double f = 50 + 90 * std::exp (-x * 30); ph += 2 * juce::MathConstants<double>::pi * f / SR;
                                     return (float) (0.9 * std::sin (ph) * std::exp (-x * 7) + 0.3 * noise (rng) * std::exp (-x * 400)); }, 0.6);
        }
        if (step == 2 || step == 6)   // Snare
            add (t, [&] (double x) { return (float) (0.35 * std::sin (2 * juce::MathConstants<double>::pi * 190 * x) * std::exp (-x * 25)
                                                     + 0.45 * noise (rng) * std::exp (-x * 18)); }, 0.4);
        // Hi-Hat (hochpassiges Rauschen, leiser – wie aus der Raum-Perspektive eines Mikrofons)
        float prev = 0;
        add (t, [&] (double x) { const float w = noise (rng); const float hp = w - prev; prev = w;
                                 return (float) (0.12 * hp * std::exp (-x * 60)); }, 0.08);
    }
    b.applyGain (0, 0, n, 0.5f / b.getMagnitude (0, 0, n));   // Spitze −6 dBFS
    return b;
}

struct Result { juce::AudioBuffer<float> out; float compGr = 0, limGr = 0; };

static Result render (const juce::AudioBuffer<float>& in, std::map<juce::String, float> params)
{
    OneMicDrumsProcessor p;
    p.setPlayConfigDetails (1, 2, SR, BLOCK);
    for (auto& [id, v] : params)
    {
        auto* prm = p.apvts.getParameter (id);
        prm->setValueNotifyingHost (prm->convertTo0to1 (v));
    }
    p.prepareToPlay (SR, BLOCK);
    Result r;
    r.out.setSize (2, in.getNumSamples());
    juce::AudioBuffer<float> blk (2, BLOCK);
    juce::MidiBuffer midi;
    for (int pos = 0; pos < in.getNumSamples(); pos += BLOCK)
    {
        const int len = juce::jmin (BLOCK, in.getNumSamples() - pos);
        blk.setSize (2, len, false, false, true);
        blk.clear();
        blk.copyFrom (0, 0, in, 0, pos, len);
        p.processBlock (blk, midi);
        r.out.copyFrom (0, pos, blk, 0, 0, len);
        r.out.copyFrom (1, pos, blk, 1, 0, len);
        r.compGr = juce::jmax (r.compGr, p.gainReductionDb.load());
        r.limGr = juce::jmax (r.limGr, p.crushReductionDb.load());
    }
    return r;
}

static float rmsDb (const float* d, int n) { double s = 0; for (int i = 0; i < n; ++i) s += (double) d[i] * d[i]; return (float) (10 * std::log10 (s / juce::jmax (1, n) + 1e-20)); }
static float peakDb (const juce::AudioBuffer<float>& b, int from, int to)
{
    float m = 0; for (int c = 0; c < b.getNumChannels(); ++c) for (int i = from; i < to; ++i) m = juce::jmax (m, std::abs (b.getSample (c, i)));
    return juce::Decibels::gainToDecibels (m, -120.0f);
}

static void writeWav (const juce::File& f, const juce::AudioBuffer<float>& b)
{
    f.deleteFile();
    juce::WavAudioFormat wav;
    std::unique_ptr<juce::AudioFormatWriter> w (wav.createWriterFor (new juce::FileOutputStream (f), SR,
                                                (unsigned) b.getNumChannels(), 24, {}, 0));
    if (w) w->writeFromAudioSampleBuffer (b, 0, b.getNumSamples());
}

int main (int argc, char** argv)
{
    juce::ScopedJuceInitialiser_GUI gui;
    const juce::File outDir = argc > 1 ? juce::File (argv[1]) : juce::File::getCurrentWorkingDirectory().getChildFile ("out");
    outDir.createDirectory();

    int fails = 0;
    auto check = [&] (bool ok, const juce::String& what) { std::printf ("%s  %s\n", ok ? "ok  " : "FAIL", what.toRawUTF8()); if (! ok) ++fails; };

    const auto dry = makeDrumLoop (9.6, 4.0);
    const int nSig = (int) (9.6 * SR), nAll = dry.getNumSamples();
    const float dryRms = rmsDb (dry.getReadPointer (0), nSig);
    std::printf ("Dry: RMS %.1f dB, Peak %.1f dB\n", dryRms, peakDb (dry, 0, nSig));

    // Neutral: alles auf 0
    auto neutral = render (dry, {});
    {
        juce::AudioBuffer<float> mid (1, nSig), side (1, nSig);
        for (int i = 0; i < nSig; ++i)
        {
            mid.setSample (0, i, 0.5f * (neutral.out.getSample (0, i) + neutral.out.getSample (1, i)));
            side.setSample (0, i, 0.5f * (neutral.out.getSample (0, i) - neutral.out.getSample (1, i)));
        }
        const float midRms = rmsDb (mid.getReadPointer (0), nSig), sideRms = rmsDb (side.getReadPointer (0), nSig);
        std::printf ("Neutral: Mid %.1f dB, Side %.1f dB, Peak %.1f dB\n", midRms, sideRms, peakDb (neutral.out, 0, nAll));
        check (std::abs (midRms - dryRms) < 0.6f, "Mono-Summe = Eingangspegel (Weiche + Stereo monokompatibel)");
        check (sideRms < midRms - 6.0f && sideRms > midRms - 30.0f, "Stereo-Anteil vorhanden, aber dezent");
    }

    // Low aus / High aus
    {
        auto noLow = render (dry, { { "low", -24.0f } });
        auto noHigh = render (dry, { { "high", -24.0f } });
        const float a = rmsDb (noLow.out.getReadPointer (0), nSig), b = rmsDb (noHigh.out.getReadPointer (0), nSig);
        std::printf ("Nur High: %.1f dB, nur Low: %.1f dB\n", a, b);
        check (a < dryRms - 1.0f && b < dryRms - 1.0f, "Bänder getrennt regelbar");
        // Im Low-Band darf kein Stereo-Anteil sein
        float sideLow = 0; for (int i = 0; i < nSig; ++i) sideLow = juce::jmax (sideLow, std::abs (noHigh.out.getSample (0, i) - noHigh.out.getSample (1, i)));
        check (sideLow < 1.0e-4f, "Bässe bleiben exakt in der Mitte");
    }

    // Kompressor
    {
        auto c50 = render (dry, { { "comp", 0.5f } });
        auto c100s = render (dry, { { "comp", 1.0f } });
        auto c60s = render (dry, { { "comp", 0.6f } });
        auto c60f = render (dry, { { "comp", 0.6f }, { "attack", 1.0f } });
        auto crest = [&] (const Result& r) { return peakDb (r.out, 0, nSig) - rmsDb (r.out.getReadPointer (0), nSig); };
        std::printf ("Comp 50%%: GR %.1f dB | 100%%: GR %.1f dB | Crest-Faktor 60%% slow %.1f dB, fast %.1f dB (dry %.1f)\n",
                     c50.compGr, c100s.compGr, crest (c60s), crest (c60f), -6.0f - dryRms);
        check (c50.compGr > 2.0f && c100s.compGr > c50.compGr, "Mehr Regler = mehr Kompression");
        std::printf ("  GR slow %.1f fast %.1f, Peak slow %.1f fast %.1f, RMS slow %.1f fast %.1f\n", c60s.compGr, c60f.compGr, peakDb (c60s.out,0,nSig), peakDb (c60f.out,0,nSig), rmsDb (c60s.out.getReadPointer (0), nSig), rmsDb (c60f.out.getReadPointer (0), nSig));
        check (c60f.compGr > c60s.compGr + 2.0f && peakDb (c60f.out, 0, nSig) < peakDb (c60s.out, 0, nSig) - 1.0f,
               "Fast fängt Transienten (mehr Reduktion, niedrigere Spitzen), Slow lässt sie durch");
    }

    // Hall: Ausklang nach dem Loop
    {
        float lastTail = -200.0f;
        const char* names[] = { "Plate", "Room", "Hall", "Space" };
        const float pos[] = { 0.125f, 0.375f, 0.625f, 0.875f };
        float tails[4];
        for (int k = 0; k < 4; ++k)
        {
            auto r = render (dry, { { "space", pos[k] }, { "spacemix", 0.5f } });
            const int t0 = nSig + (int) (0.7 * SR);      // 0,7 s nach Loop-Ende
            tails[k] = rmsDb (r.out.getReadPointer (0) + t0, (int) (0.8 * SR));
            juce::AudioBuffer<float> wetOnly (1, nSig);
            for (int i = 0; i < nSig; ++i) wetOnly.setSample (0, i, r.out.getSample (0, i) - neutral.out.getSample (0, i));
            const float t02 = rmsDb (r.out.getReadPointer (0) + nSig + (int) (0.15 * SR), (int) (0.1 * SR));
            std::printf ("%s: Hall-Anteil %.1f dB (trocken %.1f), 0,2 s nach Ende %.1f dB, 1,1 s nach Ende %.1f dB\n", names[k],
                         rmsDb (wetOnly.getReadPointer (0), nSig), dryRms, t02, tails[k]);
            writeWav (outDir.getChildFile (juce::String ("space-") + names[k] + ".wav"), r.out);
        }
        lastTail = tails[0];
        check (tails[2] > tails[1] + 6.0f && tails[3] > tails[2], "Hall und Space klingen länger aus als Room");

        // Mix-Fader regelt die Menge, das Poti innerhalb einer Hall-Art die Raumgröße
        auto wetRms = [&] (float sp, float mx)
        {
            auto r = render (dry, { { "space", sp }, { "spacemix", mx } });
            juce::AudioBuffer<float> w (1, nSig);
            for (int i = 0; i < nSig; ++i) w.setSample (0, i, r.out.getSample (0, i) - neutral.out.getSample (0, i));
            return std::pair<float, float> { rmsDb (w.getReadPointer (0), nSig),
                                             rmsDb (r.out.getReadPointer (0) + nSig + (int) (0.7 * SR), (int) (0.8 * SR)) };
        };
        const auto m25 = wetRms (0.625f, 0.25f), m50 = wetRms (0.625f, 0.5f), m100 = wetRms (0.625f, 1.0f);
        std::printf ("Hall-Mix 25 %%: %.1f dB, 50 %%: %.1f dB, 100 %%: %.1f dB\n", m25.first, m50.first, m100.first);
        check (m25.first < m50.first - 3.0f && m50.first < m100.first - 3.0f, "Mehr Mix = mehr Hall");
        const auto small = wetRms (0.51f, 0.5f), big = wetRms (0.74f, 0.5f);
        std::printf ("Hall klein: Ausklang %.1f dB, Hall groß: %.1f dB\n", small.second, big.second);
        check (big.second > small.second + 6.0f, "Weiter drehen innerhalb einer Hall-Art = größerer Raum");
        float lo = 1e9f, hi = -1e9f;
        for (float sp : { 0.02f, 0.23f, 0.27f, 0.48f, 0.52f, 0.73f, 0.77f, 0.98f })
        {
            const float w = wetRms (sp, 0.5f).first;
            std::printf ("  Space %.2f: Hall-Anteil %.1f dB\n", sp, w);
            lo = juce::jmin (lo, w); hi = juce::jmax (hi, w);
        }
        check (hi - lo < 6.0f, "Ähnliche Hall-Menge über alle Arten/Größen bei gleichem Mix (Spanne " + juce::String (hi - lo, 1) + " dB)");
        juce::ignoreUnused (lastTail);
        auto zero = render (dry, { { "space", 0.6f }, { "spacemix", 0.0f } });
        check (rmsDb (zero.out.getReadPointer (0) + nSig + (int) (0.7 * SR), (int) (0.8 * SR)) < -100.0f, "Mix 0 = kein Hall");
    }

    // Crush
    {
        auto cr = render (dry, { { "crush", 1.0f } });
        const float pk = peakDb (cr.out, 0, nAll), rms = rmsDb (cr.out.getReadPointer (0), nSig);
        std::printf ("Crush 100%%: Peak %.2f dB, RMS %.1f dB (+%.1f), Limiter-GR %.1f dB\n", pk, rms, rms - dryRms, cr.limGr);
        check (pk < 0.0f, "Crush: kein Clipping über 0 dBFS");
        check (rms > dryRms + 8.0f, "Crush macht deutlich lauter");
    }

    // Zufällige Parameter: keine NaN/Inf, keine Übersteuerung
    {
        std::mt19937 rng (3);
        std::uniform_real_distribution<float> u (0.0f, 1.0f);
        bool finite = true; float maxPk = -200;
        for (int k = 0; k < 6; ++k)
        {
            auto r = render (dry, { { "low", -24 + 36 * u (rng) }, { "high", -24 + 36 * u (rng) }, { "comp", u (rng) },
                                    { "attack", u (rng) > 0.5f ? 1.0f : 0.0f }, { "space", u (rng) }, { "spacemix", u (rng) }, { "crush", 0.05f + u (rng) } });
            for (int c = 0; c < 2; ++c) for (int i = 0; i < nAll; ++i) finite &= std::isfinite (r.out.getSample (c, i));
            maxPk = juce::jmax (maxPk, peakDb (r.out, 0, nAll));
        }
        check (finite, "Keine NaN/Inf bei zufälligen Einstellungen");
        check (maxPk < 0.0f, "Mit Crush > 0 nie über 0 dBFS (max " + juce::String (maxPk, 2) + " dB)");
    }

    // Hörbeispiele
    {
        juce::AudioBuffer<float> dryStereo (2, nAll);
        dryStereo.copyFrom (0, 0, dry, 0, 0, nAll);
        dryStereo.copyFrom (1, 0, dry, 0, 0, nAll);
        writeWav (outDir.getChildFile ("00-dry.wav"), dryStereo);
        writeWav (outDir.getChildFile ("01-neutral.wav"), neutral.out);
        writeWav (outDir.getChildFile ("02-fat.wav"),
                  render (dry, { { "low", 3.0f }, { "high", 1.0f }, { "comp", 0.55f }, { "space", 0.42f }, { "spacemix", 0.5f }, { "crush", 0.45f } }).out);
        writeWav (outDir.getChildFile ("03-smash.wav"),
                  render (dry, { { "low", 4.0f }, { "comp", 0.9f }, { "attack", 1.0f }, { "space", 0.7f }, { "spacemix", 0.6f }, { "crush", 0.85f } }).out);
    }

    // Bildschirmfoto der Oberfläche
    {
        OneMicDrumsProcessor p;
        for (auto [id, v] : std::map<juce::String, float> { { "low", 3.0f }, { "high", 1.0f }, { "comp", 0.55f }, { "space", 0.42f }, { "spacemix", 0.35f }, { "crush", 0.45f } })
            p.apvts.getParameter (id)->setValueNotifyingHost (p.apvts.getParameter (id)->convertTo0to1 (v));
        std::unique_ptr<juce::AudioProcessorEditor> ed (p.createEditor());
        ed->setSize (760, 400);
        auto img = ed->createComponentSnapshot (ed->getLocalBounds(), true, 2.0f);
        juce::PNGImageFormat png;
        auto f = outDir.getChildFile ("gui.png");
        f.deleteFile();
        juce::FileOutputStream os (f);
        png.writeImageToStream (img, os);
    }

    std::printf (fails == 0 ? "OMD OK\n" : "OMD: %d Fehler\n", fails);
    return fails == 0 ? 0 : 1;
}
