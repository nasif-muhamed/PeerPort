import { useNavigate } from "react-router-dom";
import { IoMdArrowRoundBack } from "react-icons/io";

const BackButton = ({ to, className = "" }) => {
  const navigate = useNavigate();

  const handleBack = () => {
    if (to) {
      navigate(to);
    } else {
      navigate(-1);
    }
  };

  return (
    <button
      onClick={handleBack}
      className={`flex items-center gap-2 text-text-secondary hover:text-text-primary transition-colors duration-200 mb-6 ${className}`}
    >
      <IoMdArrowRoundBack className="w-5 h-5"/>
      Back
    </button>
  );
};

export default BackButton;