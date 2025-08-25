import { useEffect, useRef } from 'react';
import TypingIndicator from '../ui/TypingIndicator';
import ChatBubble from '../ChatBubble';

const MessageArea = ({ messages, chatLoading, loadingOlderMessages, onLoadMore, hasMoreMessages }) => {
  const messagesEndRef = useRef(null);
  const messagesContainerRef = useRef(null);
  const prevScrollHeight = useRef(0);
  const shouldScrollToBottom = useRef(true);

  const formatTime = (timestampStr) => {
    const timestamp = new Date(timestampStr);
    return timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  // Scroll to bottom function
  const scrollToBottom = () => {
    const container = messagesContainerRef.current;
    if (container) {
      // Use scrollTop and scrollHeight for reliable scrolling
      container.scrollTop = container.scrollHeight;
    }
  };

  // Scroll to bottom when new messages arrive (not when loading older messages)
  useEffect(() => {
    if (shouldScrollToBottom.current) {
      scrollToBottom();
    }
    shouldScrollToBottom.current = true;
  }, [messages]);

  // Handle scroll event to detect when user reaches the top
  const handleScroll = () => {
    const container = messagesContainerRef.current;
    if (!container) return;

    // Check if scrolled to top (with small threshold)
    if (container.scrollTop <= 10 && hasMoreMessages && !loadingOlderMessages) {
      // Store current scroll height to restore position later
      prevScrollHeight.current = container.scrollHeight;
      shouldScrollToBottom.current = false;
      onLoadMore();
    }
  };

  // Restore scroll position after loading older messages
  useEffect(() => {
    if (!loadingOlderMessages && prevScrollHeight.current > 0) {
      const container = messagesContainerRef.current;
      if (container) {
        // Calculate new scroll position to maintain user's view
        const newScrollHeight = container.scrollHeight;
        const scrollDifference = newScrollHeight - prevScrollHeight.current;
        container.scrollTop = scrollDifference;
        prevScrollHeight.current = 0;
      }
    }
  }, [loadingOlderMessages]);

  return (
    <div
      ref={messagesContainerRef}
      className="flex-1 overflow-y-auto p-4 space-y-4"
      onScroll={handleScroll}
    >
      {/* Unified loading indicator for both older messages and initial chat loading */}
      {(loadingOlderMessages || chatLoading) && (
        <div className="flex justify-center py-4">
          <TypingIndicator />
        </div>
      )}

      {/* Messages */}
      {messages.map((msg, idx) => (
        <div key={msg.id} className="animate-chat-appear">
          {msg.msg_type === 'system' ? (
            <div className="text-center">
              <span className="text-text-muted text-sm bg-background-secondary px-3 py-1 rounded-full">
                {msg.content}
              </span>
            </div>
          ) : (
            <div className={`flex ${msg.msg_type === 'sent' ? 'justify-end' : 'justify-start'}`}>
              <div className={`max-w-xs lg:max-w-md ${msg.msg_type === 'sent' ? 'order-2' : 'order-1'}`}>
                {msg.msg_type === 'received' && (
                  <p className="text-text-secondary text-xs mb-1 px-3">{msg.sender_username}</p>
                )}
                <ChatBubble variant={msg.msg_type === 'sent' ? 'sent' : 'received'}>
                  <p className="break-words">{msg.content}</p>
                  <p className="text-xs opacity-70 mt-1">{formatTime(msg.timestamp)}</p>
                </ChatBubble>
              </div>
            </div>
          )}
        </div>
      ))}
      <div ref={messagesEndRef} />
    </div>
  );
};

export default MessageArea;