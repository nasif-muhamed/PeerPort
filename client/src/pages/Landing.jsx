import { Link } from "react-router-dom";
import { IoIosFlash, IoIosLock, IoIosGlobe } from "react-icons/io";
import ChatButton from "../components/ChatButton";
import ChatBubble from "../components/ChatBubble";
import Card from '../components/CardLanding'
import { useAuthTokens } from '../hooks/useAuthTokens'

const Landing = () => {
  const { username } = useAuthTokens()

  return (
    <div className="min-h-screen flex flex-col justify-center items-center px-4 py-8">
      <div className="max-w-4xl w-full mx-auto text-center">
        {/* Hero Section */}
        <div className="mb-12 animate-fade-in">
          <h1 className="text-5xl md:text-7xl font-bold mb-6 bg-gradient-primary bg-clip-text">
            Peer<span className="text-accent-primary">Port</span>
          </h1>

          <p className="text-xl md:text-2xl text-text-secondary mb-8 max-w-2xl mx-auto">
            Connect instantly, chat temporarily. Create rooms, invite friends, and enjoy conversations that disappear when you're done.
          </p>
        </div>

        {/* Chat Demo Section */}
        <div className="max-w-2xl mx-auto mb-12 space-y-4 animate-slide-up">
          <div className="flex justify-end">
            <ChatBubble variant="sent">
              Hey! Want to create a temporary chat room?
            </ChatBubble>
          </div>
          <div className="flex justify-start">
            <ChatBubble variant="received">
              Absolutely! This looks amazing! 🚀
            </ChatBubble>
          </div>
          <div className="flex justify-end">
            <ChatBubble variant="sent">
              Join PeerPort and let's get started!
            </ChatBubble>
          </div>
        </div>

        {/* Features */}
        <div className="grid md:grid-cols-3 gap-8 mb-12">
          <Card 
            icon={<IoIosFlash />} 
            title={"Instant Rooms"} 
            description={"Create chat rooms in seconds with customizable connection limits"}
          />

          <Card 
            icon={<IoIosLock className="text-amber-400"/>} 
            title={"Temporary"} 
            description={"All conversations are temporary - perfect for quick discussions"}
          />

          <Card 
            icon={<IoIosGlobe className="text-sky-400" />} 
            title={"Public & Private"} 
            description={"Join public rooms or create private ones for your team"}
          />
        </div>

        {/* CTA Buttons */}
        <div className="flex flex-col sm:flex-row gap-4 justify-center items-center animate-slide-up">
          <Link to={username ? "/dashboard" : "/register"}>
            <ChatButton variant="primary" className="w-full sm:w-auto">
              {username ? "Go to Dashboard" : "Get Started"}
            </ChatButton>
          </Link>
          {!username && <Link to={"/login"}>
            <ChatButton variant="secondary" className="w-full sm:w-auto">
              Already have an account?
            </ChatButton>
          </Link>}
        </div>
      </div>
    </div>
  );
};

export default Landing;