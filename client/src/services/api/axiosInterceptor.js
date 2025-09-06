import api from "./axiosInstance";
import { store } from "../../global-state/app/store";
import { updateAccess, logout } from "../../global-state/features/authSlice";
import { getRefreshToken } from "./apiService";

const DEBUG_MODE = import.meta.env.VITE_APP_DEBUG === 'true';

// Global flag to prevent concurrent refresh attempts
let isRefreshing = false;
let failedQueue = [];

const processQueue = (error, token = null) => {
  failedQueue.forEach((prom) => {
    if (token) {
      prom.resolve(token);
    } else {
      prom.reject(error);
    }
  });
  failedQueue = [];
};

// Request interceptor
api.interceptors.request.use(
  (config) => {
    const { accessToken } = store.getState().auth;
    if (accessToken) {
      config.headers.Authorization = `Bearer ${accessToken}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (!error.response) {
      if (DEBUG_MODE) console.error('Network error:', error.message);
      return Promise.reject(error);
    }

    if (DEBUG_MODE) console.log('Error details:', error.response?.data, error.response?.status);

    if (error.response?.status === 401 && !originalRequest._retry) {
      if (DEBUG_MODE) console.log('Error: Attempting to refresh token');
      originalRequest._retry = true;

      const errorCode = error.response?.data?.code;
      if (DEBUG_MODE) console.log('Error Code:', errorCode);

      if (errorCode === 'token_not_valid') {
        const { refreshToken } = store.getState().auth;
        if (DEBUG_MODE) console.log('Using refresh token:', refreshToken);

        if (refreshToken) {
          if (isRefreshing) {
            return new Promise((resolve, reject) => {
              failedQueue.push({ resolve, reject });
            })
              .then((token) => {
                originalRequest.headers.Authorization = `Bearer ${token}`;
                return api(originalRequest);
              })
              .catch((err) => Promise.reject(err));
          }

          isRefreshing = true;

          try {
            const response = await getRefreshToken({ refresh: refreshToken });
            const newAccessToken = response.data.access;
            if (DEBUG_MODE) console.log('New access token:', newAccessToken);

            store.dispatch(updateAccess({ access: newAccessToken }));
            originalRequest.headers.Authorization = `Bearer ${newAccessToken}`;
            processQueue(null, newAccessToken);
            isRefreshing = false;

            return api(originalRequest);
          } catch (refreshError) {
            if (DEBUG_MODE) console.error('Token refresh failed:', refreshError);

            if (refreshError.response?.status === 401 || !refreshToken) {
              if (DEBUG_MODE) console.log('Refresh token invalid or expired, logging out');
              store.dispatch(logout()); // Clear tokens from Redux
              processQueue(refreshError);
              isRefreshing = false;
              // Force redirect to login
              window.location.href = '/login';
              return Promise.reject(refreshError);
            }

            processQueue(refreshError);
            isRefreshing = false;
            return Promise.reject(refreshError);
          }
        } else {
          if (DEBUG_MODE) console.log('No refresh token available, logging out');
          store.dispatch(logout());
          window.location.href = '/login';
          return Promise.reject(error);
        }
      }
    }

    if (DEBUG_MODE) console.log('Non-401 error or retry exhausted');
    return Promise.reject(error);
  }
);

export default api;