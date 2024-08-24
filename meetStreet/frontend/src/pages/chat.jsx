import { useState, useEffect } from 'react';
import io from 'socket.io-client';

const socket = io('http://localhost:5000', {
  query: { user_id: 'your_user_id' } // Replace 'your_user_id' with the actual user ID
});

const Chat = ({ recipientId, userId }) => {
  const [message, setMessage] = useState('');
  const [messages, setMessages] = useState([]);

  useEffect(() => {
    socket.on('private_message', (data) => {
      setMessages((prevMessages) => [...prevMessages, data]);
    });

    return () => {
      socket.off('private_message');
    };
  }, []);

  const sendMessage = () => {
    if (message !== '') {
      socket.emit('private_message', {
        sender_id: userId,
        recipient_id: recipientId,
        message
      });
      setMessages((prevMessages) => [...prevMessages, { sender_id: userId, message }]);
      setMessage('');
    }
  };

  return (
    <div className="chat-container max-w-md mx-auto mt-4 bg-gray-100 rounded-lg shadow-lg">
      <div className="chat-header flex items-center justify-between p-4 bg-purple-600 text-white rounded-t-lg">
        <div className="flex items-center">
          <img
            src="https://via.placeholder.com/50" // Replace with the recipient's profile picture
            alt="Recipient"
            className="w-10 h-10 rounded-full mr-3"
          />
          <div>
            <h2 className="font-semibold">Wade Warren</h2>
            <span className="text-sm text-green-300">Online</span>
          </div>
        </div>
        <button className="text-2xl">⋮</button>
      </div>
      
      <div className="chat-messages p-4 bg-white max-h-96 overflow-y-scroll">
        {messages.map((msg, index) => (
          <div
            key={index}
            className={`message my-2 p-2 rounded-lg max-w-xs ${
              msg.sender_id === userId ? 'bg-purple-600 text-white self-end' : 'bg-gray-300 text-black self-start'
            }`}
          >
            {msg.message}
          </div>
        ))}
      </div>
      
      <div className="chat-input flex items-center p-4 bg-gray-200 rounded-b-lg">
        <input
          type="text"
          className="flex-grow p-2 rounded-l-lg border border-r-0 border-gray-300 focus:outline-none"
          placeholder="Type your message..."
          value={message}
          onChange={(e) => setMessage(e.target.value)}
        />
        <button
          className="p-2 bg-purple-600 text-white rounded-r-lg"
          onClick={sendMessage}
        >
          Send
        </button>
      </div>
    </div>
  );
};

export default Chat;
