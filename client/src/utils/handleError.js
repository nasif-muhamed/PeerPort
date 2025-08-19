import { toast } from "sonner";

export const handleError = (error) => {
  const DEBUG_MODE = import.meta.env.VITE_APP_DEBUG === 'true';
  if (DEBUG_MODE) console.log('error:', error);

  let message = "Something went wrong. Please try again.";

  if (error?.response) {
    // Backend responded with an error
    const data = error.response.data;

    if (typeof data === "string") {
      message = data;
    } else if (typeof data?.detail === "string") {
      message = data.detail;
    } else if (typeof data === "object") {
      // Collect field-specific errors from DRF
      message = Object.values(data).flat().join(" ") || message;
    }
  } else if (error?.request) {
    // No response (e.g. server down, CORS, network error)
    message = "Server not responding. Please check your connection.";
  } else if (error?.message) {
    // JS error (e.g. request setup)
    message = error.message;
  }

  toast.error(message);
};
