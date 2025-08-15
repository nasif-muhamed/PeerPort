const validateFormData = (formData) => {
  const username = formData.username.trim();
  const email = formData.email.trim();
  const password = formData.password.trim();
  const confirmPassword = formData.confirmPassword.trim();

  const usernameRegex = /^[a-z_]{4,}$/;
  if (!usernameRegex.test(username)) {
    return { isValid: false, errorMessage: "Username must be at least 4 characters and contain only lowercase letters and underscores." };
  }

  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailRegex.test(email)) {
    return { isValid: false, errorMessage: "Please enter a valid email address." };
  }

  const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;
  if (!passwordRegex.test(password)) {
    return { isValid: false, errorMessage: "Password must be at least 8 characters with 1 lowercase, 1 uppercase, 1 number, and 1 special character." };
  }

  if (password !== confirmPassword) {
    return { isValid: false, errorMessage: "Passwords do not match." };
  }

  return { isValid: true, errorMessage: null };
};

export default validateFormData;