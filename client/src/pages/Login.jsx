import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { IoIosSend  } from "react-icons/io";
import { toast } from "sonner";

import ChatInput from "../components/ChatInput";
import ChatButton from "../components/ChatButton";
import ChatBubble from "../components/ChatBubble";
import ChatLoader from "../components/ui/ChatLoader";
import validateLoginFormData from "../utils/validations/validateLoginFormData"
import { loginUser } from "../services/api/api_service"
import { handleError } from "../utils/handleError";
import { useAuthTokens } from "../hooks/useAuthTokens";

const Login = () => {
  const [loading, setLoading] = useState(false)
  const { setTokens } = useAuthTokens()
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    username: "",
    password: ""
  });

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const {isValid, errorMessage} = validateLoginFormData(formData);
    if (!isValid) {
      toast.error(errorMessage);
      return;
    };

    try{
      setLoading(true)
      const response = await loginUser(formData)
      setTokens(response?.data?.access, response?.data?.refresh);
      navigate('/dashboard')
    }catch (error) {
      handleError(error)
    }finally{
      setLoading(false)
    }
  };

  return (
    <div className="min-h-screen flex flex-col justify-center items-center px-4 py-8">
      {loading && <ChatLoader message="Kindly wait for a moment"/>}
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