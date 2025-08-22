import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { IoIosSend  } from "react-icons/io";
import { toast } from 'sonner'

import ChatInput from "../components/ChatInput";
import ChatButton from "../components/ChatButton";
import ChatBubble from "../components/ChatBubble";
import validateRegisterFormData from "../utils/validations/validateRegisterFormData"
import ChatLoader from "../components/ui/ChatLoader";
import { registerUser } from "../services/api/api_service"
import { handleError } from "../utils/handleError";

const Register = () => {
  const [loading, setLoading] = useState(false)
  const [formData, setFormData] = useState({
    username: "",
    email: "",
    password: "",
    confirmPassword: "",
  });
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const {isValid, errorMessage} = validateRegisterFormData(formData);
    if (!isValid) {
      toast.error(errorMessage);
      return;
    };

    try{
      setLoading(true);
      const response = await registerUser(formData);
      toast.success(response?.data?.message || 'User registered successfully');
      navigate('/login');
    }catch (error){
      handleError(error);
    }finally{
      setLoading(false);
    };
  };

  return (
    <div className="min-h-screen flex flex-col justify-center items-center px-4 py-8">
      {loading && <ChatLoader message="Kindly wait for a moment"/>}
      <div className="max-w-md w-full">        
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold mb-2">Join PeerPort</h1>
          <p className="text-text-secondary">Create your account to start chatting</p>
        </div>

        {/* Chat-style Registration Form */}
        <div className="space-y-6">
          <div className="flex justify-end">
            <ChatBubble variant="received">
              What should we call you?
            </ChatBubble>
          </div>
          
          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="flex justify-end">
              <ChatInput
                placeholder="Enter your username"
                name="username"
                value={formData.username}
                onChange={handleChange}
                variant="sent"
                required
              />
            </div>

            <div className="flex justify-start">
              <ChatBubble variant="received">
                And your email address?
              </ChatBubble>
            </div>

            <div className="flex justify-end">
              <ChatInput
                placeholder="Enter your email"
                name="email"
                type="email"
                value={formData.email}
                onChange={handleChange}
                variant="sent"
                required
              />
            </div>

            <div className="flex justify-start">
              <ChatBubble variant="received">
                Create a secure password & confirm it!
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

            <div className="flex justify-end">
              <ChatInput
                placeholder="confirm your password"
                name="confirmPassword"
                type="password"
                value={formData.confirmPassword}
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
              Already have an account?{" "}
              <Link to="/login" className="text-accent-primary hover:text-chat-sent-hover transition-colors">
                Sign in here
              </Link>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Register;