import axios from "axios";

const API_ENDPOINT = "http://127.0.0.1:8000/api/";
//

const CONFIG = { headers: { "Content-Type": "application/json" } };

// USER REGISTER
const register = async (userData) => {
  const response = await axios.post(
    API_ENDPOINT + "users/register/",
    userData,
    CONFIG
  );
  return response;
};

// USER LOGIN
const login = async (userData) => {
  const response = await axios.post(
    API_ENDPOINT + "users/login/",
    userData,
    CONFIG
  );
  if (response.data[0].token) {
    localStorage.setItem("user", JSON.stringify(response.data));
  }
  return response.data;
};

const authService = { register, login };
export default authService;
