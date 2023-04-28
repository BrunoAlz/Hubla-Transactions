import React from "react";
import Navbar from "../../../../frontend/src/components/Navbar";
import Sidemenu from "../../../../frontend/src/components/Sidemenu";

const Home = () => {

  return (
    <div>
      <Navbar />
      <div className="container-fluid">
        <div className="row">
          <Sidemenu />
          <main className="col-md-9 ms-sm-auto col-lg-10 px-md-4">
            
          </main>
        </div>
      </div>
    </div>
  );
};

export default Home;
