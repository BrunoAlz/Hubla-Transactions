// import { useState } from 'react'
import Login from "./pages/Auth/Login";
import Register from "./pages/Auth/Register";
import Home from "./pages/Home/Home";
import { BrowserRouter, Routes, Route } from "react-router-dom";
// TOASTS
import { ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";


import './App.css'

function App() {

  return (
    <>
      <div className="App">
        <BrowserRouter>
          <Routes>
            <Route path={"/"} element={<Home />} />
            <Route path={"/login"} element={<Login />} />
            <Route path={"/register"} element={<Register />} />
          </Routes>
          <ToastContainer theme="dark" />
        </BrowserRouter>
      </div>
    </>
  );
}

export default App
