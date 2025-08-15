import { Link } from "react-router-dom";
import ChatButton from "../components/ChatButton";
import ChatBubble from "../components/ChatBubble";

const NotFound = () => {
  return (
    <div className="min-h-screen flex flex-col justify-center items-center px-4 py-8">
      <div className="max-w-2xl w-full mx-auto text-center">
        {/* Chat-style 404 */}
        <div className="space-y-6 mb-12">
          <div className="flex justify-start animate-chat-appear">
            <ChatBubble variant="received">
              Hmm... I can't find that page 🤔
            </ChatBubble>
          </div>
          <div className="flex justify-end animate-chat-appear" style={{animationDelay: '0.3s'}}>
            <ChatBubble variant="sent">
              Error 404: Page not found
            </ChatBubble>
          </div>
          <div className="flex justify-start animate-chat-appear" style={{animationDelay: '0.6s'}}>
            <ChatBubble variant="received">
              Let's get you back to somewhere useful! 🚀
            </ChatBubble>
          </div>
        </div>

        <div className="space-y-4 animate-fade-in">
          <h1 className="text-6xl font-bold text-accent-primary mb-4">404</h1>
          <p className="text-xl text-text-secondary mb-8">
            Looks like this chat room doesn't exist or has been closed.
          </p>
          
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link>
              <ChatButton variant="primary">
                Go Home
              </ChatButton>
            </Link>
            <Link>
              <ChatButton variant="secondary">
                Dashboard
              </ChatButton>
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
};

export default NotFound;