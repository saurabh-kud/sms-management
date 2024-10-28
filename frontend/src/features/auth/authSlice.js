import { createAsyncThunk, createSlice } from "@reduxjs/toolkit";

import serviceAuth from "./authService/authService";

const user = JSON.parse(localStorage.getItem("user"));
const initialState = {
  user: user ? user : null,
  isError: false,
  isLoading: false,
  isSucess: false,
  msg: "",
};
//register a user with backend
export const register = createAsyncThunk(
  "auth/register",
  async (userData, thunkAPI) => {
    try {
      return await serviceAuth.register(userData);
    } catch (error) {
      const message = error.response.data && error.response.data.message;
      return thunkAPI.rejectWithValue(message);
    }
  }
);

//login a user with backend
export const login = createAsyncThunk(
  "auth/login",
  async (userData, thunkAPI) => {
    try {
      return await serviceAuth.login(userData);
    } catch (error) {
      const message = error.response.data && error.response.data.message;
      return thunkAPI.rejectWithValue(message);
    }
  }
);

//logout the user
export const logout = createAsyncThunk("auth/logout", async () => {
  await serviceAuth.logout();
});

const authSlice = createSlice({
  name: "auth",
  initialState,
  reducers: {
    reset: (state) => {
      state.isError = false;
      state.isLoading = false;
      state.isSucess = false;
      state.msg = "";
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(register.pending, (state) => {
        state.isLoading = true;
      })
      .addCase(register.fulfilled, (state, { payload }) => {
        state.isLoading = false;
        state.isSucess = true;
        state.user = payload;
      })
      .addCase(register.rejected, (state, { payload }) => {
        state.isLoading = false;
        state.isSucess = false;
        state.isError = true;
        state.msg = payload;
        state.user = null;
      })
      .addCase(login.pending, (state) => {
        state.isLoading = true;
      })
      .addCase(login.fulfilled, (state, { payload }) => {
        state.isLoading = false;
        state.isSucess = true;
        state.user = payload;
      })
      .addCase(login.rejected, (state, { payload }) => {
        state.isLoading = false;
        state.isSucess = false;
        state.isError = true;
        state.msg = payload;
        state.user = null;
      })
      .addCase(logout.fulfilled, (state) => {
        state.isError = false;
        state.isSucess = false;
        state.isLoading = false;
        state.msg = "";
        state.user = null;
      });
  },
});

export const { reset } = authSlice.actions;
export default authSlice.reducer;
