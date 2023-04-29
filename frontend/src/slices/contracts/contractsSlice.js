import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import contractsService from "../../services/contracts/contractsService";

const initialState = {
  upload: [],
  error: false,
  success: false,
  loading: false,
};

// Publish user publish
export const fileUpload = createAsyncThunk(
  "fileUpload/publish",
  async (fileUpload, thunkAPI) => {
    const token = thunkAPI.getState().auth.user.token;

    const data = await contractsService.contractUpload(fileUpload, token);

    // Check for erros
    if (data.errors) {
      return thunkAPI.rejectWithValue(data.errors[0]);
    }
    return data;
  }
);

export const fileUploadSlice = createSlice({
  name: "fileUpload",
  initialState,
  reducers: {
    resetMessage: (state) => {
      state.message = null;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fileUpload.pending, (state) => {
        state.loading = true;
        state.error = false;
      })
      .addCase(fileUpload.fulfilled, (state, action) => {
        state.loading = false;
        state.success = true;
        state.error = null;
        state.upload = action.payload;
        state.message = "Contrato cadastrado com Sucesso!";
      })
      .addCase(fileUpload.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
        state.fileUpload = [];
      });
  },
});

export default fileUpload.reducer;
