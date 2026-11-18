#include "PluginProcessor.h"
#include "PluginEditor.h"

namespace
{
    constexpr float kLimiterCeiling = 0.944f;   // −0,5 dBFS
    constexpr float kMaxDriveDb = 20.0f;

    inline float coefFor (double timeSeconds, double sampleRate)
    {
        return (float) std::exp (-1.0 / (timeSeconds * sampleRate));
    }

    inline float smoothstep (float e0, float e1, float x)
    {
        const float t = juce::jlimit (0.0f, 1.0f, (x - e0) / (e1 - e0));
        return t * t * (3.0f - 2.0f * t);
    }
}

//==============================================================================
// OneKnobCompressor
//==============================================================================
namespace omd
{
void OneKnobCompressor::prepare (double sampleRate)
{
    sr = sampleRate;
    makeup.reset (sampleRate, 0.05);
    reset();
    setAmount (0.0f, false);
}

void OneKnobCompressor::reset()
{
    envDb = 0.0f;
    lastGrDb = 0.0f;
}

void OneKnobCompressor::setAmount (float a, bool fastAttack)
{
    a = juce::jlimit (0.0f, 1.0f, a);
    // Je weiter aufgedreht: Threshold sinkt, Ratio steigt (1:1 … 12:1).
    thresholdDb = -32.0f * std::pow (a, 0.75f);
    ratio       = 1.0f + 11.0f * std::pow (a, 1.6f);
    kneeDb      = 8.0f - 4.0f * a;

    // Slow lässt den Anschlag durch (Punch), Fast greift die Transiente.
    attackCoef  = coefFor (fastAttack ? 0.0008 : 0.025, sr);
    releaseCoef = coefFor (fastAttack ? 0.070  : 0.160, sr);

    // Automatische Aufholverstärkung: etwa die Hälfte der Reduktion bei Vollaussteuerung.
    const float makeupDb = -thresholdDb * (1.0f - 1.0f / ratio) * 0.45f;
    makeup.setTargetValue (juce::Decibels::decibelsToGain (makeupDb));
}

float OneKnobCompressor::computeGainDb (float levelDb) const noexcept
{
    const float over = levelDb - thresholdDb;
    if (2.0f * over < -kneeDb)
        return 0.0f;
    if (2.0f * std::abs (over) <= kneeDb)
    {
        const float t = over + kneeDb * 0.5f;
        return (1.0f / ratio - 1.0f) * t * t / (2.0f * kneeDb);
    }
    return (1.0f / ratio - 1.0f) * over;
}

float OneKnobCompressor::computeGain (float x)
{
    const float levelDb = juce::Decibels::gainToDecibels (std::abs (x), -120.0f);
    const float targetGr = -computeGainDb (levelDb);        // positiv = Reduktion
    const float coef = targetGr > envDb ? attackCoef : releaseCoef;
    envDb = targetGr + coef * (envDb - targetGr);
    lastGrDb = envDb;
    return juce::Decibels::decibelsToGain (-envDb) * makeup.getNextValue();
}

//==============================================================================
// MonoToStereo
//==============================================================================
void MonoToStereo::prepare (double sampleRate)
{
    sr = sampleRate;
    d1 = (int) std::round (0.0097 * sr);    // zwei nicht-harmonische Verzögerungen
    d2 = (int) std::round (0.0173 * sr);
    delay.assign ((size_t) (d2 + 2), 0.0f);
    sideHp.coefficients = juce::dsp::IIR::Coefficients<float>::makeHighPass (sr, 300.0f);
    reset();
}

void MonoToStereo::reset()
{
    std::fill (delay.begin(), delay.end(), 0.0f);
    writePos = 0;
    sideHp.reset();
}

void MonoToStereo::process (const float* low, const float* high, float* left, float* right, int n)
{
    const int size = (int) delay.size();
    for (int i = 0; i < n; ++i)
    {
        delay[(size_t) writePos] = high[i];
        auto tap = [&] (int d) { int r = writePos - d; if (r < 0) r += size; return delay[(size_t) r]; };
        const float side = sideHp.processSample (tap (d1) - 0.55f * tap (d2)) * width;
        if (++writePos >= size) writePos = 0;

        const float mid = low[i] + high[i];
        left[i]  = mid + side;     // L + R = 2 · Mid → in Mono keine Auslöschung/Kammfilter
        right[i] = mid - side;
    }
}

//==============================================================================
// SpaceReverb
//==============================================================================
SpaceReverb::Character SpaceReverb::characterFor (float x)
{
    // Ankerpunkte jeweils in der Mitte des Viertels.
    static const Character anchors[4] =
    {
        //  size  damp  pre   wet   lowCut  highCut
        { 0.70f, 0.05f,  0.0f, 1.25f, 260.0f, 12000.0f },   // Plate: dicht, hell, ohne Pre-Delay
        { 0.52f, 0.50f,  7.0f, 1.45f, 200.0f,  8000.0f },   // Room: kurz, natürlich
        { 0.84f, 0.40f, 24.0f, 1.10f, 180.0f,  7500.0f },   // Hall: lang, Pre-Delay
        { 0.97f, 0.28f, 48.0f, 0.95f, 150.0f,  6500.0f },   // Space: sehr groß, langer Ausklang
    };

    const float t = juce::jlimit (0.0f, 3.0f, x * 4.0f - 0.5f);
    const int i0 = juce::jmin ((int) t, 2);
    const float f = t - (float) i0;
    const auto& a = anchors[i0];
    const auto& b = anchors[i0 + 1];
    auto mix = [f] (float p, float q) { return p + (q - p) * f; };

    Character c { mix (a.size, b.size), mix (a.damping, b.damping), mix (a.preDelayMs, b.preDelayMs),
                  mix (a.wet, b.wet), mix (a.lowCutHz, b.lowCutHz), mix (a.highCutHz, b.highCutHz) };

    // Von 0 aus sanft einblenden (erstes Achtel), danach volle Hall-Menge.
    c.wet *= smoothstep (0.0f, 0.125f, x);
    return c;
}

juce::String SpaceReverb::typeNameFor (float x)
{
    if (x < 0.005f) return "Dry";
    if (x < 0.25f)  return "Plate";
    if (x < 0.50f)  return "Room";
    if (x < 0.75f)  return "Hall";
    return "Space";
}

void SpaceReverb::prepare (double sampleRate, int maxBlock)
{
    sr = sampleRate;
    reverb.setSampleRate (sampleRate);
    preDelay.assign ((size_t) (0.1 * sr) + 4, 0.0f);
    preDelaySamples.reset (sampleRate, 0.2);
    wet.reset (sampleRate, 0.05);
    bufL.assign ((size_t) maxBlock, 0.0f);
    bufR.assign ((size_t) maxBlock, 0.0f);
    params.dryLevel = 0.0f;
    params.width = 1.0f;
    params.freezeMode = 0.0f;
    lastAmount = -1.0f;
    reset();
}

void SpaceReverb::reset()
{
    reverb.reset();
    sendHp.reset();
    sendLp.reset();
    std::fill (preDelay.begin(), preDelay.end(), 0.0f);
    writePos = 0;
}

void SpaceReverb::setAmount (float x)
{
    if (std::abs (x - lastAmount) < 1.0e-4f)
        return;
    const bool first = lastAmount < 0.0f;
    lastAmount = x;

    const auto c = characterFor (x);
    params.roomSize = c.size;
    params.damping = c.damping;
    params.wetLevel = 0.33f;              // juce::Reverb skaliert intern ×3
    reverb.setParameters (params);

    // Send-Filter: kein Bass-Matsch im Hall, keine scharfen Höhen (außer Plate).
    if (std::abs (c.lowCutHz - lowCut) > 1.0f || std::abs (c.highCutHz - highCut) > 10.0f)
    {
        lowCut = c.lowCutHz;
        highCut = c.highCutHz;
        sendHp.coefficients = juce::dsp::IIR::Coefficients<float>::makeHighPass (sr, lowCut);
        sendLp.coefficients = juce::dsp::IIR::Coefficients<float>::makeLowPass (sr, highCut);
    }

    const float pd = c.preDelayMs * 0.001f * (float) sr;
    if (first) { preDelaySamples.setCurrentAndTargetValue (pd); wet.setCurrentAndTargetValue (c.wet); }
    else       { preDelaySamples.setTargetValue (pd);           wet.setTargetValue (c.wet); }
}

void SpaceReverb::processAdd (const float* send, float* left, float* right, int n)
{
    // Ganz zu: Hall noch ausklingen lassen, aber nichts Neues einspeisen.
    const bool silentInput = wet.getTargetValue() <= 0.0f && ! wet.isSmoothing();

    const int size = (int) preDelay.size();
    for (int i = 0; i < n; ++i)
    {
        const float in = silentInput ? 0.0f : sendLp.processSample (sendHp.processSample (send[i]));
        preDelay[(size_t) writePos] = in;

        float rp = (float) writePos - preDelaySamples.getNextValue();
        if (rp < 0.0f) rp += (float) size;
        const int r0 = (int) rp;
        const int r1 = (r0 + 1) % size;
        const float fr = rp - (float) r0;
        const float delayed = preDelay[(size_t) r0] + fr * (preDelay[(size_t) r1] - preDelay[(size_t) r0]);
        if (++writePos >= size) writePos = 0;

        const float g = wet.getNextValue();
        bufL[(size_t) i] = delayed * g;
        bufR[(size_t) i] = delayed * g;
    }

    reverb.processStereo (bufL.data(), bufR.data(), n);

    for (int i = 0; i < n; ++i)
    {
        left[i]  += bufL[(size_t) i];     // Parallel-Bus: Hall wird zum trockenen Signal addiert
        right[i] += bufR[(size_t) i];
    }
}
} // namespace omd

