import { useEffect, useState } from "react";
import { useSelector, useDispatch } from "react-redux";
import { Link, useNavigate } from "react-router-dom";
import { toast } from "react-toastify";
import "../css/register.css";
import { register, reset, logout } from "../features/auth/authSlice";
import { FaUser, FaEnvelope, FaLock } from "react-icons/fa";

const Register = () => {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const { isLoading, isError, isSuccess, user, msg } = useSelector(
    (state) => state.auth
  );
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    password: "",
  });

  const { name, email, password } = formData;

  useEffect(() => {
    if (isError) {
      toast.error(msg);
    }

    if (user) {
      toast.success("Success");
      navigate("/");
    }
    dispatch(reset());
  }, [isError, user, isSuccess, msg, dispatch, navigate]);

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData({
      ...formData,
      [name]: type === "checkbox" ? checked : value,
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!name || !email || !password) {
      toast.error("All fields are required");
    } else {
      const userData = { name, email, password };

      dispatch(register(userData));
    }
  };

  if (isLoading) {
    return (
      <div
        style={{
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          height: "100vh",
          flexDirection: "column",
        }}
      >
        <h1 style={{ fontWeight: 500 }}>loading....</h1>
      </div>
    );
  }

  return (
    <div className="container1">
      <div className="innerform">
        <form onSubmit={handleSubmit}>
          <h2>Register</h2>

          <div className="input-wrapper">
            <FaUser className="icon" />
            <input
              placeholder="Enter your name"
              type="text"
              name="name"
              value={name}
              onChange={handleChange}
            />
          </div>

          <div className="input-wrapper">
            <FaEnvelope className="icon" />
            <input
              placeholder="Enter your email"
              type="email"
              name="email"
              value={email}
              onChange={handleChange}
            />
          </div>

          <div className="input-wrapper">
            <FaLock className="icon" />
            <input
              placeholder="Enter your password"
              type="password"
              name="password"
              value={password}
              onChange={handleChange}
            />
          </div>

          <button type="submit">Register</button>
        </form>
        <p>
          Already have an account? <Link to="/login">Login</Link>
        </p>
      </div>
    </div>
  );
};

export default Register;
