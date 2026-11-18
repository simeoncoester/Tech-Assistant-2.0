cmake_minimum_required(VERSION 3.22)
project(OneMicDrums VERSION 0.1.0)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
if(APPLE)
    set(CMAKE_OSX_DEPLOYMENT_TARGET "10.13" CACHE STRING "")
    # Universal Binary (Apple Silicon + Intel), falls nicht anders gewünscht
    if(NOT CMAKE_OSX_ARCHITECTURES)
        set(CMAKE_OSX_ARCHITECTURES "arm64;x86_64" CACHE STRING "" FORCE)
    endif()
endif()

include(FetchContent)
FetchContent_Declare(JUCE
    GIT_REPOSITORY https://github.com/juce-framework/JUCE.git
    GIT_TAG 8.0.4
    GIT_SHALLOW ON)
FetchContent_MakeAvailable(JUCE)

# Plugin-Formate je Plattform
set(OMD_FORMATS VST3)
if(APPLE)
    list(APPEND OMD_FORMATS AU Standalone)
elseif(WIN32)
    list(APPEND OMD_FORMATS Standalone)
endif()

# Pro Tools (AAX): braucht das AAX SDK von Avid (developer.avid.com).
#   cmake -DAAX_SDK_PATH=/pfad/zum/aax-sdk ...
if(AAX_SDK_PATH AND (APPLE OR WIN32))
    juce_set_aax_sdk_path(${AAX_SDK_PATH})
    list(APPEND OMD_FORMATS AAX)
endif()

juce_add_plugin(OneMicDrums
    COMPANY_NAME "Tech Assistent"
    BUNDLE_ID com.techassistent.onemicdrums
    PLUGIN_MANUFACTURER_CODE TchA
    PLUGIN_CODE OMDr
    PRODUCT_NAME "One Mic Drums"
    FORMATS ${OMD_FORMATS}
    IS_SYNTH FALSE
    NEEDS_MIDI_INPUT FALSE
    NEEDS_MIDI_OUTPUT FALSE
    IS_MIDI_EFFECT FALSE
    EDITOR_WANTS_KEYBOARD_FOCUS FALSE
    COPY_PLUGIN_AFTER_BUILD FALSE
    VST3_CATEGORIES Fx Dynamics Reverb
    AU_MAIN_TYPE kAudioUnitType_Effect
    AAX_CATEGORY AAX_ePlugInCategory_Dynamics)

target_sources(OneMicDrums PRIVATE
    Source/PluginProcessor.cpp
    Source/PluginEditor.cpp)

target_compile_definitions(OneMicDrums PUBLIC
    JUCE_WEB_BROWSER=0
    JUCE_USE_CURL=0
    JUCE_VST3_CAN_REPLACE_VST2=0
    JUCE_DISPLAY_SPLASH_SCREEN=0)

target_link_libraries(OneMicDrums
    PRIVATE
        juce::juce_audio_utils
        juce::juce_dsp
    PUBLIC
        juce::juce_recommended_config_flags
        juce::juce_recommended_lto_flags
        juce::juce_recommended_warning_flags)

# Offline-Test (nicht Teil des Plugins): cmake -DOMD_BUILD_TESTS=ON
option(OMD_BUILD_TESTS "Offline-Messprogramm bauen" OFF)
if(OMD_BUILD_TESTS)
    juce_add_console_app(OneMicDrumsTest PRODUCT_NAME "OneMicDrumsTest")
    target_sources(OneMicDrumsTest PRIVATE Tests/OfflineTest.cpp Source/PluginProcessor.cpp Source/PluginEditor.cpp)
    target_compile_definitions(OneMicDrumsTest PRIVATE JUCE_WEB_BROWSER=0 JUCE_USE_CURL=0
        JucePlugin_Name="One\ Mic\ Drums")
    target_link_libraries(OneMicDrumsTest PRIVATE juce::juce_audio_utils juce::juce_dsp
        juce::juce_recommended_config_flags)
endif()
