import React, { useState, useEffect, useRef } from 'react';
import './FullChatbot.css';
import axios from 'axios';

const FullChatbot = ({ title, apiUrl }) => {
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
  const [status, setStatus] = useState("Offline");
  const messagesEndRef = useRef(null);

  useEffect(() => {
    const fetchStatus = async () => {
      try {
        const response = await axios.get('/api/status');
        setStatus(response.data.status);
      } catch (error) {
        setStatus("Offline");
      }
    };
    fetchStatus();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (input.trim() === '') return;

    const timestamp = new Date();
    const time = `${timestamp.getHours()}:${timestamp.getMinutes()}`;

    setMessages([...messages, { text: input, time, isBot: false }]);
    setInput(''); // Clear the input

    try {
      const response = await axios.post(apiUrl, {
        message: input,
      });

      const botMessage = response.data.text;
      const botTimestamp = new Date();
      const botTime = `${botTimestamp.getHours()}:${botTimestamp.getMinutes()}`;

      setMessages((prevMessages) => [
        ...prevMessages,
        { text: botMessage, time: botTime, isBot: true },
      ]);
    } catch (error) {
      console.error('Error while getting response from the backend server:', error);
    }
  };

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  return (
    <div className="canvas" style={{ margin: '0 1rem' }}>
      <div className="title-container">
        <h3>{title}</h3>
        <span className={`status-text ${status.toLowerCase()}`}>{`Status: ${status}`}</span>
      </div>
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
  );
};

export default FullChatbot;