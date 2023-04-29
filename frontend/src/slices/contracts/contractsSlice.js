import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import contractsService from "../../services/contracts/contractsService";

const initialState = {
  upload: [],
  isError: false,
  isLoading: false,
  isSuccess: false,
  message: "",
};

export const fileUpload = createAsyncThunk(
  "contracts/fileUpload",
  async (fileUpload, thunkAPI) => {
    const token = thunkAPI.getState().auth.user.token;

    const data = await contractsService.contractUpload(fileUpload, token);

    if (data.success) {
      return thunkAPI.fulfillWithValue(data);
    } else {
      const message = data.error.upload[0];
      return thunkAPI.rejectWithValue(message);
    }
  }
);



export const fileUploadSlice = createSlice({
  name: "fileUpload",
  initialState,
  reducers: {
    reset: (state) => {
      state.isLoading = false;
      state.isError = false;
      state.isSuccess = false;
      state.message = "";
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fileUpload.pending, (state) => {
        state.isLoading = true;
        state.isError = false;
      })
      .addCase(fileUpload.fulfilled, (state, action) => {
        state.isLoading = false;
        state.isSuccess = true;
        state.isError = null;
        state.message = action.payload;
      })
      .addCase(fileUpload.rejected, (state, action) => {
        state.isLoading = false;
        state.isSuccess = false;
        state.isError = true;
        state.message = action.payload;
      });
  },
});

export const { reset } = fileUploadSlice.actions;
export default fileUploadSlice.reducer;
