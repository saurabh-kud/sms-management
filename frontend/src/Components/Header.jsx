import React from "react";
import { Link } from "react-router-dom";
import "../css/header.css";
import { FaSignInAlt, FaSignOutAlt, FaUser } from "react-icons/fa";
import { useDispatch, useSelector } from "react-redux";
import { logout } from "../features/auth/authSlice";
import { FaTelegramPlane } from "react-icons/fa";
const Header = () => {
  const dispatch = useDispatch();
  const { user } = useSelector((state) => state.auth);

  return (
    <>
      <div className="container">
        <div className="logo">
          <Link to="/">
            <FaTelegramPlane />
            Sms Management
          </Link>
        </div>
        {/* <div className="search">
          <input className="searchinput" placeholder="Search..."></input>
        </div> */}
        <div className="list">
          <ul>
            {user ? (
              <li>
                <div
                  className="logout"
                  onClick={() => {
                    dispatch(logout());
                  }}
                >
                  <FaSignOutAlt /> <span>Logout</span>
                </div>
              </li>
            ) : (
              <>
                <li>
                  <FaUser />
                  <Link to="/signup">Register</Link>
                </li>
                <li>
                  <FaSignInAlt />
                  <Link to="/login">Login</Link>
                </li>
              </>
            )}
          </ul>
        </div>
      </div>
    </>
  );
};

export default Header;