//==============================================================================
// Processor
//==============================================================================
OneMicDrumsProcessor::OneMicDrumsProcessor()
    : AudioProcessor (BusesProperties()
                          .withInput ("Input", juce::AudioChannelSet::mono(), true)
                          .withOutput ("Output", juce::AudioChannelSet::stereo(), true)),
      apvts (*this, nullptr, "STATE", createLayout())
{
    pLow    = dynamic_cast<juce::AudioParameterFloat*>  (apvts.getParameter ("low"));
    pHigh   = dynamic_cast<juce::AudioParameterFloat*>  (apvts.getParameter ("high"));
    pComp   = dynamic_cast<juce::AudioParameterFloat*>  (apvts.getParameter ("comp"));
    pAttack = dynamic_cast<juce::AudioParameterChoice*> (apvts.getParameter ("attack"));
    pSpace  = dynamic_cast<juce::AudioParameterFloat*>  (apvts.getParameter ("space"));
    pCrush  = dynamic_cast<juce::AudioParameterFloat*>  (apvts.getParameter ("crush"));
    pOutput = dynamic_cast<juce::AudioParameterFloat*>  (apvts.getParameter ("output"));
    jassert (pLow && pHigh && pComp && pAttack && pSpace && pCrush && pOutput);
}

juce::AudioProcessorValueTreeState::ParameterLayout OneMicDrumsProcessor::createLayout()
{
    using namespace juce;
    AudioProcessorValueTreeState::ParameterLayout layout;

    auto dB = AudioParameterFloatAttributes().withLabel ("dB")
                  .withStringFromValueFunction ([] (float v, int) { return (v > 0 ? "+" : "") + String (v, 1) + " dB"; });
    auto pct = AudioParameterFloatAttributes().withLabel ("%")
                  .withStringFromValueFunction ([] (float v, int) { return String (roundToInt (v * 100.0f)) + " %"; });

    layout.add (std::make_unique<AudioParameterFloat> (ParameterID { "low", 1 }, "Low (< 160 Hz)",
                                                       NormalisableRange<float> (-24.0f, 12.0f, 0.1f), 0.0f, dB));
    layout.add (std::make_unique<AudioParameterFloat> (ParameterID { "high", 1 }, "High (> 160 Hz)",
                                                       NormalisableRange<float> (-24.0f, 12.0f, 0.1f), 0.0f, dB));
    layout.add (std::make_unique<AudioParameterFloat> (ParameterID { "comp", 1 }, "Compress",
                                                       NormalisableRange<float> (0.0f, 1.0f, 0.001f), 0.0f, pct));
    layout.add (std::make_unique<AudioParameterChoice> (ParameterID { "attack", 1 }, "Attack",
                                                        StringArray { "Slow", "Fast" }, 0));
    layout.add (std::make_unique<AudioParameterFloat> (ParameterID { "space", 1 }, "Space",
                    NormalisableRange<float> (0.0f, 1.0f, 0.001f), 0.0f,
                    AudioParameterFloatAttributes().withStringFromValueFunction ([] (float v, int)
                    {
                        return omd::SpaceReverb::typeNameFor (v) + (v >= 0.005f ? " " + String (roundToInt (v * 100.0f)) + " %" : String());
                    })));
    layout.add (std::make_unique<AudioParameterFloat> (ParameterID { "crush", 1 }, "Crush",
                                                       NormalisableRange<float> (0.0f, 1.0f, 0.001f), 0.0f, pct));
    layout.add (std::make_unique<AudioParameterFloat> (ParameterID { "output", 1 }, "Output",
                                                       NormalisableRange<float> (-24.0f, 6.0f, 0.1f), 0.0f, dB));
    return layout;
}

