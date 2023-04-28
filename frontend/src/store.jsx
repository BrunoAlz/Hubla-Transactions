import { configureStore } from "@reduxjs/toolkit";

import authReducer from "../src/slices/auth/authSlice";

export const store = configureStore({
  reducer: {
    auth: authReducer,
  },
});
