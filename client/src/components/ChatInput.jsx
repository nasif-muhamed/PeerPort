import { useState } from "react";
import { FaEye, FaEyeSlash } from "react-icons/fa";

const ChatInput = ({ 
  placeholder,
  name,
  value, 
  onChange, 
  variant = "sent",
  type = "text",
  required = false,
  className = "",
  ...rest
}) => {
  const variants = {
    sent: "chat-input-sent",
    received: "chat-input-received"
  };
  
  const [showPassword, setShowPassword] = useState(false);
  const isPasswordField = type === "password";

  return (
    <div className="relative">
      <input
        type={isPasswordField ? (showPassword ? "text" : "password") : type}
        name={name}
        placeholder={placeholder}
        value={value}
        onChange={onChange}
        required={required}
        className={`${variants[variant]} ${className} animate-chat-appear ${isPasswordField && "pr-8"}`}
        {...rest}
      />
      {isPasswordField && (
        <button
          type="button"
          onClick={() => setShowPassword(!showPassword)}
          className="absolute right-3 top-1/2 -translate-y-1/2 text-white "
        >
          {showPassword ? <FaEyeSlash /> : <FaEye />}
        </button>
      )}
    </div>
  );
};

export default ChatInput;