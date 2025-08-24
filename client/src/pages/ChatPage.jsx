import { useState, useEffect, useRef, use } from "react";
import { useParams, useNavigate } from "react-router-dom";

import BackButton from "../components/BackButton";
import ChatInput from "../components/ChatInput";
import ChatBubble from "../components/ChatBubble";
import ChatButton from "../components/ChatButton";
import ChatLoader from "../components/ui/ChatLoader";
import TypingIndicator from "../components/ui/TypingIndicator";
import { getRoomDetials } from "../services/api/api_service";
import { handleError} from "../utils/handleError"

const ChatPage = () => {
  const { roomId } = useParams();
  const navigate = useNavigate();
  const messagesEndRef = useRef(null);
  
  const [loading, setLoading] = useState(false)
  const [chatLoading, setChatLoading] = useState(false)
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState([]);
  const [room, setRoom] = useState({});

  const fetchRoomDetails = async () => {
    setLoading(true)
    try {
      const { data } = await getRoomDetials(roomId);
      setRoom(data)
    } catch (error) {
      handleError(error)
      navigate(-1)
    } finally {
      setLoading(false)
    }
  }

  const handleSendMessage = () => {
    if (!message.trim()) return;
    
    const newMessage = {
      id: messages.length + 1,
      text: message,
      sender: "You",
      timestamp: new Date(),
      type: "sent"
    };
    
    setMessages([...messages, newMessage]);
    setMessage("");
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  useEffect(() => {
    fetchRoomDetails()
  }, [])

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const formatTime = (timestamp) => {
    return timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  return (
    <div className="flex h-screen overflow-hidden">
      {loading && <ChatLoader/>}
      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col">
        {/* Header */}
        <div className="border-b border-border-primary rounded-none p-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <BackButton className="!mb-0"/>
              <div>
                <h1 className="text-xl font-semibold">{room.name}</h1>
                <p className="text-text-secondary text-sm">
                  {room.participant_count} participants
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Messages Area */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {chatLoading && <div className="flex justify-center">
            <TypingIndicator />
          </div>}
          {messages.map((msg) => (
            <div key={msg.id} className="animate-chat-appear">
              {msg.type === 'system' ? (
                <div className="text-center">
                  <span className="text-text-muted text-sm bg-background-secondary px-3 py-1 rounded-full">
                    {msg.text}
                  </span>
                </div>
              ) : (
                <div className={`flex ${msg.type === 'sent' ? 'justify-end' : 'justify-start'}`}>
                  <div className={`max-w-xs lg:max-w-md ${msg.type === 'sent' ? 'order-2' : 'order-1'}`}>
                    {msg.type === 'received' && (
                      <p className="text-text-secondary text-xs mb-1 px-3">{msg.sender}</p>
                    )}
                    <ChatBubble variant={msg.type === 'sent' ? 'sent' : 'received'}>
                      <p className="break-words">{msg.text}</p>
                      <p className="text-xs opacity-70 mt-1">{formatTime(msg.timestamp)}</p>
                    </ChatBubble>
                  </div>
                </div>
              )}
            </div>
          ))}
          <div ref={messagesEndRef} />
        </div>

        {/* Message Input */}
        <div className="border-t border-border-primary rounded-none p-4">
          <div className="flex gap-3">
            <div className="flex-1">
              <ChatInput
                name={'chat-input'}
                placeholder="Type a message..."
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                onKeyPress={handleKeyPress}
                variant="received"
                className="w-full max-w-full"
              />
            </div>
            <ChatButton
              variant="send"
              onClick={handleSendMessage}
              disabled={!message.trim()}
              className="px-5 font-bold"
            >
              Send
            </ChatButton>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChatPage;