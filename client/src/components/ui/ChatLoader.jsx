import ChatBubble from "../ChatBubble";
import TypingIndicator from "./TypingIndicator";

const ChatLoader = ({ message = "Processing your request..." }) => {  
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center">
      <div className="absolute inset-0 bg-black/60" />
      
      <div className="relative bg-bg-primary/30 backdrop-blur-sm rounded-2xl border border-border-primary shadow-card p-6 max-w-sm mx-4">
        <div className="flex justify-start mb-4">
          <ChatBubble variant="received">
            {message}
          </ChatBubble>
        </div>
        
        <div className="flex justify-end">
          <TypingIndicator/>
        </div>
      </div>
    </div>
  );
};

export default ChatLoader