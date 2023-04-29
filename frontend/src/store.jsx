import { configureStore } from "@reduxjs/toolkit";

import authReducer from "../src/slices/auth/authSlice";
import contractReducer  from "../src/slices/contracts/contractsSlice";

export const store = configureStore({
  reducer: {
    auth: authReducer,
    contracts: contractReducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: false,
    }),
});
