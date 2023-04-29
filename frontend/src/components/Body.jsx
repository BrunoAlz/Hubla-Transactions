import React from "react";
import Table from "./Table";

const Body = () => {



  return (
    <div>
      <div className="container-fluid">
        <div className="row">
          <main className="col-md-9 ms-sm-auto col-lg-10 px-md-4">
            <Table/>
          </main>
        </div>
      </div>
    </div>
  );
};

export default Body;
