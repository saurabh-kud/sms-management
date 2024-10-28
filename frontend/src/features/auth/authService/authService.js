import axios from "axios";

const BASE_URL = import.meta.env.VITE_APP_BASE_URL;

const register = async (userData) => {
  const response = await axios.post(`${BASE_URL + "/register"}`, userData);
  if (response.data) {
    localStorage.setItem("user", JSON.stringify(response.data.data));
  }
  return response.data.data;
};

const login = async (userData) => {
  const response = await axios.post(`${BASE_URL + "/login"}`, userData);
  if (response.data) {
    localStorage.setItem("user", JSON.stringify(response.data.data));
  }
  return response.data.data;
};

const logout = () => {
  localStorage.removeItem("user");
};

const serviceAuth = {
  register,
  login,
  logout,
};

export default serviceAuth;