bool OneMicDrumsProcessor::isBusesLayoutSupported (const BusesLayout& layouts) const
{
    const auto in = layouts.getMainInputChannelSet();
    const auto out = layouts.getMainOutputChannelSet();
    // Gedacht für Mono → Stereo; Stereo → Stereo geht auch (Eingang wird zu Mono summiert).
    return out == juce::AudioChannelSet::stereo()
        && (in == juce::AudioChannelSet::mono() || in == juce::AudioChannelSet::stereo());
}

void OneMicDrumsProcessor::prepareToPlay (double sampleRate, int samplesPerBlock)
{
    const auto block = (juce::uint32) juce::jmax (1, samplesPerBlock);
    juce::dsp::ProcessSpec monoSpec { sampleRate, block, 1 };

    lowPass.setType (juce::dsp::LinkwitzRileyFilterType::lowpass);
    lowPass.setCutoffFrequency (crossoverHz);
    lowPass.prepare (monoSpec);

    mono.setSize (1, (int) block);
    lowBand.setSize (1, (int) block);
    highBand.setSize (1, (int) block);

    for (auto* s : { &lowGain, &highGain, &outGain })
        s->reset (sampleRate, 0.03);
    drive.reset (sampleRate * 4.0, 0.03);
    clipAmount.reset (sampleRate * 4.0, 0.03);

    comp.prepare (sampleRate);
    widener.prepare (sampleRate);
    space.prepare (sampleRate, (int) block);

    oversampling = std::make_unique<juce::dsp::Oversampling<float>> (
        2, 2, juce::dsp::Oversampling<float>::filterHalfBandPolyphaseIIR, true, true);
    oversampling->initProcessing (block);
    limLookahead = juce::jmax (8, (int) std::round (0.001 * sampleRate));   // 1 ms
    limDelayL.assign ((size_t) limLookahead, 0.0f);
    limDelayR.assign ((size_t) limLookahead, 0.0f);
    limAvgBuf.assign ((size_t) limLookahead, 1.0f);
    limMinQueue.assign ((size_t) limLookahead + 2, { 0, 1.0f });
    limRelease = coefFor (0.12, sampleRate);
    resetLimiter();
    setLatencySamples ((int) std::round (oversampling->getLatencyInSamples()) + limLookahead);

    // Startwerte ohne Rampe
    lowGain.setCurrentAndTargetValue (bandGain (pLow->get()));
    highGain.setCurrentAndTargetValue (bandGain (pHigh->get()));
    outGain.setCurrentAndTargetValue (juce::Decibels::decibelsToGain (pOutput->get()));
}

