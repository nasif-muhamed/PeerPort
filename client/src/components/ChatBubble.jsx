const ChatBubble = ({ 
  children, 
  variant = "sent", 
  className = "" 
}) => {
  const variants = {
    sent: "chat-bubble-sent",
    received: "chat-bubble-received"
  };

  return (
    <div className={`${variants[variant]} ${className} animate-chat-appear`}>
      {children}
    </div>
  );
};

export default ChatBubble;