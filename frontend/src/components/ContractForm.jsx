import { useState } from "react";
import { fileUpload } from "../slices/contracts/contractsSlice";
import {useDispatch } from "react-redux";


const ContractForm = () => {
  const [upload, setUpload] = useState(null);
  const dispatch = useDispatch();

  const handleFile = (e) => {
    setUpload(e.target.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const formData = new FormData();
    formData.append("upload", upload);

    dispatch(fileUpload(formData));
  };

  return (
    <form onSubmit={handleSubmit}>
      <input type="file" accept=".txt" onChange={handleFile} />
      <button type="submit">Enviar</button>
    </form>
  );
};

export default ContractForm;
