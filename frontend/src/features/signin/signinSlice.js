import { createSlice } from '@reduxjs/toolkit'

export const signinSlice = createSlice({
  name: 'signin',
  initialState: {
    signin: false,
  },
  reducers: {
    signin: (state, action) => {
        state.signin = action.payload.signin;
    },
  },
})

export const { signin } = signinSlice.actions

export default signinSlice.reducer