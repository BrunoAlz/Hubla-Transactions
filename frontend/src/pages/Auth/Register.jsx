import "./Auth.css";
import logo from "../../assets/navLogo.svg";
// HOOKS
import { useState, useEffect } from "react";
// REDUX
import { useDispatch, useSelector } from "react-redux";
// ROUTERS
import { useNavigate } from "react-router-dom";
// REDUCERS
import { register, reset } from "../../slices/auth/authSlice";
import { toast } from "react-toastify";

const Register = () => {
  const [first_name, setFirstName] = useState("");
  const [last_name, setLastName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [password_confirm, setPasswordConfirm] = useState("");

  const navigate = useNavigate();
  const dispatch = useDispatch();

  const { user, isLoading, isError, isSuccess, message } = useSelector(
    (state) => state.auth
  );

  useEffect(() => {
    if (isError) {
      console.log(message);
      Object.values(message).forEach((errorArray) => {
        errorArray.forEach((errorMessage) => {
          toast.error(errorMessage);
        });
      });
    }
    // if (isSuccess) {
    //   navigate("/");     
    // }

    dispatch(reset());
  }, [isError, isSuccess, message, user, navigate, dispatch]);

  const handlerSubmit = (e) => {
    e.preventDefault();

    if (!password) {
      toast.error("As senhas devem ser iguais");
    } else {
      const userData = {
        first_name,
        last_name,
        email,
        password,
        password_confirm,
      };
      dispatch(register(userData));
    }
  };

  return (
    <div className="grey-bg px-4 mt-5 py-5 px-md-5 text-center text-lg-start">
      <div className="container mt-5">
        <div className="row gx-lg-5 align-items-center">
          <div className="col-lg-6 mb-5 mb-lg-0">
            <div className="card">
              <div className="card-body py-5 px-md-5 shadow">
                <p className="text-center fs-2 fw-bold">Register</p>
                <form onSubmit={handlerSubmit}>
                  <div className="row">
                    <div className="col-md-6 mb-4">
                      <div className="form-outline">
                        <label className="form-label fs-5 fw-semi-bold">
                          First name
                        </label>
                        <input
                          type="text"
                          required
                          className="form-control"
                          onChange={(e) => setFirstName(e.target.value)}
                          value={first_name || ""}
                        />
                      </div>
                    </div>
                    <div className="col-md-6 mb-4">
                      <div className="form-outline">
                        <label className="form-label fs-5 fw-semi-bold">
                          Last name
                        </label>
                        <input
                          required
                          type="text"
                          className="form-control"
                          onChange={(e) => setLastName(e.target.value)}
                          value={last_name || ""}
                        />
                      </div>
                    </div>
                  </div>

                  <div className="form-outline mb-4">
                    <label className="form-label fs-5 fw-semi-bold">
                      Email
                    </label>
                    <input
                      required
                      type="email"
                      className="form-control"
                      onChange={(e) => setEmail(e.target.value)}
                      value={email || ""}
                    />
                  </div>
                  <div className="row">
                    <div className="col-md-6 mb-4">
                      <div className="form-outline">
                        <label className="form-label fs-5 fw-semi-bold">
                          Password
                        </label>
                        <input
                          required
                          type="password"
                          className="form-control"
                          onChange={(e) => setPassword(e.target.value)}
                          value={password || ""}
                        />
                      </div>
                    </div>
                    <div className="col-md-6 mb-4">
                      <div className="form-outline">
                        <label className="form-label fs-5 fw-semi-bold">
                          Confirm Password
                        </label>
                        <input
                          required
                          type="password"
                          className="form-control"
                          onChange={(e) => setPasswordConfirm(e.target.value)}
                          value={password_confirm || ""}
                        />
                      </div>
                    </div>
                  </div>

                  <div className="row">
                    {isLoading && "CARREGANDO"}
                    <button
                      type="submit"
                      className="btn btn-primary btn-block shadow mb-4"
                    >
                      <span className="fs-5">Sign up</span>
                    </button>
                  </div>
                </form>
              </div>
            </div>
          </div>

          <div className="col-lg-6 mb-lg-0">
            <img
              className="hubla-register"
              src={logo}
              alt="Logo do Breaking News"
            />
            <h1 className="display-5 mb-4 fw-bold ls-tight">Transactions</h1>
            <p className="text-primary display-4">
              Your <span className="fw-bold">.</span>TXT will now work for you.
            </p>
            <p className="login-text pt-3 mt-4">
              With our data extraction software, turning your{" "}
              <span className="fw-bold">.</span>TXT into cash is easier than
              printing cash at home. Don't waste any more time trying to
              decipher your financial data manually. Let us take care of it for
              you and unlock the full potential of your business.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Register;
