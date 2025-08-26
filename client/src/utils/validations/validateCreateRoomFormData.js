const validateCreateRoomFormData = (formData) => {
  const name = formData.name.trim();
  const limit = formData.limit;
  const access = formData.access.trim();

  // Validate room name
  if (!name) {
    return { isValid: false, errorMessage: "Room name is required." };
  }

  if (name.length < 3) {
    return { isValid: false, errorMessage: "Room name must be at least 3 characters." };
  }

  if (name.length > 255) {
    return { isValid: false, errorMessage: "Room name should not be more than 255 characters." };
  }

  if (!/^[a-zA-Z0-9\s]*$/.test(name)) {
    return { isValid: false, errorMessage: "Room name should only contain letters, numbers, and spaces." };
  }

  if (!access) {
    return { isValid: false, errorMessage: "Access type is required." };
  }

  if (access !== "public" && access !== "private") {
    return { isValid: false, errorMessage: "Access type must be either PUBLIC or PRIVATE." };
  }

  if (!limit) {
    return { isValid: false, errorMessage: "Max limit is required." };
  }

  if (limit < 1 || limit > 50) {
    return { isValid: false, errorMessage: "Limit must be between 1 and 50." };
  }

  return { isValid: true, errorMessage: null };
};

export default validateCreateRoomFormData;
