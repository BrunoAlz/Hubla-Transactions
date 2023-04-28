import axios from "axios";

const REGISTER_URL = "http://127.0.0.1:8000/api/users/register/";
// 

const CONFIG = { headers: { "Content-Type": "application/json" } };

// USER REGISTER
const register = async (userData) => {
  const response = await axios.post(REGISTER_URL, userData, CONFIG);
  return response;
};


const authService = { register};
export default authService;
