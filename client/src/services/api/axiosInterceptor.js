import api from "./axiosInstance";
import { store } from "../../global-state/app/store"; 
import { updateAccess, logout } from "../../global-state/features/authSlice";
import { getRefreshToken } from "./apiService";

const DEBUG_MODE = import.meta.env.VITE_APP_DEBUG === 'true';

// Request interceptor
api.interceptors.request.use(
  (config) => {
    const { accessToken } = store.getState().auth;
    if (accessToken) {
      config.headers.Authorization = `Bearer ${accessToken}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor
api.interceptors.response.use(
  (response) => {
    return response;
  },
  async (error) => {
    const originalRequest = error.config;

    // Handle network errors
    if (!error.response) {
      if (DEBUG_MODE) console.error('Network error:', error.message);
      return Promise.reject(error);
    }

    if (DEBUG_MODE) console.log('Error details:', error.response?.data, error.response?.status);
    // Check if the error is due to an expired token
    if (error.response?.status === 401 && !originalRequest._retry) {
      if (DEBUG_MODE) console.log('Error: Refreshing token due to expired token');
      originalRequest._retry = true;
      const errorCode = error.response?.data?.code;
      if (DEBUG_MODE) console.log('Error Code:', errorCode);
      
      if (errorCode === 'token_not_valid') {
        const { refreshToken } = store.getState().auth;
        if (DEBUG_MODE) console.log('Using refresh token:', refreshToken);

        if (refreshToken) {
          try {
            // Attempt to refresh the token
            const response = await getRefreshToken({refresh: refreshToken})
            if (DEBUG_MODE) console.log('Current access token:', store.getState().auth.accessToken);
            if (DEBUG_MODE) console.log('New access token:', response.data.access);
            
            // Update the access token
            store.dispatch(updateAccess({ access: response.data.access }));

            // Retry the original request with the new token
            originalRequest.headers.Authorization = `Bearer ${response.data.access}`;
            return api(originalRequest);
          } catch (refreshError) {
            // Handle error if token refresh fails
            if (DEBUG_MODE) console.error('Token refresh failed:', refreshError);
            store.dispatch(logout()); // clear tokens on failure
            return Promise.reject(refreshError);
          }
        }
      }
    }
    if (DEBUG_MODE) console.log('outside')
    // if (error.status === 400 && error.response?.data?.error.toLowerCase().includes("invalid token")) {
    //   if (DEBUG_MODE) console.log('inside')
    //   if (DEBUG_MODE) console.warn("Invalid token detected, logging out user...");
    //   store.dispatch(logout());
    // }

    return Promise.reject(error);
  }
);

export default api;
