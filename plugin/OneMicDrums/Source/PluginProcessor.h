#pragma once

#include <juce_audio_processors/juce_audio_processors.h>
#include <juce_dsp/juce_dsp.h>

//==============================================================================
// One Mic Drums
//
// Signalweg (ein Mikrofon rein, Stereo raus):
//
//   Mono-Eingang ─┬─ Low  (Linkwitz-Riley 24 dB/Okt. unter 160 Hz) ─ Gain ─┐
//                 └─ High (über 160 Hz) ─────────────────────────── Gain ─┤
//                                                                          ▼
//                                   Kompressor (ein Regler + Slow/Fast) ──┤
//                                                                          ▼
//                       Stereo-Bild: Bässe mittig, Höhen breit (monokompatibel)
//                                                                          ▼
//                   + Hall als Parallel-Bus (Plate → Room → Hall → Space)
//                                                                          ▼
//                                       Crush: Drive + Limiter (4× Oversampling)
//                                                                          ▼
//                                                                Stereo-Ausgang
//==============================================================================

namespace omd
{
    // Feed-forward-Kompressor mit Soft-Knee. Ein Regler steuert Threshold, Ratio
    // und automatische Aufholverstärkung gleichzeitig.
    class OneKnobCompressor
    {
    public:
        void prepare (double sampleRate);
        void reset();
        void setAmount (float amount01, bool fastAttack);
        // Liefert den Gain-Faktor (inkl. Aufholverstärkung) für dieses Sample.
        float computeGain (float detectorInput);
        float getGainReductionDb() const noexcept { return lastGrDb; }

    private:
        double sr = 44100.0;
        float thresholdDb = 0.0f, ratio = 1.0f, kneeDb = 6.0f;
        float attackCoef = 0.0f, releaseCoef = 0.0f;
        float envDb = 0.0f;           // geglättete Pegelreduktion (positiv = weniger Pegel)
        float lastGrDb = 0.0f;
        juce::SmoothedValue<float> makeup { 1.0f };
        float computeGainDb (float levelDb) const noexcept;
    };

    // Raum-Regler: morpht zwischen vier Hall-Charakteren und mischt parallel zu.
    class SpaceReverb
    {
    public:
        void prepare (double sampleRate, int maxBlock);
        void reset();
        void setAmount (float amount01);
        // Nimmt das Mono-Send-Signal und addiert den Stereo-Hall auf L/R.
        void processAdd (const float* send, float* left, float* right, int numSamples);

        static juce::String typeNameFor (float amount01);

    private:
        struct Character { float size, damping, preDelayMs, wet, lowCutHz, highCutHz; };
        static Character characterFor (float amount01);

        double sr = 44100.0;
        juce::Reverb reverb;
        juce::Reverb::Parameters params;
        juce::dsp::IIR::Filter<float> sendHp, sendLp;
        std::vector<float> preDelay;
        int writePos = 0;
        juce::SmoothedValue<float> preDelaySamples { 0.0f }, wet { 0.0f };
        std::vector<float> bufL, bufR;
        float lastAmount = -1.0f;
        float lowCut = 0.0f, highCut = 0.0f;
    };

    // Erzeugt aus Mono ein breites Stereo-Signal. Bässe bleiben in der Mitte,
    // die Höhen bekommen ein dekorreliertes Seitensignal (M/S), das sich in Mono
    // vollständig auslöscht – also keine Kammfilter beim Summieren.
    class MonoToStereo
    {
    public:
        void prepare (double sampleRate);
        void reset();
        void process (const float* low, const float* high, float* left, float* right, int numSamples);

    private:
        double sr = 44100.0;
        std::vector<float> delay;
        int writePos = 0, d1 = 0, d2 = 0;
        juce::dsp::IIR::Filter<float> sideHp;
        float width = 0.42f;
    };
}

//==============================================================================
class OneMicDrumsProcessor : public juce::AudioProcessor
{
public:
    OneMicDrumsProcessor();
    ~OneMicDrumsProcessor() override = default;

    void prepareToPlay (double sampleRate, int samplesPerBlock) override;
    void releaseResources() override {}
    bool isBusesLayoutSupported (const BusesLayout& layouts) const override;
    void processBlock (juce::AudioBuffer<float>&, juce::MidiBuffer&) override;
    using AudioProcessor::processBlock;

    juce::AudioProcessorEditor* createEditor() override;
    bool hasEditor() const override { return true; }

    const juce::String getName() const override { return JucePlugin_Name; }
    bool acceptsMidi() const override { return false; }
    bool producesMidi() const override { return false; }
    bool isMidiEffect() const override { return false; }
    double getTailLengthSeconds() const override { return 6.0; }

    int getNumPrograms() override { return 1; }
    int getCurrentProgram() override { return 0; }
    void setCurrentProgram (int) override {}
    const juce::String getProgramName (int) override { return {}; }
    void changeProgramName (int, const juce::String&) override {}

    void getStateInformation (juce::MemoryBlock& destData) override;
    void setStateInformation (const void* data, int sizeInBytes) override;

    static juce::AudioProcessorValueTreeState::ParameterLayout createLayout();
    juce::AudioProcessorValueTreeState apvts;

    // Für die Anzeige im Editor
    std::atomic<float> gainReductionDb { 0.0f };
    std::atomic<float> crushReductionDb { 0.0f };

    static constexpr float crossoverHz = 160.0f;

private:
    juce::AudioParameterFloat* pLow = nullptr;
    juce::AudioParameterFloat* pHigh = nullptr;
    juce::AudioParameterFloat* pComp = nullptr;
    juce::AudioParameterChoice* pAttack = nullptr;
    juce::AudioParameterFloat* pSpace = nullptr;
    juce::AudioParameterFloat* pCrush = nullptr;
    juce::AudioParameterFloat* pOutput = nullptr;

    juce::dsp::LinkwitzRileyFilter<float> lowPass, highPass;
    juce::SmoothedValue<float> lowGain { 1.0f }, highGain { 1.0f }, outGain { 1.0f };
    juce::SmoothedValue<float> drive { 1.0f }, clipAmount { 0.0f };
    static float bandGain (float dB) { return dB <= -23.95f ? 0.0f : juce::Decibels::decibelsToGain (dB); }

    omd::OneKnobCompressor comp;
    omd::MonoToStereo widener;
    omd::SpaceReverb space;

    std::unique_ptr<juce::dsp::Oversampling<float>> oversampling;
    // Lookahead-Limiter (nach dem Downsampling, damit nichts mehr über die Grenze geht)
    int limLookahead = 48;
    std::vector<float> limDelayL, limDelayR, limTargets, limAvgBuf;
    std::vector<std::pair<int, float>> limMinQueue;   // Ringpuffer für gleitendes Minimum
    int limQHead = 0, limQTail = 0, limPos = 0, limIndex = 0;
    double limAvgSum = 0.0;
    float limGain = 1.0f, limRelease = 0.0f;
    void resetLimiter();
    float limiterGain (float peak);

    juce::AudioBuffer<float> mono, lowBand, highBand;

    void processCrush (juce::AudioBuffer<float>& stereo, int numSamples);

    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR (OneMicDrumsProcessor)
};
