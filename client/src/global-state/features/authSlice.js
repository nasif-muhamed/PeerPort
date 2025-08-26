import { createSlice } from '@reduxjs/toolkit';

const initialState = {
  accessToken: null,
  refreshToken: null,
  username: null,
  userId: null,
};

const authSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {
    login: (state, action) => {
      state.userId = action.payload.userId;
      state.username = action.payload.username;
      state.accessToken = action.payload.access;
      state.refreshToken = action.payload.refresh;
    },
    updateAccess: (state, action) => {
      state.accessToken = action.payload.access;
    },
    updateRefresh: (state, action) => {
      state.refreshToken = action.payload.refresh;
    },
    logout: (state) => {
      state.accessToken = null;
      state.refreshToken = null;
      state.username = null;
      state.userId = null;
    },
  },
});

export const { login, updateAccess, updateRefresh, logout } = authSlice.actions;
export default authSlice.reducer;
