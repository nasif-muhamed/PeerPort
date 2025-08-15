const ChatButton = ({ 
  children, 
  variant = "primary", 
  onClick, 
  disabled = false, 
  className = "",
  type = "button" 
}) => {
  const variants = {
    primary: "btn-primary",
    secondary: "btn-secondary", 
    send: "btn-send"
  };

  return (
    <button
      type={type}
      onClick={onClick}
      disabled={disabled}
      className={`${variants[variant]} ${className} ${disabled ? 'opacity-50 cursor-not-allowed' : ''}`}
    >
      {children}
    </button>
  );
};

export default ChatButton;