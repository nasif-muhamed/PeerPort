import ChatBubble from "../ChatBubble";

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
          <div className="bg-chat-sent rounded-2xl rounded-br-md px-4 py-3 animate-chat-appear">
            <div className="flex space-x-1">
              <div className="w-2 h-2 bg-white rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
              <div className="w-2 h-2 bg-white rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
              <div className="w-2 h-2 bg-white rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChatLoader