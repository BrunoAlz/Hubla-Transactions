import React from "react";
import { useDispatch } from "react-redux";
import { useNavigate } from "react-router-dom";
import { logout, reset } from "../slices/auth/authSlice";
import { NavLink } from "react-router-dom";


const Navbar = () => {

  const navigate = useNavigate();
  const dispatch = useDispatch();

  const handleLogout = () => {
    dispatch(logout());
    dispatch(reset());

    navigate("/login");
  };

  return (
    <header className="navbar navbar-dark sticky-top bg-dark flex-md-nowrap p-0 shadow">
      <NavLink to="/" className=" text-center navbar-brand col-md-3 col-lg-2 fs-4">
        Hubla Transactions <i className="bi bi-filetype-txt"></i>
      </NavLink>

      <input
        className="form-control form-control-dark w-100 rounded-0 border-0"
        type="text"
        placeholder="Search"
        aria-label="Search"
      />

      <div className="navbar-nav">
        <div className="nav-item text-nowrap">
          <button className="nav-link px-3 fs-4" onClick={handleLogout}>
            Sign out
          </button>
        </div>
      </div>
    </header>
  );
};

export default Navbar;
