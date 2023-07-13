import { createSlice } from '@reduxjs/toolkit'

export const formSlice = createSlice({
  name: 'form',
  initialState: {
    user_prompt: "",
    mode: 0,
    num_songs: "",
    title: "",
    input_error: null
  },
  reducers: {
    submit: (state, action) => {
        state.user_prompt = action.payload.user_prompt;
        state.mode = action.payload.mode;
        state.num_songs = action.payload.num_songs;
        state.title = action.payload.title;
        state.input_error = action.payload.input_error;
    },
    go_back: (state) => {
        state.user_prompt = "";
        state.mode = 0;
        state.num_songs = "";
        state.title = "";
        state.input_error = null;
    }
  },
})

// Action creators are generated for each case reducer function
export const { submit, go_back } = formSlice.actions

export default formSlice.reducer