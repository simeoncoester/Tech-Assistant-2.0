#pragma once

#include <juce_gui_basics/juce_gui_basics.h>
#include "PluginProcessor.h"

class OmdLookAndFeel : public juce::LookAndFeel_V4
{
public:
    OmdLookAndFeel();
    void drawRotarySlider (juce::Graphics&, int x, int y, int w, int h, float pos,
                           float startAngle, float endAngle, juce::Slider&) override;
    void drawLinearSlider (juce::Graphics&, int x, int y, int w, int h, float pos, float minPos, float maxPos,
                           juce::Slider::SliderStyle, juce::Slider&) override;
    void drawButtonBackground (juce::Graphics&, juce::Button&, const juce::Colour&,
                               bool highlighted, bool down) override;
};

// Ein Drehregler mit Titel und Wertanzeige
class OmdKnob : public juce::Component
{
public:
    OmdKnob (juce::AudioProcessorValueTreeState&, const juce::String& paramId,
             const juce::String& title, juce::Colour accent, bool big);
    void resized() override;
    void paint (juce::Graphics&) override;

    juce::Slider slider;
    juce::String title;
    juce::Colour accent;
    bool big;
    float scale = 1.0f;
    int insetX = 0;
    std::function<void (juce::Graphics&, juce::Rectangle<float> knobArea)> paintExtra;

private:
    std::unique_ptr<juce::AudioProcessorValueTreeState::SliderAttachment> attachment;
};

class OneMicDrumsEditor : public juce::AudioProcessorEditor, private juce::Timer
{
public:
    explicit OneMicDrumsEditor (OneMicDrumsProcessor&);
    ~OneMicDrumsEditor() override;

    void paint (juce::Graphics&) override;
    void resized() override;

private:
    void timerCallback() override;

    OneMicDrumsProcessor& proc;
    OmdLookAndFeel lnf;

    OmdKnob low, high, comp, space, crush, output;
    juce::TextButton slowBtn { "SLOW" }, fastBtn { "FAST" };
    juce::Slider spaceMix;   // Menge des Halls im Mix (Fader unter dem Space-Poti)
    std::unique_ptr<juce::AudioProcessorValueTreeState::SliderAttachment> spaceMixAttachment;
    juce::ParameterAttachment attackAttachment;

    float grDisplay = 0.0f, crushDisplay = 0.0f;
    juce::Rectangle<int> panels[5];   // Split, Compress, Space, Crush, Output

    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR (OneMicDrumsEditor)
};
