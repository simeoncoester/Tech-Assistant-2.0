#include "PluginEditor.h"

namespace colours
{
    const juce::Colour bg       { 0xff15171c };
    const juce::Colour panel    { 0xff1e2128 };
    const juce::Colour edge     { 0xff2e323c };
    const juce::Colour text     { 0xffe8eaee };
    const juce::Colour dim      { 0xff8a909c };
    const juce::Colour low      { 0xffe8833a };   // orange
    const juce::Colour high     { 0xff4fa3e8 };   // blau
    const juce::Colour comp     { 0xffe0c045 };   // gelb
    const juce::Colour space    { 0xff9b7be8 };   // violett
    const juce::Colour crush    { 0xffe0484b };   // rot
    const juce::Colour out      { 0xffb8bcc6 };
}

//==============================================================================
OmdLookAndFeel::OmdLookAndFeel()
{
    setColour (juce::Slider::textBoxTextColourId, colours::text);
    setColour (juce::Slider::textBoxOutlineColourId, juce::Colours::transparentBlack);
    setColour (juce::Slider::textBoxBackgroundColourId, juce::Colours::transparentBlack);
    setColour (juce::TextButton::textColourOffId, colours::dim);
    setColour (juce::TextButton::textColourOnId, colours::text);
}

void OmdLookAndFeel::drawRotarySlider (juce::Graphics& g, int x, int y, int w, int h, float pos,
                                       float a0, float a1, juce::Slider& s)
{
    const auto accent = s.findColour (juce::Slider::rotarySliderFillColourId);
    auto area = juce::Rectangle<float> ((float) x, (float) y, (float) w, (float) h).reduced (6.0f);
    const float d = juce::jmin (area.getWidth(), area.getHeight());
    area = area.withSizeKeepingCentre (d, d);
    const auto c = area.getCentre();
    const float r = d * 0.5f;
    const float angle = a0 + pos * (a1 - a0);

    // Ring: Hintergrund + Wert
    const float ringW = juce::jmax (3.0f, r * 0.09f);
    juce::Path track, value;
    track.addCentredArc (c.x, c.y, r - ringW, r - ringW, 0.0f, a0, a1, true);
    value.addCentredArc (c.x, c.y, r - ringW, r - ringW, 0.0f, a0, angle, true);
    g.setColour (colours::edge);
    g.strokePath (track, juce::PathStrokeType (ringW, juce::PathStrokeType::curved, juce::PathStrokeType::rounded));
    g.setColour (accent);
    g.strokePath (value, juce::PathStrokeType (ringW, juce::PathStrokeType::curved, juce::PathStrokeType::rounded));

    // Knopf
    const float kr = r * 0.70f;
    auto knob = juce::Rectangle<float> (kr * 2.0f, kr * 2.0f).withCentre (c);
    g.setColour (juce::Colours::black.withAlpha (0.45f));
    g.fillEllipse (knob.translated (0.0f, r * 0.06f));
    g.setGradientFill (juce::ColourGradient (juce::Colour (0xff3a3f4a), c.x, knob.getY(),
                                             juce::Colour (0xff1c1f25), c.x, knob.getBottom(), false));
    g.fillEllipse (knob);
    g.setColour (juce::Colours::white.withAlpha (0.10f));
    g.drawEllipse (knob.reduced (0.5f), 1.0f);

    // Zeiger
    juce::Path ptr;
    ptr.addRoundedRectangle (-1.6f, -kr * 0.92f, 3.2f, kr * 0.45f, 1.6f);
    g.setColour (accent.brighter (0.3f));
    g.fillPath (ptr, juce::AffineTransform::rotation (angle).translated (c.x, c.y));
}

