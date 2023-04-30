import { fileUpload, reset } from "../slices/contracts/contractsSlice";
import { useState, useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { toast } from "react-toastify";

const ContractForm = () => {
  const [upload, setUpload] = useState(null);
  
  const dispatch = useDispatch();

  const { user, isLoading, isError, isSuccess, message } = useSelector(
    (state) => state.contracts
  );

  useEffect(() => {
    if (isError) {
      toast.error(message)
    }
    if (isSuccess){
      toast.success(message.success)
    }

    dispatch(reset());
  }, [isError, isSuccess, message, user,  dispatch]);

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
      <div className="row">
        <div className="col-6">
          <input
            className="form-control "
            type="file"
            accept=".txt"
            onChange={handleFile}
          />
        </div>
        <div className="col-6">
          <button className="btn btn-success btn-sm">Submit</button>
        </div>
      </div>
      {isLoading && "ENVIADO!"}
    </form>
  );
};

export default ContractForm;
