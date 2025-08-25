import { useState } from 'react'
import ChatInput from "../ChatInput";
import ChatButton from "../ChatButton";
import { useWebSocket } from "../../context/ChatNotificationSocketContext"
import { handleError } from '../../utils/handleError';
import { useAuthTokens } from "../../hooks/useAuthTokens"

const MessageInput = ({ roomId, setMessages }) => {
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const { wsSend } = useWebSocket();
  const { userId, username } = useAuthTokens()
  
  const createTempMsg = () => {
    return {
      id: new Date(),
      content: message,
      sender: userId,
      room: roomId,
      timestamp: new Date().toString(),
      msg_type: "sent",
      sender_username: username,
      type: 'text',
      temporary: true,
    };
  }

  const handleSendMessage = async () => {
    const tempMsg = createTempMsg()
    try {
      setLoading(true);
      wsSend({
        type: 'send_chat',
        room_id: roomId,
        payload: {
          message: message,
        }
      });
      setMessage('');
      setMessages(prev => [...prev, tempMsg])
    } catch (error) {
      handleError(error, 'Error sending message');
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  return (
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
          disabled={!message.trim() || loading}
          className="px-5 font-bold"
        >
          Send
        </ChatButton>
      </div>
    </div>
  )
}

export default MessageInput