void OmdLookAndFeel::drawButtonBackground (juce::Graphics& g, juce::Button& b, const juce::Colour&,
                                           bool highlighted, bool)
{
    auto r = b.getLocalBounds().toFloat().reduced (1.0f);
    const bool on = b.getToggleState();
    const auto accent = colours::comp;
    g.setColour (on ? accent.withAlpha (0.16f) : colours::panel.brighter (highlighted ? 0.06f : 0.0f));
    g.fillRoundedRectangle (r, 8.0f);
    g.setColour (on ? accent : colours::edge);
    g.drawRoundedRectangle (r, 8.0f, on ? 1.5f : 1.0f);
}

//==============================================================================
OmdKnob::OmdKnob (juce::AudioProcessorValueTreeState& state, const juce::String& id,
                  const juce::String& t, juce::Colour a, bool b)
    : title (t), accent (a), big (b)
{
    slider.setSliderStyle (juce::Slider::RotaryHorizontalVerticalDrag);
    slider.setTextBoxStyle (juce::Slider::TextBoxBelow, false, 110, 20);
    slider.setColour (juce::Slider::rotarySliderFillColourId, accent);
    slider.setColour (juce::Slider::textBoxOutlineColourId, juce::Colours::transparentBlack);
    slider.setColour (juce::Slider::textBoxTextColourId, colours::text);
    slider.setRotaryParameters (juce::MathConstants<float>::pi * 1.25f,
                                juce::MathConstants<float>::pi * 2.75f, true);
    slider.setVelocityBasedMode (false);
    slider.setMouseDragSensitivity (220);
    addAndMakeVisible (slider);
    attachment = std::make_unique<juce::AudioProcessorValueTreeState::SliderAttachment> (state, id, slider);
    slider.setDoubleClickReturnValue (true, (double) state.getParameter (id)->convertFrom0to1 (
                                                state.getParameter (id)->getDefaultValue()));
    setInterceptsMouseClicks (false, true);
}

void OmdKnob::resized()
{
    auto r = getLocalBounds();
    r.removeFromTop (juce::roundToInt ((big ? 26.0f : 22.0f) * scale));
    slider.setBounds (r.reduced (insetX, 0));
}

void OmdKnob::paint (juce::Graphics& g)
{
    g.setColour (colours::text);
    g.setFont (juce::FontOptions ((big ? 15.0f : 12.5f) * scale, juce::Font::bold));
    g.drawText (title.toUpperCase(), getLocalBounds().removeFromTop (juce::roundToInt ((big ? 24.0f : 20.0f) * scale)),
                juce::Justification::centred);
}

//==============================================================================
OneMicDrumsEditor::OneMicDrumsEditor (OneMicDrumsProcessor& p)
    : AudioProcessorEditor (p), proc (p),
      low    (p.apvts, "low",    "Low",      colours::low,   false),
      high   (p.apvts, "high",   "High",     colours::high,  false),
      comp   (p.apvts, "comp",   "Compress", colours::comp,  true),
      space  (p.apvts, "space",  "Space",    colours::space, true),
      crush  (p.apvts, "crush",  "Crush",    colours::crush, true),
      output (p.apvts, "output", "Output",   colours::out,   false),
      attackAttachment (*p.apvts.getParameter ("attack"), [this] (float v)
      {
          slowBtn.setToggleState (v < 0.5f, juce::dontSendNotification);
          fastBtn.setToggleState (v >= 0.5f, juce::dontSendNotification);
      })
{
    setLookAndFeel (&lnf);
    for (auto* k : { &low, &high, &comp, &space, &crush, &output })
        addAndMakeVisible (*k);

    for (auto* b : { &slowBtn, &fastBtn })
    {
        b->setClickingTogglesState (false);
        addAndMakeVisible (*b);
    }
    slowBtn.onClick = [this] { attackAttachment.setValueAsCompleteGesture (0.0f); };
    fastBtn.onClick = [this] { attackAttachment.setValueAsCompleteGesture (1.0f); };
    attackAttachment.sendInitialUpdate();

    slowBtn.setTooltip ("Slow attack: transient passes through (more punch)");
    fastBtn.setTooltip ("Fast attack: transient gets caught (smoother, denser)");

    setSize (760, 400);
    setResizable (true, true);
    setResizeLimits (620, 340, 1400, 740);
    getConstrainer()->setFixedAspectRatio (760.0 / 400.0);
    startTimerHz (30);
}

