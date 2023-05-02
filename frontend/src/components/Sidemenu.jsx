import { useSelector } from "react-redux";
import { NavLink } from "react-router-dom";

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
            <NavLink to="/contracts" className="nav-link">
              <span data-feather="file" className="align-text-bottom"></span>
              Contracts <i className="bi bi-file-text"></i>
            </NavLink>
          </li>
        </ul>
      </div>
    </nav>

    
  );
};

export default Sidemenu;
