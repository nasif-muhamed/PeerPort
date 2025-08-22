import api from "./axiosInterceptor";

// auth
export const registerUser = (data) => api.post("users/register/", data);
export const loginUser = (data) => api.post("users/login/", data);
export const getRefreshToken = (data) => api.post("users/refresh-token/", data);
export const getProfile = () => api.post("users/profile/");
export const logoutUser = (data) => api.post("users/logout/", data);

// chat
export const createRoom = (data) => api.post("chats/rooms/", data);
