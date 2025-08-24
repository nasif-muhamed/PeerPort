import React from "react";

const TypingIndicator = React.memo(({className=""}) => {
  return (
    <div className={`${className} bg-chat-sent rounded-2xl rounded-br-md px-4 py-3 animate-chat-appear`}>
      <div className="flex space-x-1">
        <div className="w-2 h-2 bg-white rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
        <div className="w-2 h-2 bg-white rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
        <div className="w-2 h-2 bg-white rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
      </div>
    </div>
  );
});

export default TypingIndicator