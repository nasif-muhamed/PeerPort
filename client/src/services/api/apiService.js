import axios from "axios";
import api from "./axiosInterceptor";


const BASE_URL = import.meta.env.VITE_API_URL


// auth
export const registerUser = (data) => api.post("users/register/", data);
export const loginUser = (data) => api.post("users/login/", data);
export const getRefreshToken = (data) => axios.post(`${BASE_URL}/users/refresh-token/`, data);
export const getProfile = () => api.post("users/profile/");
export const logoutUser = (data) => api.post("users/logout/", data);

// chat
export const createRoom = (data) => api.post("chats/rooms/", data);
export const getMyRooms = (url) => api.get(url || "chats/rooms/");
export const getMyRoom = (roomId) => api.get(`chats/my-rooms/${roomId}/`);
export const updateMyRoom = (roomId, data) => api.patch(`chats/my-rooms/${roomId}/`, data);
export const deleteMyRoom = (roomId) => api.delete(`chats/my-rooms/${roomId}/`);
export const getAllRooms = (url, searchTerm) => api.get(url || "chats/all-rooms/", {params: {search: searchTerm}});
export const getRoomDetials = (roomId) => api.get(`/chats/rooms/${roomId}`)
export const getMessages = (roomId, page=1) => api.get(`/chats/rooms/${roomId}/messages/`, {params: {page:page, page_size: 9}})
