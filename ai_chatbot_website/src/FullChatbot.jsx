import React, { useState, useEffect, useRef } from 'react';
import './FullChatbot.css';

const FullChatbot = () => {
  const timestamp = new Date();
  const initialTime = `${timestamp.getHours()}:${timestamp.getMinutes()}`;

  const [input, setInput] = useState('');
  const [messages, setMessages] = useState([
    {
      text: 'Merhaba, size nasıl yardımcı olabilirim?',
      time: initialTime,
      isBot: true,
    },
  ]);
  const messagesEndRef = useRef(null);

  const handleSubmit = (e) => {
    e.preventDefault();

    if (input.trim() === '') return;

    const timestamp = new Date();
    const time = `${timestamp.getHours()}:${timestamp.getMinutes()}`;

    setMessages([...messages, { text: input, time, isBot: false }]);
    setInput('');
  };

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  return (
    <div className="canvas">
      <div className="chatbot-container">
        <div className="chatbot-messages">
          {messages.map((message, i) => (
            <div key={i} className={`chatbot-message ${message.isBot ? 'bot' : 'user'}`}>
              <div className="message-text">{message.text}</div>
              <div className="message-time">{message.time}</div>
            </div>
          ))}
          <div ref={messagesEndRef} />
        </div>
        <div className="chatbot-input-container">
            <form onSubmit={handleSubmit} className="chatbot-input">
            <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Type your message here..."
            />
            <button type="submit">Send</button>
            </form>
        </div>
      </div>
    </div>
  );
};

export default FullChatbot;