void OneMicDrumsProcessor::resetLimiter()
{
    std::fill (limDelayL.begin(), limDelayL.end(), 0.0f);
    std::fill (limDelayR.begin(), limDelayR.end(), 0.0f);
    std::fill (limAvgBuf.begin(), limAvgBuf.end(), 1.0f);
    limAvgSum = (double) limLookahead;
    limQHead = limQTail = 0;
    limPos = 0;
    limIndex = 0;
    limGain = 1.0f;
}

// Gleitendes Minimum der Ziel-Gains über die Lookahead-Länge, danach gleitender
// Mittelwert über dieselbe Länge: Der Gain ist garantiert unten, wenn die Spitze
// (um die Lookahead-Länge verzögert) am Ausgang ankommt – ohne harten Sprung.
float OneMicDrumsProcessor::limiterGain (float peak)
{
    const float target = peak > kLimiterCeiling ? kLimiterCeiling / peak : 1.0f;
    const int cap = (int) limMinQueue.size();
    const int idx = limIndex++;

    while (limQHead != limQTail)
    {
        const int last = (limQTail - 1 + cap) % cap;
        if (limMinQueue[(size_t) last].second >= target) limQTail = last; else break;
    }
    limMinQueue[(size_t) limQTail] = { idx, target };
    limQTail = (limQTail + 1) % cap;
    while (limMinQueue[(size_t) limQHead].first < idx - limLookahead)
        limQHead = (limQHead + 1) % cap;
    const float held = limMinQueue[(size_t) limQHead].second;

    limAvgSum += held - limAvgBuf[(size_t) limPos];
    limAvgBuf[(size_t) limPos] = held;
    const float avg = (float) (limAvgSum / limLookahead);

    limGain = avg < limGain ? avg : avg + limRelease * (limGain - avg);
    if (limIndex > (1 << 30)) // Überlauf vermeiden
    {
        for (auto& q : limMinQueue) q.first -= (1 << 29);
        limIndex -= (1 << 29);
    }
    return limGain;
}

