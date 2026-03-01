# Phase 3 Voice Chat Skill

## Overview
This skill provides voice interaction capabilities for ChatAgent, including speech recognition (voice-to-text) and speech synthesis (text-to-speech) with male/female voice options.

## Features

### Speech Recognition
- Real-time voice input using Web Speech API
- Multi-language support
- Auto-detection of spoken language
- Continuous listening mode option

### Speech Synthesis
- Text-to-speech output
- Male and female voice selection
- Adjustable rate and pitch
- Auto-speak responses option

## Architecture

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   User Voice    │────▶│  Speech          │────▶│   Transcript    │
│   Input         │     │  Recognition     │     │   Text          │
└─────────────────┘     └──────────────────┘     └─────────────────┘
                                                        │
                                                        ▼
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   Audio Output  │◀────│  Speech          │◀────│   AI Response   │
│   (Speaker)     │     │  Synthesis       │     │   Text          │
└─────────────────┘     └──────────────────┘     └─────────────────┘
```

## Implementation

### Frontend Service (chatService.ts)

#### Speech Recognition
```typescript
export const startSpeechRecognition = (
  onResult: (transcript: string) => void,
  onError: (error: string) => void,
  onEnd: () => void,
  lang: string = 'en-US'
): (() => void) => {
  const SpeechRecognition = (window as any).SpeechRecognition || 
                            (window as any).webkitSpeechRecognition;
  
  const recognition = new SpeechRecognition();
  recognition.continuous = false;
  recognition.interimResults = false;
  recognition.lang = lang;

  recognition.onresult = (event: any) => {
    const transcript = event.results[0][0].transcript;
    onResult(transcript);
  };

  recognition.start();
  return () => recognition.stop();
};
```

#### Speech Synthesis
```typescript
export const speakText = (
  text: string,
  settings: VoiceSettings = { 
    voiceType: 'female', 
    rate: 1.0, 
    pitch: 1.0, 
    lang: 'en-US' 
  }
): void => {
  const utterance = new SpeechSynthesisUtterance(text);
  utterance.rate = settings.rate;
  utterance.pitch = settings.pitch;
  utterance.lang = settings.lang;
  
  const voices = window.speechSynthesis.getVoices();
  const preferredVoice = findVoice(voices, settings.voiceType, settings.lang);
  
  if (preferredVoice) {
    utterance.voice = preferredVoice;
  }
  
  window.speechSynthesis.speak(utterance);
};
```

### Voice Settings Interface

```typescript
interface VoiceSettings {
  voiceType: 'male' | 'female';
  rate: number;      // 0.1 to 10 (default: 1.0)
  pitch: number;     // 0 to 2 (default: 1.0)
  autoSpeak: boolean;
  lang: string;
}
```

## Voice Selection

### Male Voice Indicators
```
- David (Microsoft)
- Mark
- James
- Names containing: 'male', 'man', 'boy'
```

### Female Voice Indicators
```
- Zira (Microsoft)
- Samantha (Apple)
- Google US English
- Names containing: 'female', 'woman', 'girl'
```

### Voice Finding Algorithm
```typescript
export const findVoice = (
  voices: SpeechSynthesisVoice[],
  voiceType: 'male' | 'female',
  lang: string
): SpeechSynthesisVoice | undefined => {
  const langVoices = voices.filter(v => v.lang.startsWith(lang.split('-')[0]));
  
  for (const voice of langVoices) {
    const name = voice.name.toLowerCase();
    
    if (voiceType === 'female') {
      if (name.includes('female') || name.includes('zira') || 
          name.includes('samantha')) {
        return voice;
      }
    } else {
      if (name.includes('male') || name.includes('david') || 
          name.includes('mark')) {
        return voice;
      }
    }
  }
  
  return langVoices[0];
};
```

## Language Codes

| Language | Code | Speech Recognition |
|----------|------|-------------------|
| English | en | en-US |
| Urdu | ur | ur-PK |
| Roman Urdu | roman_ur | ur-PK |
| Roman English | roman_en | en-US |

## UI Components

### Voice Input Button
```tsx
<button
  onClick={startListening}
  className={`p-2.5 rounded-xl ${
    isListening
      ? 'bg-red-600 text-white animate-pulse'
      : 'bg-gray-700 text-gray-300'
  }`}
>
  <FiMic size={18} />
</button>
```

### Voice Settings Panel
```tsx
<div className="voice-settings">
  <div>
    <span>Voice Type</span>
    <button onClick={() => setVoiceType('male')}>Male</button>
    <button onClick={() => setVoiceType('female')}>Female</button>
  </div>
  <div>
    <span>Auto Speak</span>
    <Toggle checked={autoSpeak} onChange={setAutoSpeak} />
  </div>
</div>
```

## Usage Examples

### Start Voice Input
```typescript
// Start listening
const stopListening = startSpeechRecognition(
  (transcript) => {
    console.log('User said:', transcript);
    sendMessage(transcript);
  },
  (error) => console.error('Error:', error),
  () => console.log('Listening ended')
);

// Stop listening
stopListening();
```

### Speak Response
```typescript
// Speak with default settings
speakText('Hello, how can I help you?');

// Speak with custom settings
speakText('Hello', {
  voiceType: 'female',
  rate: 0.9,
  pitch: 1.1,
  lang: 'en-US'
});
```

## Browser Support

| Browser | Speech Recognition | Speech Synthesis |
|---------|-------------------|------------------|
| Chrome | ✅ Full | ✅ Full |
| Edge | ✅ Full | ✅ Full |
| Safari | ⚠️ Limited | ✅ Full |
| Firefox | ❌ No | ⚠️ Limited |

## Error Handling

### Common Errors
```typescript
// Recognition not supported
if (!SpeechRecognition) {
  onError('Speech recognition not supported in this browser');
  return;
}

// Already started error
try {
  recognition.start();
} catch (e) {
  if (e.name === 'InvalidStateError') {
    // Already running, stop it first
    recognition.stop();
  }
}
```

## Best Practices

1. **Always check browser support before using voice features**
2. **Provide visual feedback during listening state**
3. **Handle errors gracefully with user-friendly messages**
4. **Allow users to disable voice features**
5. **Respect user privacy - don't record without consent**

## Testing Checklist

- [ ] Voice input works in Chrome
- [ ] Voice input works in Edge
- [ ] Male voice selection works
- [ ] Female voice selection works
- [ ] Auto-speak toggle works
- [ ] Language switching works
- [ ] Error handling displays correctly
- [ ] Visual feedback shows listening state

## Performance Optimization

1. **Cache voices list** - Get voices once and cache
2. **Debounce recognition restart** - Prevent rapid start/stop
3. **Cancel ongoing speech** - Before starting new speech
4. **Use appropriate timeout** - For recognition timeout

## Future Enhancements

1. Custom voice training
2. Voice command shortcuts
3. Offline speech recognition
4. Multi-speaker detection
5. Emotion detection from voice
