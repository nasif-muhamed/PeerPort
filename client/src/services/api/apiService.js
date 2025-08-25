import api from "./axiosInterceptor";

// auth
export const registerUser = (data) => api.post("users/register/", data);
export const loginUser = (data) => api.post("users/login/", data);
export const getRefreshToken = (data) => api.post("users/refresh-token/", data);
export const getProfile = () => api.post("users/profile/");
export const logoutUser = (data) => api.post("users/logout/", data);

// chat
export const createRoom = (data) => api.post("chats/rooms/", data);
export const getMyRooms = (url) => api.get(url || "chats/rooms/");
export const getAllRooms = (url, searchTerm) => api.get(url || "chats/all-rooms/", {params: {search: searchTerm}});
export const getRoomDetials = (roomId) => api.get(`/chats/rooms/${roomId}`)
export const getMessages = (roomId, page=1) => api.get(`/chats/rooms/${roomId}/messages/`, {params: {page:page, page_size: 9}})
