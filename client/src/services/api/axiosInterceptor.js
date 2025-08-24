import api from "./axiosInstance";
import { store } from "../../global-state/app/store"; 
import { updateAcess, loguout } from "../../global-state/features/authSlice";
import { getRefreshToken } from "./api_service";

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
    console.log('her:', error.response?.data?.error, error.status)
    // Check if the error is due to an expired token
    if (error.response?.status === 401 && !originalRequest._retry) {
      console.log('Error: Refreshing token due to expired token');
      originalRequest._retry = true;
      const errorCode = error.response?.data?.code;
      console.log('Error Code:', errorCode);
      
      if (errorCode === 'token_not_valid') {
        const { refreshToken } = store.getState().auth;
        console.log('Using refresh token:', refreshToken);

        if (refreshToken) {
          try {
            // Attempt to refresh the token
            const response = await getRefreshToken({refresh: refreshToken})
            console.log('Current access token:', store.getState().auth.accessToken);
            console.log('New access token:', response.data.access);
            
            // Update the access token
            store.dispatch(updateAcess({ access: response.data.access }));

            // Retry the original request with the new token
            originalRequest.headers.Authorization = `Bearer ${response.data.access}`;
            return api(originalRequest);
          } catch (refreshError) {
            // Handle error if token refresh fails
            console.error('Token refresh failed:', refreshError);
            store.dispatch(loguout()); // clear tokens on failure
            return Promise.reject(refreshError);
          }
        }
      }
    }
    console.log('outside')
    if (error.status === 400 && error.response?.data?.error.toLowerCase().includes("invalid token")) {
      console.log('inside')
      console.warn("Invalid token detected, logging out user...");
      store.dispatch(loguout());
    }

    return Promise.reject(error);
  }
);

export default api;
