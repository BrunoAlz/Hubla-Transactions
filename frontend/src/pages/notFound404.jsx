import logo from "../assets/appLogo.png";
import { Link } from "react-router-dom";

const notFound404 = () => {
  return (
    <div className="grey-bg  px-4 mt-5 py-5 px-md-5 text-center text-lg-start">
      <div className="container back-img mt-5 ">
        <div className="row gx-lg-5 align-items-center">
          <div className="col-lg-6 mb-5 mb-lg-0">
            <p className="not-found text-center fw-bold ls-tight m-0 p-0">
              4<span className="text-green">0</span>4
            </p>
          </div>

          <div className="col-lg-6 text-center mb-5 mb-lg-0">
            <img
              className="img-fluid hubla-login square-logo"
              src={logo}
              alt="Hubla Transactions"
            />
            <h1 className="display-3 fw-bold ls-tight">
              Not Found<span className="text-green">.</span>
            </h1>
            <span className="fw-bold">Hubla Transactions</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default notFound404;