OneMicDrumsEditor::~OneMicDrumsEditor()
{
    setLookAndFeel (nullptr);
}

void OneMicDrumsEditor::timerCallback()
{
    const float gr = proc.gainReductionDb.load();
    const float cr = proc.crushReductionDb.load();
    grDisplay = gr > grDisplay ? gr : grDisplay * 0.85f + gr * 0.15f;
    crushDisplay = cr > crushDisplay ? cr : crushDisplay * 0.85f + cr * 0.15f;
    repaint();
}

void OneMicDrumsEditor::paint (juce::Graphics& g)
{
    const float s = (float) getWidth() / 760.0f;
    g.fillAll (colours::bg);

    // Kopfzeile
    auto top = getLocalBounds().removeFromTop (juce::roundToInt (48 * s)).toFloat();
    g.setColour (colours::text);
    g.setFont (juce::FontOptions (22.0f * s, juce::Font::bold));
    g.drawText ("ONE MIC DRUMS", top.reduced (18 * s, 0), juce::Justification::centredLeft);
    g.setColour (colours::dim);
    g.setFont (juce::FontOptions (12.0f * s));
    g.drawText ("MONO IN  >  STEREO OUT", top.reduced (18 * s, 0), juce::Justification::centredRight);

    // Felder
    const char* panelLabels[5] = { "SPLIT @ 160 HZ", "", "", "", "" };
    for (int i = 0; i < 5; ++i)
    {
        auto f = panels[i].toFloat();
        g.setColour (colours::panel);
        g.fillRoundedRectangle (f, 12 * s);
        g.setColour (colours::edge);
        g.drawRoundedRectangle (f, 12 * s, 1.0f);
        if (*panelLabels[i])
        {
            g.setColour (colours::dim);
            g.setFont (juce::FontOptions (10.5f * s, juce::Font::bold));
            g.drawText (panelLabels[i], f.removeFromBottom (22 * s), juce::Justification::centred);
        }
    }

    // Crush: Limiter-Anzeige
    {
        auto b = panels[3].toFloat().reduced (22 * s, 0);
        auto bar = juce::Rectangle<float> (b.getX(), panels[3].getBottom() - 34 * s, b.getWidth(), 4 * s);
        g.setColour (colours::edge);
        g.fillRoundedRectangle (bar, 2 * s);
        g.setColour (colours::crush);
        g.fillRoundedRectangle (bar.withWidth (bar.getWidth() * juce::jlimit (0.0f, 1.0f, crushDisplay / 20.0f)), 2 * s);
        g.setColour (colours::dim);
        g.setFont (juce::FontOptions (10.0f * s));
        g.drawText ("LIMIT  -" + juce::String (crushDisplay, 1) + " dB", bar.translated (0, 7 * s).withHeight (14 * s),
                    juce::Justification::centred);
    }

    // Kompressor-GR unter den Attack-Knöpfen
    {
        auto b = slowBtn.getBounds().getUnion (fastBtn.getBounds()).toFloat();
        auto bar = juce::Rectangle<float> (b.getX(), b.getY() - 8 * s, b.getWidth(), 4 * s);
        g.setColour (colours::edge);
        g.fillRoundedRectangle (bar, 2 * s);
        g.setColour (colours::comp);
        g.fillRoundedRectangle (bar.withWidth (bar.getWidth() * juce::jlimit (0.0f, 1.0f, grDisplay / 20.0f)), 2 * s);
    }

    // Space: Bereiche als Beschriftung rund um den Regler
    {
        auto kb = space.slider.getBounds().translated (space.getX(), space.getY()).toFloat();
        kb = kb.withTrimmedBottom (18.0f * s);   // Textfeld
        const float d = juce::jmin (kb.getWidth(), kb.getHeight()) - 12.0f;   // wie drawRotarySlider (reduced 6)
        const auto c = kb.getCentre();
        const float a0 = juce::MathConstants<float>::pi * 1.25f, a1 = juce::MathConstants<float>::pi * 2.75f;
        const float v = proc.apvts.getRawParameterValue ("space")->load();
        const char* names[] = { "PLATE", "ROOM", "HALL", "SPACE" };
        g.setFont (juce::FontOptions (9.5f * s, juce::Font::bold));
        for (int i = 0; i < 4; ++i)
        {
            const float a = a0 + (a1 - a0) * (0.125f + 0.25f * (float) i);
            const float rr = d * 0.5f + 14.0f * s;
            const auto pt = c.getPointOnCircumference (rr, a);
            const bool active = v >= 0.005f && juce::jmin (3, (int) (v * 4.0f)) == i;
            g.setColour (active ? colours::space.brighter (0.4f) : colours::dim.withAlpha (0.8f));
            g.drawText (names[i], juce::Rectangle<float> (60 * s, 14 * s).withCentre (pt), juce::Justification::centred);
        }
        // Trennstriche an den Viertelgrenzen
        g.setColour (colours::bg);
        for (int i = 1; i < 4; ++i)
        {
            const float a = a0 + (a1 - a0) * 0.25f * (float) i;
            const float ringW = juce::jmax (3.0f, d * 0.5f * 0.09f);
            g.drawLine (juce::Line<float> (c.getPointOnCircumference (d * 0.5f - ringW * 1.8f, a),
                                           c.getPointOnCircumference (d * 0.5f - ringW * 0.2f, a)), 2.0f);
        }
    }
}

