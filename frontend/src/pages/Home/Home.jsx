import Layout from "../Layout";
import { fileUpload, reset } from "../../slices/contracts/contractsSlice";
import { useState, useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { useNavigate } from "react-router-dom";
import logo from "../../assets/navLogo.svg";
import { toast } from "react-toastify";

const Home = () => {
  const [upload, setUpload] = useState(null);

  const dispatch = useDispatch();
  const navigate = useNavigate();

  const { isLoading, isError, isSuccess, message } = useSelector(
    (state) => state.contracts
  );

  const handleFile = (e) => {
    setUpload(e.target.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const formData = new FormData();
    formData.append("upload", upload);
    dispatch(fileUpload(formData));
  };

  useEffect(() => {
    if (isSuccess) {
      navigate("/contracts");
      toast.success(message);
    }
    if (isError) {
      toast.error(message);
    }
  }, [isSuccess, isError, isLoading, navigate]);

  return (
    <div>
      <Layout />
      <div className="container-fluid">
        <div className="row">
          <main className="col-md-9 ms-sm-auto col-lg-10 px-md-4">
            <div className="container mt-5 mb-">
              <form onSubmit={handleSubmit}>
                <input
                  className="form-control "
                  type="file"
                  accept=".txt"
                  onChange={handleFile}
                />
                <div>
                  <button className="btn btn-success btn-md mt-3">
                    Submit
                  </button>
                </div>
              </form>
            </div>
            {isLoading && "ENVIADAZZZZZZZZZZZZZZZZZZZZZZZZZZZZZO!"}
            <div className="container mt-5">
              <div className="row gx-lg-5 align-items-center">
                <div className="col-lg-6 mb-5 mb-lg-0">
                  <img
                    className="img-fluid hubla-login"
                    src={logo}
                    alt="Hubla Logo"
                  />
                  <h1 className="display-3 fw-bold ls-tight">
                    The best offer <br />
                    <span className="text-primary">
                      for your <span className="">.</span>
                      <span className="">T</span>
                      <span className="ms-4">x</span>
                      <span className="ms-4">t</span>
                    </span>
                  </h1>
                </div>
              </div>
            </div>
          </main>
        </div>
      </div>
    </div>
  );
};

export default Home;
