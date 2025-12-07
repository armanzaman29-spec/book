import React, { useState, useEffect, useCallback } from 'react';
import './ChatWidget.css';

// Create a mock API service to prevent errors when backend is not available
const mockApiService = {
  query: async (question) => {
    // Simulate a delay to mimic API call
    await new Promise(resolve => setTimeout(resolve, 500));

    // Return a mock response
    return {
      answer: "I'm your AI assistant. The backend service is not currently available, so I'm providing a mock response. To get real responses, please ensure the backend service is running on port 8000.",
      sources: []
    };
  }
};

// Try to import the real API service, fallback to mock if it fails
let apiService;
try {
  apiService = require('@site/src/services/api').default;
} catch (error) {
  console.warn('API service not available, using mock service:', error);
  apiService = mockApiService;
}

const ChatWidget = () => {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isWidgetOpen, setIsWidgetOpen] = useState(false);
  const [apiError, setApiError] = useState(false);

  // Initialize with a welcome message
  useEffect(() => {
    setMessages([
      {
        id: 1,
        text: "Hello! I'm your AI assistant for the Physical AI & Humanoid Robotics textbook. How can I help you today?",
        sender: 'bot',
        timestamp: new Date()
      }
    ]);
  }, []);

  const handleSend = useCallback(async () => {
    if (!inputValue.trim() || isLoading) return;

    // Add user message
    const userMessage = {
      id: Date.now(),
      text: inputValue,
      sender: 'user',
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      // Call the backend API to get the response
      const response = await apiService.query(inputValue);

      const botMessage = {
        id: Date.now() + 1,
        text: response.answer || "I couldn't generate a response. Please try again.",
        sender: 'bot',
        timestamp: new Date()
      };

      setMessages(prev => [...prev, botMessage]);
      setApiError(false); // Clear any previous API errors
    } catch (error) {
      console.error('ChatWidget API Error:', error);
      setApiError(true);

      const errorMessage = {
        id: Date.now() + 1,
        text: "The backend service is not available. I'm running in offline mode with limited functionality.",
        sender: 'bot',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  }, [inputValue, isLoading]);

  const handleKeyPress = useCallback((e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  }, [handleSend]);

  // Don't render anything if there are critical errors that could break the page
  if (typeof window !== 'undefined' && window?.document) {
    return (
      <div className="chat-widget">
        {isWidgetOpen ? (
          <div className="chat-container">
            <div className="chat-header">
              <h3>Textbook AI Assistant</h3>
              <button
                className="chat-close-btn"
                onClick={() => setIsWidgetOpen(false)}
              >
                ×
              </button>
            </div>

            <div className="chat-messages">
              {messages.map((message) => (
                <div
                  key={message.id}
                  className={`message ${message.sender}-message`}
                >
                  <div className="message-text">{message.text}</div>
                  <div className="message-timestamp">
                    {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                  </div>
                </div>
              ))}

              {isLoading && (
                <div className="message bot-message">
                  <div className="message-text">
                    <div className="typing-indicator">
                      <span></span>
                      <span></span>
                      <span></span>
                    </div>
                  </div>
                </div>
              )}
            </div>

            <div className="chat-input-area">
              <textarea
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder={apiError
                  ? "Backend unavailable - type anything to see mock response"
                  : "Ask a question about the textbook content..."}
                rows="2"
                disabled={isLoading}
              />
              <button
                onClick={handleSend}
                disabled={!inputValue.trim() || isLoading}
                className="send-button"
              >
                Send
              </button>
            </div>
          </div>
        ) : (
          <button
            className="chat-toggle-btn"
            onClick={() => setIsWidgetOpen(true)}
          >
            💬 AI Assistant
          </button>
        )}
      </div>
    );
  }

  // Fallback render for SSR or if there are issues
  return null;
};

export default ChatWidget;