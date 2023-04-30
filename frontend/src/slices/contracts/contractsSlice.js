import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import contractsService from "../../services/contracts/contractsService";

const initialState = {
  upload: [],
  contracts: [],
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

export const contractsList = createAsyncThunk(
  "contracts/listAll",
  async (_, thunkAPI) => {
    const token = thunkAPI.getState().auth.user.token;
    const data = await contractsService.getContracts(token);
    console.log(data.data);
    if (data.data) {
      return thunkAPI.fulfillWithValue(data.data);
    } else {
      const message = data;
      return thunkAPI.rejectWithValue(message);
    }
  }
);

export const contractsSlice = createSlice({
  name: "fileUpload",
  initialState,
  reducers: {
    reset: (state) => initialState,
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
        state.isError = false;
        state.message = action.payload;
      })
      .addCase(fileUpload.rejected, (state, action) => {
        state.isLoading = false;
        state.isSuccess = false;
        state.isError = true;
        state.message = action.payload;
      })
      .addCase(contractsList.pending, (state) => {
        state.isLoading = true;
      })
      .addCase(contractsList.fulfilled, (state, action) => {
        state.isLoading = false;
        state.isSuccess = true;
        state.isError = false;
        state.message = action.payload;
        state.contracts = action.payload;
      })
      .addCase(contractsList.rejected, (state, action) => {
        state.isLoading = false;
        state.isSuccess = false;
        state.isError = true;
        state.message = action.payload;
      });
  },
});

export const { reset } = contractsSlice.actions;
export default contractsSlice.reducer;