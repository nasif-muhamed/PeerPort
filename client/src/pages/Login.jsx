import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { IoIosSend  } from "react-icons/io";
import { toast } from "sonner";
import { loginUser } from "../services/api/api_service"
import ChatInput from "../components/ChatInput";
import ChatButton from "../components/ChatButton";
import ChatBubble from "../components/ChatBubble";

const Login = () => {
  const [formData, setFormData] = useState({
    username: "",
    password: ""
  });
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!formData.username.trim()){
      toast.error('Username is required')
    }
    if (!formData.password.trim()){
      toast.error('Password is required')
    }
    try{

    }catch{

    }finally{
      
    }
  };

  return (
    <div className="min-h-screen flex flex-col justify-center items-center px-4 py-8">
      <div className="max-w-md w-full">        
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold mb-2">Welcome Back</h1>
          <p className="text-text-secondary">Sign in to continue chatting</p>
        </div>

        {/* Chat-style Login Form */}
        <div className="space-y-6">
          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="flex justify-start">
              <ChatBubble variant="received">
                Welcome back! What's your username?
              </ChatBubble>
            </div>

            <div className="flex justify-end">
              <ChatInput
                placeholder="Enter your username"
                name="username"
                type="text"
                value={formData.username}
                onChange={handleChange}
                variant="sent"
                required
              />
            </div>

            <div className="flex justify-start">
              <ChatBubble variant="received">
                And your password?
              </ChatBubble>
            </div>

            <div className="flex justify-end">
              <ChatInput
                placeholder="Enter your password"
                name="password"
                type="password"
                value={formData.password}
                onChange={handleChange}
                variant="sent"
                required
              />
            </div>

            <div className="flex justify-end mt-8">
              <ChatButton 
                type="submit" 
                variant="send"
                className="rounded-full p-4"
              >
                <IoIosSend  className="w-6 h-6"/>
              </ChatButton>
            </div>
          </form>

          <div className="text-center mt-6 animate-fade-in">
            <p className="text-text-secondary">
              Don't have an account?{" "}
              <Link to="/register" className="text-accent-primary hover:text-chat-sent-hover transition-colors">
                Create one here
              </Link>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Login;