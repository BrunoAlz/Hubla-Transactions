import React from 'react'
import { useSelector } from "react-redux";


const Sidemenu = () => {
  const { user } = useSelector((state) => state.auth);

  return (
    <nav
      id="sidebarMenu"
      className="col-md-3 col-lg-2 d-md-block bg-body-tertiary sidebar collapse"
    >
      <div className="position-sticky pt-3 sidebar-sticky">
        <ul className="nav flex-column">
          <h4 className="m-3 text-center">
            Olá {user.first_name} {user.last_name}
          </h4>
          <li className="nav-item">
            <a className="nav-link active" aria-current="page" href="#">
              <span data-feather="home" className="align-text-bottom"></span>
              Dashboard
            </a>
          </li>
          <li className="nav-item">
            <a className="nav-link" href="#">
              <span data-feather="file" className="align-text-bottom"></span>
              Orders
            </a>
          </li>   
        </ul>
      </div>
    </nav>
  );
}

export default Sidemenu