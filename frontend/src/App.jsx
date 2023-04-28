// import { useState } from 'react'
import Login from "./pages/Auth/Login";
import Register from "./pages/Auth/Register";
import Home from "./pages/Home/Home";
import { useSelector } from "react-redux";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

import "./App.css";

function App() {
  const { user } = useSelector((state) => state.auth);

  return (
    <>
      <div className="App">
        <BrowserRouter>
          <Routes>
            <Route
              path={"/"}
              element={ user ? <Home /> : <Navigate to="/login" />}
            />
            <Route path={"/login"} element={<Login />} />
            <Route path={"/register"} element={<Register />} />
          </Routes>
          <ToastContainer theme="dark" />
        </BrowserRouter>
      </div>
    </>
  );
}

export default App;
