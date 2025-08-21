import { createSlice } from '@reduxjs/toolkit';
import { persistor } from "../app/store";

const initialState = {
  accessToken: null,
  refreshToken: null,
};

const authSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {
    login: (state, action) => {
      state.accessToken = action.payload.access;
      state.refreshToken = action.payload.refresh;
    },
    updateAcess: (state, action) => {
      state.accessToken = action.payload.access;
    },
    updateRefresh: (state, action) => {
      state.refreshToken = action.payload.refresh;
    },    
    loguout: (state) => {
      state.accessToken = null;
      state.refreshToken = null;
    },
  },
});

export const { login, updateAcess, updateRefresh, loguout } = authSlice.actions;
export default authSlice.reducer;
