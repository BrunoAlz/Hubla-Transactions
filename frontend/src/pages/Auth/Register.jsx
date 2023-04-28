import React from 'react'
import "./Auth.css";


const Register = () => {
  return (
    <div>
      <form className="form-auth">
        {/* <img className="mb-4" src="/docs/5.3/assets/brand/bootstrap-logo.svg" alt="" width="72" height="57"> */}
        <h1 className="h3 mb-3 fw-normal">Register</h1>

        <div className="form-floating">
          <input
            type="email"
            className="form-control"
            id="floatingInput"
            placeholder="name@example.com"
          />
          <label for="floatingInput">Email address</label>
        </div>
        <div className="form-floating">
          <input
            type="password"
            className="form-control"
            id="floatingPassword"
            placeholder="Password"
          />
          <label for="floatingPassword">Password</label>
        </div>

        <div className="checkbox mb-3">
          <label>
            <input type="checkbox" value="remember-me" /> Remember me
          </label>
        </div>
        <button className="w-100 btn btn-lg btn-primary" type="submit">
          Register
        </button>
        <p className="mt-5 mb-3 text-body-secondary">© 2017–2023</p>
      </form>
    </div>
  );
};

export default Register;