import { useState, useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { Link, useNavigate } from "react-router-dom";
import { toast } from "react-toastify";
import { FaUser, FaLock } from "react-icons/fa";
import "../css/register.css";
import { login, reset } from "../features/auth/authSlice";

const Login = () => {
  const navigate = useNavigate();
  const dispatch = useDispatch();
  const [formData, setFormData] = useState({
    email: "",
    password: "",
  });

  const { isLoading, isError, user, msg } = useSelector((state) => state.auth);

  useEffect(() => {
    if (isError) {
      toast.error(msg);
    }
    if (user) {
      toast.success("success");
      navigate("/");
    }
    dispatch(reset());
  }, [isLoading, isError, user, msg, dispatch, navigate]);

  const { email, password } = formData;

  const handleChange = (e) => {
    const { name, value } = e.target;

    setFormData({
      ...formData,
      [name]: value,
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    if (!email || !password) {
      toast.error("All fields are required");
    } else {
      dispatch(login(formData));
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
          <h2>Login</h2>

          <div className="input-wrapper">
            <FaUser className="icon" />
            <input
              placeholder="Email"
              type="email"
              name="email"
              value={email}
              onChange={handleChange}
              className="input-field"
            />
          </div>

          <div className="input-wrapper">
            <FaLock className="icon" />
            <input
              placeholder="Password"
              type="password"
              name="password"
              value={password}
              onChange={handleChange}
              className="input-field"
            />
          </div>

          <button>Login</button>
        </form>
        <p>
          Doesn&apos;t have an account? <Link to="/signup">Sign Up</Link>
        </p>
      </div>
    </div>
  );
};

export default Login;
