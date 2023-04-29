import React from 'react'
import { useSelector } from "react-redux";
import ContractForm from './ContractForm';


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
          <li className="nav-item fs-4  mx-3">
            <a className="nav-link active" aria-current="page" href="#">
              <span data-feather="home" className="align-text-bottom"></span>
              Dashboard <i className="bi bi-pie-chart"></i>
            </a>
          </li>
          <li className="nav-item fs-4  mx-3">
            <a className="nav-link" href="#">
              <span data-feather="file" className="align-text-bottom"></span>
              Contracts <i className="bi bi-file-text"></i>
            </a>
          </li>

          <ContractForm/>

        </ul>
      </div>
    </nav>
  );
}

export default Sidemenu