import { configureStore } from '@reduxjs/toolkit'
import formReducer from '../features/form/formSlice'
import signinReducer from '../features/signin/signinSlice'

export default configureStore({
  reducer: {
    form: formReducer,
    signin: signinReducer,
  },
})