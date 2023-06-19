import React, { useState } from 'react';
import FullChatbot from './FullChatbot';
import './ChatbotButton.css'; // New CSS for the buttons

const ChatbotContainer = () => {
  const [isVisible, setIsVisible] = useState(false);
  const [model, setModel] = useState("GPT-3");

  const handleClick = () => setIsVisible(!isVisible);
  const handleModelChange = () => setModel(model === "GPT-3" ? "GPT-3" : "BERT");

  const apiUrl = model === "GPT-3"
    ? "http://localhost:5000/generate-response-gpt3"
    : "http://localhost:5000/generate-response-bert";

  return (
    <div style={{ position: 'fixed', right: '20px', bottom: '20px' }}>
      {isVisible
        ? (
          <>
            <FullChatbot title={`Model: ${model}`} apiUrl={apiUrl} closeChatbot={handleClick} />
            {/* <button onClick={handleModelChange}>Switch to {model === "BERT" ? "GPT-3" : "BERT"}</button> */}
          </>
        )
        : <img src='src/assets/bee.jpg'  width="90" alt='Open chatbot' className='chatbot-button' onClick={handleClick} />
      }
    </div>
  );
};

export default ChatbotContainer;
