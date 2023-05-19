import React from 'react';
import FullChatbot from './FullChatbot';

const ChatbotContainer = () => {
  return (
    <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>
      <FullChatbot title="Model: BERT" apiUrl="http://localhost:5000/generate-response-bert" />
      <FullChatbot title="Model: GPT-3" apiUrl="http://localhost:5000/generate-response-gpt3" />
      {/* <FullChatbot title="Model: GPT-4" apiUrl="/generate-response-gpt4" /> */}
    </div>
  );
};

export default ChatbotContainer;
