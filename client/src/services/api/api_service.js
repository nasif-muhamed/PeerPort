import api from "./axiosInterceptor";

export const registerUser = (data) => api.post("users/register/", data);
export const loginUser = (data) => api.post("users/login/", data);
export const getRefreshToken = (data) => api.post("users/refresh-token/", data);
export const getProfile = () => api.post("users/profile/");