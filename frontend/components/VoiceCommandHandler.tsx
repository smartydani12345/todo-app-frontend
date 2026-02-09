import { useState, useEffect, useRef } from 'react';

interface VoiceCommandHandlerProps {
  onAddTask: (title: string) => void;
  onUpdateTask: (taskId: string, updates: any) => void;
  onDeleteTask: (taskId: string) => void;
}

export const VoiceCommandHandler: React.FC<VoiceCommandHandlerProps> = ({
  onAddTask,
  onUpdateTask,
  onDeleteTask
}) => {
  const [isListening, setIsListening] = useState(false);
  const [transcript, setTranscript] = useState('');
  const [isSupported, setIsSupported] = useState(true);
  const recognitionRef = useRef<any>(null);

  useEffect(() => {
    // Check if the browser supports the Web Speech API
    const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;

    if (SpeechRecognition) {
      const recognition = new SpeechRecognition();
      recognition.continuous = false;
      recognition.interimResults = false;
      recognition.lang = 'en-US';

      recognition.onresult = (event: any) => {
        const speechResult = event.results[0][0].transcript.toLowerCase();
        setTranscript(speechResult);
        processVoiceCommand(speechResult);
      };

      recognition.onerror = (event: any) => {
        console.error('Speech recognition error', event.error);
        setIsListening(false);
      };

      recognition.onend = () => {
        setIsListening(false);
      };

      recognitionRef.current = recognition;
    } else {
      setIsSupported(false);
    }

    // Cleanup
    return () => {
      if (recognitionRef.current) {
        recognitionRef.current.stop();
      }
    };
  }, []);

  const processVoiceCommand = (command: string) => {
    // Add task command: "add task buy groceries" or "create task buy groceries"
    const addTaskMatch = command.match(/(?:add|create)\s+(?:a\s+)?task\s+(.+)/);
    if (addTaskMatch) {
      onAddTask(addTaskMatch[1].trim());
      return;
    }

    // Update task command: "update task 1 to completed" or "mark task 1 as completed"
    const updateTaskMatch = command.match(/(?:update|mark)\s+task\s+(\d+)\s+(?:to|as)\s+(.+)/);
    if (updateTaskMatch) {
      const taskId = updateTaskMatch[1];
      const updateText = updateTaskMatch[2];
      onUpdateTask(taskId, { completed: updateText.includes('completed') });
      return;
    }

    // Delete task command: "delete task 1" or "remove task 1"
    const deleteTaskMatch = command.match(/(?:delete|remove)\s+task\s+(\d+)/);
    if (deleteTaskMatch) {
      onDeleteTask(deleteTaskMatch[1]);
      return;
    }

    // Other potential commands could be added here
  };

  const startListening = () => {
    if (recognitionRef.current && !isListening) {
      setTranscript('');
      recognitionRef.current.start();
      setIsListening(true);
    }
  };

  const stopListening = () => {
    if (recognitionRef.current && isListening) {
      recognitionRef.current.stop();
      setIsListening(false);
    }
  };

  if (!isSupported) {
    return (
      <div className="text-sm text-gray-500 dark:text-gray-400 p-2">
        Voice commands are not supported in this browser.
      </div>
    );
  }

  return (
    <div className="p-2">
      <button
        onClick={isListening ? stopListening : startListening}
        className={`px-4 py-2 rounded-md text-white ${
          isListening ? 'bg-red-500 hover:bg-red-600' : 'bg-blue-500 hover:bg-blue-600'
        }`}
      >
        {isListening ? 'Stop Listening' : 'Start Voice Command'}
      </button>
      {isListening && (
        <div className="mt-2 text-sm text-gray-600 dark:text-gray-300">
          Listening... Say "add task [task name]" or "delete task [number]"
        </div>
      )}
      {transcript && (
        <div className="mt-2 text-sm text-gray-700 dark:text-gray-200">
          Recognized: "{transcript}"
        </div>
      )}
    </div>
  );
};