void OneMicDrumsEditor::resized()
{
    const float s = (float) getWidth() / 760.0f;
    auto S = [s] (float v) { return juce::roundToInt (v * s); };

    auto r = getLocalBounds();
    r.removeFromTop (S (52));
    r = r.reduced (S (16), 0);
    r.removeFromBottom (S (16));

    // Spalten: Split | Compress | Space | Crush | Output
    const int gap = S (12);
    panels[0] = r.removeFromLeft (S (128)); r.removeFromLeft (gap);
    panels[4] = r.removeFromRight (S (96)); r.removeFromRight (gap);
    const int w = (r.getWidth() - 2 * gap) / 3;
    panels[1] = r.removeFromLeft (w); r.removeFromLeft (gap);
    panels[2] = r.removeFromLeft (w); r.removeFromLeft (gap);
    panels[3] = r;

    for (auto* k : { &low, &high, &comp, &space, &crush, &output })
    {
        k->scale = s;
        k->insetX = 0;
        k->slider.setTextBoxStyle (juce::Slider::TextBoxBelow, false, S (110), S (18));
    }

    auto split = panels[0].reduced (S (6), S (8));
    split.removeFromBottom (S (16));
    high.setBounds (split.removeFromTop (split.getHeight() / 2));
    low.setBounds (split);

    // Große Regler: gleiche Größe in allen drei Feldern
    auto bigArea = [&] (juce::Rectangle<int> p) { auto a = p.reduced (S (8), S (10)); a.removeFromBottom (S (48)); return a; };
    auto c = bigArea (panels[1]);
    comp.setBounds (c);
    auto btnRow = panels[1].reduced (S (14), 0).withTop (panels[1].getBottom() - S (42)).withHeight (S (28));
    slowBtn.setBounds (btnRow.removeFromLeft (btnRow.getWidth() / 2).reduced (S (3), 0));
    fastBtn.setBounds (btnRow.reduced (S (3), 0));

    space.setBounds (bigArea (panels[2]));
    space.insetX = S (16);         // Platz für PLATE / SPACE links und rechts
    space.resized();
    crush.setBounds (bigArea (panels[3]));

    auto o = panels[4].reduced (S (6), 0);
    output.setBounds (o.withSizeKeepingCentre (o.getWidth(), S (130)));

    for (auto* k : { &low, &high, &comp, &space, &crush, &output })
        k->resized();
}
