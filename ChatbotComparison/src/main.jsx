import React from 'react';
import ReactDOM from 'react-dom/client';
import ChatbotContainer from './ChatbotContainer';
import Wrapper from './Wrapper'; // Add this line
import './index.css';

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <Wrapper>
      <ChatbotContainer />
    </Wrapper>
  </React.StrictMode>,
);
