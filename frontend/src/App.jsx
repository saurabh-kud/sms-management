import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import React, { useEffect } from "react";

import Header from "./Components/Header";
import Dashboard from "./Pages/Dashboard";
import CountryDashboard from "./Pages/CountryDashboard";
import Register from "./Pages/Register";
import Login from "./Pages/Login";
import { ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

import { useSelector } from "react-redux";
const BASE_URL = import.meta.env.VITE_APP_BASE_URL;
import { toast } from "react-toastify";
import axios from "axios";

function App() {
  const { user } = useSelector((state) => state.auth);

  useEffect(() => {
    const checkServerActive = async () => {
      const config = {
        headers: {
          authorization: `Bearer ${user?.accessToken}`,
        },
      };
      try {
        const res = await axios.get(`${BASE_URL}/docs`, config);
      } catch (error) {
        console.log(error);
        toast.error("Server might down try again! Please refresh..");
      }
    };

    checkServerActive();
  }, []);

  return (
    <>
      <Router>
        <Header />
        <Routes>
          <Route path="/" element={user ? <Dashboard /> : <Login />} />
          <Route
            path="/country"
            element={user ? <CountryDashboard /> : <Login />}
          />
          <Route path="/signup" element={<Register />} />
          <Route path="/login" element={<Login />} />
        </Routes>
      </Router>
      <ToastContainer />
    </>
  );
}

export default App;
