import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { IoLogOutOutline, IoPersonCircleOutline, IoMenuOutline, IoCloseOutline } from 'react-icons/io5';
import { toast } from 'sonner';
import { clearTokens } from '../../utils/tokenManager';

const ChatNavbar = ({
  username = "User",
  className = ""
}) => {
  const navigate = useNavigate();
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  const handleLogout = () => {
    setIsMobileMenuOpen(false);
    clearTokens();
    toast.info('See you soon');
    navigate('/', { replace: true });
  };

  return (
    <>
      {/* Fixed Floating Navbar - Made Wider */}
      <nav className={`fixed top-4 left-1/2 transform -translate-x-1/2 z-50 ${className}`}>
        <div className="bg-bg-primary/80 backdrop-blur-xl border border-border-primary/50 rounded-2xl shadow-card px-8 py-4 max-w-6xl w-[calc(100vw-2rem)] mx-4 sm:w-auto sm:mx-0">
          <div className="flex items-center justify-between space-x-6">
            {/* Logo/Brand */}
            <div className="flex items-center space-x-3">
              <div className="w-8 h-8 bg-gradient-to-r from-accent-primary to-chat-sent-hover rounded-full flex items-center justify-center animate-pulse">
                <div className="w-4 h-4 bg-white rounded-full" />
              </div>
              <h1 className="text-xl font-bold text-text-primary">
                Peer<span className="text-accent-primary">Port</span>
              </h1>
            </div>

            {/* Desktop: User Info & Logout */}
            <div className="hidden sm:flex items-center space-x-6">
              {/* User Bubble */}
              <div className="chat-bubble-received flex items-center space-x-2 !py-2 !px-4 !max-w-none">
                <IoPersonCircleOutline className="w-5 h-5 text-accent-secondary" />
                <span className="text-sm font-medium">{username}</span>
              </div>

              {/* Logout Button */}
              <button
                onClick={handleLogout}
                className="group bg-bg-tertiary hover:bg-accent-danger/20 border border-border-primary hover:border-accent-danger/50 rounded-xl px-5 py-2.5 transition-all duration-200 flex items-center space-x-2"
                title="Logout"
              >
                <IoLogOutOutline className="w-5 h-5 text-text-secondary group-hover:text-accent-danger transition-colors" />
                <span className="text-sm text-text-secondary group-hover:text-accent-danger transition-colors">
                  Logout
                </span>
              </button>
            </div>

            {/* Mobile: Menu Button */}
            <button
              onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
              className="sm:hidden bg-bg-tertiary hover:bg-bg-secondary border border-border-primary rounded-xl p-2 transition-all duration-200"
            >
              {isMobileMenuOpen ? (
                <IoCloseOutline className="w-5 h-5 text-text-primary" />
              ) : (
                <IoMenuOutline className="w-5 h-5 text-text-primary" />
              )}
            </button>
          </div>

          {/* Mobile Menu */}
          {isMobileMenuOpen && (
            <div className="sm:hidden mt-4 pt-4 border-t border-border-primary animate-slide-up">
              <div className="space-y-3">
                {/* User Info */}
                <div className="chat-bubble-received flex items-center space-x-2 !py-2 !px-3 !max-w-none">
                  <IoPersonCircleOutline className="w-5 h-5 text-accent-secondary" />
                  <span className="text-sm font-medium">{username}</span>
                </div>

                {/* Logout Button */}
                <button
                  onClick={handleLogout}
                  className="w-full group bg-bg-tertiary hover:bg-accent-danger/20 border border-border-primary hover:border-accent-danger/50 rounded-xl px-4 py-3 transition-all duration-200 flex items-center justify-center space-x-2"
                >
                  <IoLogOutOutline className="w-5 h-5 text-text-secondary group-hover:text-accent-danger transition-colors" />
                  <span className="text-sm text-text-secondary group-hover:text-accent-danger transition-colors">
                    Logout
                  </span>
                </button>
              </div>
            </div>
          )}
        </div>
      </nav>

      {/* Mobile Menu Backdrop */}
      {isMobileMenuOpen && (
        <div
          className="fixed inset-0 bg-black/20 backdrop-blur-sm z-40 sm:hidden"
          onClick={() => setIsMobileMenuOpen(false)}
        />
      )}
    </>
  );
};

export default ChatNavbar;
