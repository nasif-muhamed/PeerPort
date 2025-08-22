import { useState } from "react";
import { toast } from "sonner";

import ChatInput from "./ChatInput";
import ChatButton from "./ChatButton";
import ChatBubble from "./ChatBubble";
import validateCreateRoomFormData from "../utils/validations/validateCreateRoomFormData";
import ChatLoader from "./ui/ChatLoader";
import { createRoom } from "../services/api/api_service";
import { handleError } from "../utils/handleError";

const CreateRoomModal = ({ onClose }) => {
  const [loading, setLoading] = useState(false)
  const [formData, setFormData] = useState({
    name: "",
    limit: 10,
    access: "public"
  });

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const {isValid, errorMessage} = validateCreateRoomFormData(formData);
    if (!isValid) {
      toast.error(errorMessage);
      return;
    };

    try{
      setLoading(true);
      const response = await createRoom(formData);
      toast.success('Room created successfully');
      onClose();
    }catch (error){
      handleError(error);
    }finally{
      setLoading(false);
    };
  };

  return (
    <div className="fixed inset-0 bg-bg-primary/80 backdrop-blur-sm flex items-center justify-center px-4 z-50">
      <div className="bg-bg-secondary border border-border-primary rounded-2xl p-6 w-full max-w-md animate-scale-in">
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-2xl font-bold">Create New Room</h2>
          <button 
            onClick={onClose}
            className="text-text-secondary hover:text-text-primary transition-colors"
          >
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        {/* Chat-style Form */}
        <div className="space-y-6">
          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="flex justify-start">
                <ChatBubble variant="received">
                  What should we call this room?
                </ChatBubble>
            </div>

            <div className="flex justify-end">
              <ChatInput
                placeholder="Enter room name"
                name="name"
                value={formData.name}
                onChange={handleChange}
                variant="sent"
                required
              />
            </div>

            <div className="flex justify-start">
              <ChatBubble variant="received">
                How many people can join?
              </ChatBubble>
            </div>

            <div className="flex justify-end">
              <select
                name="limit"
                value={formData.limit}
                onChange={handleChange}
                className="chat-input-sent appearance-none cursor-pointer"
                required
              >
                <option value={3}>3 people</option>
                <option value={5}>5 people</option>
                <option value={10}>10 people</option>
                <option value={15}>15 people</option>
                <option value={20}>20 people</option>
                <option value={50}>50 people</option>
              </select>
            </div>

            <div className="flex justify-start">
              <ChatBubble variant="received">
                Should this be a public room?
              </ChatBubble>
            </div>

            <div className="flex justify-end">
              <select
                name="access"
                value={formData.access}
                onChange={(e) => setFormData({...formData, access: e.target.value})}
                className="chat-input-sent appearance-none cursor-pointer"
                required
              >
                <option value="public">Yes, make it public</option>
                <option value="private">No, keep it private</option>
              </select>
            </div>

            <div className="flex justify-center gap-4 mt-8">
              <ChatButton 
                type="button"
                variant="secondary"
                className="bg-black/20"
                onClick={onClose}
              >
                Cancel
              </ChatButton>
              <ChatButton 
                type="submit"
                variant="primary"
              >
                Create Room
              </ChatButton>
            </div>
          </form>
        </div>
      </div>

      {loading && <ChatLoader />}
    </div>
  );
};

export default CreateRoomModal