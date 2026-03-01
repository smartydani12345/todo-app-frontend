import React, { useState, useEffect } from 'react';

interface VoiceInputProps {
  onTranscriptChange: (transcript: string) => void;
  language?: string;
}

const VoiceInput: React.FC<VoiceInputProps> = ({ onTranscriptChange, language = 'en-US' }) => {
  const [isListening, setIsListening] = useState(false);
  const [transcript, setTranscript] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [recognition, setRecognition] = useState<any>(null);

  useEffect(() => {
    // Check if the browser supports the Web Speech API
    const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;

    if (!SpeechRecognition) {
      setError('Your browser does not support speech recognition. Please use Chrome, Edge, or Safari.');
      return;
    }

    const recognitionInstance = new SpeechRecognition();
    recognitionInstance.continuous = false;
    recognitionInstance.interimResults = true;
    recognitionInstance.lang = language;

    recognitionInstance.onresult = (event: any) => {
      const transcript = Array.from(event.results)
        .map((result: any) => result[0])
        .map(result => result.transcript)
        .join('');

      setTranscript(transcript);
      onTranscriptChange(transcript);
    };

    recognitionInstance.onerror = (event: any) => {
      setError(`Speech recognition error: ${event.error}`);
      setIsListening(false);
    };

    recognitionInstance.onend = () => {
      if (isListening) {
        // Restart recognition if it was interrupted
        startListening();
      }
    };

    setRecognition(recognitionInstance);

    // Cleanup function
    return () => {
      recognitionInstance.stop();
    };
  }, [language, onTranscriptChange]);

  const startListening = () => {
    if (recognition) {
      try {
        recognition.start();
        setIsListening(true);
        setError(null);
      } catch (err) {
        setError('Permission denied. Please allow microphone access.');
        setIsListening(false);
      }
    }
  };

  const stopListening = () => {
    if (recognition) {
      recognition.stop();
      setIsListening(false);
    }
  };

  const toggleListening = () => {
    if (isListening) {
      stopListening();
    } else {
      startListening();
    }
  };

  const handleMicrophoneClick = () => {
    if (!isListening) {
      navigator.mediaDevices.getUserMedia({ audio: true })
        .then(() => {
          toggleListening();
        })
        .catch(err => {
          setError(`Microphone access denied: ${err.message}`);
        });
    } else {
      toggleListening();
    }
  };

  return (
    <div className="voice-input-container">
      <button
        onClick={handleMicrophoneClick}
        className={`mic-button ${isListening ? 'listening' : ''}`}
        aria-label={isListening ? "Stop listening" : "Start listening"}
        title={isListening ? "Stop listening" : "Start listening"}
      >
        <svg 
          xmlns="http://www.w3.org/2000/svg" 
          className={`h-6 w-6 ${isListening ? 'text-red-500' : 'text-gray-600'}`} 
          fill="none" 
          viewBox="0 0 24 24" 
          stroke="currentColor"
        >
          {isListening ? (
            <path 
              strokeLinecap="round" 
              strokeLinejoin="round" 
              strokeWidth={2} 
              d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" 
            />
          ) : (
            <path 
              strokeLinecap="round" 
              strokeLinejoin="round" 
              strokeWidth={2} 
              d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" 
            />
          )}
        </svg>
      </button>

      {error && (
        <div className="error-message text-red-500 text-sm mt-2">
          {error}
        </div>
      )}

      {transcript && (
        <div className="transcript-preview text-sm mt-2 p-2 bg-gray-100 rounded">
          <strong>Transcript:</strong> {transcript}
        </div>
      )}
    </div>
  );
};

export default VoiceInput;