import React, { useState, useEffect, useRef } from 'react';
import './FullChatbot.css';
import axios from 'axios';

const FullChatbot = ({ title, apiUrl, closeChatbot }) => {
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
        <h2>BeeBot</h2>
        <h5>{title}</h5>
        <img src='src/assets/cross.svg' width="35" alt='Close chatbot' className='close-button' onClick={closeChatbot} />
      </div>
      <div className="messages-container">
        {messages.map((message, index) => (
          <div
            key={index}
            className={`message-container ${message.isBot ? 'bot-message' : 'user-message'}`}
          >
            <p className="message-text">{message.text}</p>
            <span className="message-time">{message.time}</span>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>
      <form className="input-container" onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Mesajınızı yazınız..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
        />
        <button type="submit">Gönder</button>
      </form>
    </div>
  );
};

export default FullChatbot;