void OneMicDrumsProcessor::processCrush (juce::AudioBuffer<float>& stereo, int n)
{
    const float c = pCrush->get();
    drive.setTargetValue (juce::Decibels::decibelsToGain (kMaxDriveDb * c));
    clipAmount.setTargetValue (juce::jlimit (0.0f, 1.0f, c * 1.4f));
    // Je mehr Crush, desto schneller erholt sich der Limiter → dichter, lauter.
    limRelease = coefFor (0.12 - 0.09 * c, getSampleRate());

    // a) Drive + Sättigung mit 4× Oversampling (keine Aliasing-Artefakte)
    juce::dsp::AudioBlock<float> block (stereo.getArrayOfWritePointers(), 2, (size_t) n);
    auto up = oversampling->processSamplesUp (block);
    auto* uL = up.getChannelPointer (0);
    auto* uR = up.getChannelPointer (1);
    for (size_t i = 0; i < up.getNumSamples(); ++i)
    {
        const float g = drive.getNextValue();
        const float m = clipAmount.getNextValue();
        const float l = uL[i] * g, r = uR[i] * g;
        uL[i] = l + m * (std::tanh (l) - l);     // rundet Spitzen ab („crush“)
        uR[i] = r + m * (std::tanh (r) - r);
    }
    oversampling->processSamplesDown (block);

    // b) Gelinkter Lookahead-Limiter, Decke −0,5 dBFS
    auto* L = stereo.getWritePointer (0);
    auto* R = stereo.getWritePointer (1);
    float maxGr = 0.0f;
    for (int i = 0; i < n; ++i)
    {
        const float g = limiterGain (juce::jmax (std::abs (L[i]), std::abs (R[i])));
        const int p = limPos;
        const float dl = limDelayL[(size_t) p], dr = limDelayR[(size_t) p];
        limDelayL[(size_t) p] = L[i];
        limDelayR[(size_t) p] = R[i];
        if (++limPos >= limLookahead) limPos = 0;

        L[i] = juce::jlimit (-kLimiterCeiling, kLimiterCeiling, dl * g);
        R[i] = juce::jlimit (-kLimiterCeiling, kLimiterCeiling, dr * g);
        maxGr = juce::jmax (maxGr, -juce::Decibels::gainToDecibels (g, -60.0f));
    }
    crushReductionDb.store (maxGr);
}

