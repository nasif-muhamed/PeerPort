import { createSlice } from '@reduxjs/toolkit';

const initialState = {
  currentRoom: null,
};

const uiSlice = createSlice({
  name: 'ui',
  initialState,
  reducers: {
    setCurrentRoom: (state, payload) => {
      state.currentRoom = payload.currentRoom;
    },
  },
});

export const { setCurrentRoom } = uiSlice.actions;
export default uiSlice.reducer;
