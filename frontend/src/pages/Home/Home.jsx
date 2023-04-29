import React from "react";
import Navbar from "../../../../frontend/src/components/Navbar";
import Sidemenu from "../../../../frontend/src/components/Sidemenu";
import Body from "../../components/Body";

const Home = () => {

  return (
    <div>
      <Navbar />
      <Sidemenu />
      <Body/>
    </div>
  );
};

export default Home;
