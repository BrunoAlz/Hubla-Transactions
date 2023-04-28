import "./Auth.css";
import logo from "../../assets/navLogo.svg";

import { useState, useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { Link, useNavigate } from "react-router-dom";
import { toast } from "react-toastify";
import { login, reset } from "../../slices/auth/authSlice";

const Login = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const navigate = useNavigate();
  const dispatch = useDispatch();

  const { user, isLoading, isError, isSuccess, message } = useSelector(
    (state) => state.auth
  );

  useEffect(() => {
    if (isError) {
      toast.error(message)
    }
    if (isSuccess) {
      navigate("/");
      toast.success("Welcome to Hubla Transactions!");
    }

    dispatch(reset());
  }, [isError, isSuccess, message, user, navigate, dispatch]);

  const handlerSubmit = (e) => {
    e.preventDefault();

    const userData = {
      email,
      password,
    };

    dispatch(login(userData));
  };

  return (
    <div className="grey-bg px-4 mt-5 py-5 px-md-5 text-center text-lg-start">
      <div className="container mt-5">
        <div className="row gx-lg-5 align-items-center">
          <div className="col-lg-6 mb-5 mb-lg-0">
            <img
              className="img-fluid hubla-login"
              src={logo}
              alt="Logo do Breaking News"
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

          <div className="col-lg-6 mb-5 mb-lg-0">
            <div
              className={` ${
                isError ? "border border-3 border-danger" : ""
              } card login-card shadow`}
            >
              <div className="card-body py-5 px-md-5">
                <form onSubmit={handlerSubmit}>
                  <p className="text-center fs-2 fw-bold">Login</p>
                  <div className="row mt-5">
                    <div className="form-outline fs-5 mb-2  fw-semi-bold">
                      <p>Email</p>
                      <input
                        type="email"
                        className="form-control"
                        onChange={(e) => setEmail(e.target.value)}
                        value={email}
                        required
                      />
                    </div>
                    <div className="col-md-12 mb-4 mt-3">
                      <div className="form-outline fs-5  ">
                        <p>Password</p>
                        <input
                          type="password"
                          className="form-control"
                          onChange={(e) => setPassword(e.target.value)}
                          value={password}
                          required
                        />
                      </div>
                    </div>
                    {!isLoading ? (
                      <button
                        type="submit"
                        className="btn btn-primary btn-block mb-4 shadow"
                      >
                        <span className="fs-5">Sign in</span>
                      </button>
                    ) : (
                      <button
                        className="btn btn-secondary fs-5"
                        type="button"
                        disabled
                      >
                        <span
                          className="spinner-border spinner-border-sm mx-2"
                          role="status"
                        ></span>
                        Authenticating..
                      </button>
                    )}
                  </div>
                </form>
                <span>
                  Não é cadastrado? <Link to="/register">Sing Up</Link>
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Login;