void OneMicDrumsProcessor::processBlock (juce::AudioBuffer<float>& buffer, juce::MidiBuffer&)
{
    juce::ScopedNoDenormals noDenormals;
    const int n = buffer.getNumSamples();
    const int numIn = getTotalNumInputChannels();
    if (n == 0 || buffer.getNumChannels() < 2)
        return;

    // Puffer wachsen lassen, falls der Host größere Blöcke schickt als angekündigt
    if (mono.getNumSamples() < n)
        prepareToPlay (getSampleRate(), n);

    // 1) Eingang → Mono
    auto* m = mono.getWritePointer (0);
    if (numIn >= 2)
        for (int i = 0; i < n; ++i)
            m[i] = 0.5f * (buffer.getSample (0, i) + buffer.getSample (1, i));
    else
        juce::FloatVectorOperations::copy (m, buffer.getReadPointer (0), n);

    // 2) Frequenzweiche 160 Hz (Linkwitz-Riley: Summe ist phasen-/pegelneutral)
    lowGain.setTargetValue (bandGain (pLow->get()));      // ganz links = aus
    highGain.setTargetValue (bandGain (pHigh->get()));

    auto* lo = lowBand.getWritePointer (0);
    auto* hi = highBand.getWritePointer (0);
    for (int i = 0; i < n; ++i)
    {
        float l, h;
        lowPass.processSample (0, m[i], l, h);
        lo[i] = l * lowGain.getNextValue();
        hi[i] = h * highGain.getNextValue();
    }

    // 3) Kompressor (Detektor auf der Summe, gleicher Gain auf beide Bänder)
    comp.setAmount (pComp->get(), pAttack->getIndex() == 1);
    float maxGr = 0.0f;
    for (int i = 0; i < n; ++i)
    {
        const float g = comp.computeGain (lo[i] + hi[i]);
        lo[i] *= g;
        hi[i] *= g;
        m[i] = lo[i] + hi[i];               // Send für den Hall
        maxGr = juce::jmax (maxGr, comp.getGainReductionDb());
    }
    gainReductionDb.store (maxGr);

    // 4) Mono → Stereo
    auto* L = buffer.getWritePointer (0);
    auto* R = buffer.getWritePointer (1);
    widener.process (lo, hi, L, R, n);
    for (int ch = 2; ch < buffer.getNumChannels(); ++ch)
        buffer.clear (ch, 0, n);

    // 5) Hall als Parallel-Bus
    space.setAmount (pSpace->get());
    space.processAdd (m, L, R, n);

    // 6) Crush / Limiter
    processCrush (buffer, n);

    // 7) Ausgang
    outGain.setTargetValue (juce::Decibels::decibelsToGain (pOutput->get()));
    for (int i = 0; i < n; ++i)
    {
        const float g = outGain.getNextValue();
        L[i] *= g;
        R[i] *= g;
    }
}

juce::AudioProcessorEditor* OneMicDrumsProcessor::createEditor()
{
    return new OneMicDrumsEditor (*this);
}

void OneMicDrumsProcessor::getStateInformation (juce::MemoryBlock& destData)
{
    if (auto xml = apvts.copyState().createXml())
        copyXmlToBinary (*xml, destData);
}

void OneMicDrumsProcessor::setStateInformation (const void* data, int sizeInBytes)
{
    if (auto xml = getXmlFromBinary (data, sizeInBytes))
        if (xml->hasTagName (apvts.state.getType()))
            apvts.replaceState (juce::ValueTree::fromXml (*xml));
}

juce::AudioProcessor* JUCE_CALLTYPE createPluginFilter()
{
    return new OneMicDrumsProcessor();
}
