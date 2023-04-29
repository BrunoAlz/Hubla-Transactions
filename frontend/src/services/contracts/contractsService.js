import axios from "axios";

const API_ENDPOINT = "http://127.0.0.1:8000/api/";

const contractUpload = async (txtFile) => {
  const user = JSON.parse(localStorage.getItem("user"));
  try {
    const response = await axios.post(
      API_ENDPOINT + "transactions/contract/",
      txtFile,
      {
        headers: {
          "Content-Type": "multipart/form-data",
          Authorization: `Bearer ${user.token}`,
        },
      }
    );

    return response.data;
  } catch (error) {
    throw new Error(error.response.data.detail);
  }
};

const contractsService = { contractUpload };
export default contractsService;
