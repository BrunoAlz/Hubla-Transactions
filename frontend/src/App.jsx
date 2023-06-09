// import { useState } from 'react'
import Login from "./pages/Auth/Login";
import Register from "./pages/Auth/Register";
import Home from "./pages/Home/Home";
import NotFound404 from "./pages/notFound404";
import { useSelector } from "react-redux";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

import "./App.css";
import Contracts from "./pages/Contracts/Contracts";
import ContractsTransactions from "./pages/Contracts/ContractsTransactions";

function App() {
  const { user } = useSelector((state) => state.auth);

  return (
    <>
      <div className="App">
        <BrowserRouter>
          <Routes>
            <Route
              path={"/"}
              element={user ? <Home /> : <Navigate to="/login" />}
            />
            <Route
              path={"/contracts"}
              element={user ? <Contracts /> : <Navigate to="/login" />}
            />
            <Route
              path={"/contracts/:contract_id"}
              element={
                user ? <ContractsTransactions /> : <Navigate to="/login" />
              }
            />
            <Route path={"/login"} element={<Login />} />
            <Route path={"/register"} element={<Register />} />
            <Route path="*" element={<NotFound404 />} />
          </Routes>
          <ToastContainer theme="dark" />
        </BrowserRouter>
      </div>
    </>
  );
}

export default App;
