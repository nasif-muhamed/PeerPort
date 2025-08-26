const validateLoginFormData = (formData) => {
  const username = formData.username.trim();
  const password = formData.password.trim();

  if (!username) {
    return { isValid: false, errorMessage: "Username is required." };
  }

  if (!password) {
    return { isValid: false, errorMessage: "Password is required." };
  }

  return { isValid: true, errorMessage: null };
};

export default validateLoginFormData;