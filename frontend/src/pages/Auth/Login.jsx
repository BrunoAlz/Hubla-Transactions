import "./Auth.css";
import logo from "../../assets/navLogo.svg";
import { Link, useNavigate } from "react-router-dom";

const Login = () => {
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
            <div className="card login-card shadow">
              <div className="card-body py-5 px-md-5">
                <form>
                  <p className="text-center fs-2 fw-bold">Login</p>
                  <div className="row mt-5">
                    <div className="form-outline fs-5 mb-2  fw-semi-bold">
                      <p>Email</p>
                      <input type="email" className="form-control" />
                    </div>

                    <div className="col-md-12 mb-4 mt-3">
                      <div className="form-outline fs-5  ">
                        <p>Password</p>
                        <input type="password" className="form-control" />
                      </div>
                    </div>

                    <button
                      type="submit"
                      className="btn btn-primary btn-block mb-4 shadow"
                    >
                      <span className="fs-5">Sign in</span>
                    </button>
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
