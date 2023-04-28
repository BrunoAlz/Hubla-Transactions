import axios from "axios";
import { useAuth } from "../../hooks/useAuth";

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
    localStorage.setItem("user", JSON.stringify(response.data[0]));    
  }
  return response.data;
};

// logout user
const logout = () => {
  localStorage.removeItem("user");
};


const authService = { register, login, logout };
export default authService;
