import React, { useEffect, useState } from "react";
import "./../css/addassignment.css";
import axios from "axios";
import { toast } from "react-toastify";
import { useSelector } from "react-redux";
import { useNavigate } from "react-router-dom";
import { FiUpload } from "react-icons/fi";
import { IoArrowBack } from "react-icons/io5";
const BASE_URL = import.meta.env.VITE_APP_BASE_URL;

function AddAssignment() {
  const [country, setCountry] = useState("");
  const [operator, setOperator] = useState("");
  const [prioriry, setPriority] = useState(null);
  const { user } = useSelector((state) => state.auth);
  const navigate = useNavigate();
  const [adminList, setAdminList] = useState([]);

  useEffect(() => {
    if (!user) {
      navigate("/login");
    }

    const fetchAllAdmin = async () => {
      const config = {
        headers: {
          authorization: `Bearer ${user?.token}`,
        },
      };
      try {
        const res = await axios.get(`${BASE_URL + "/admins"}`, config);
        if (res?.data?.data) {
          setAdminList(res.data.data);
        }
      } catch (error) {
        toast.error("Failed to fetch admins");
      }
    };

    // fetchAllAdmin();
  }, [user, navigate]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!country || !operator || !prioriry) {
      toast.error("All fields are mandatory");
      return;
    }
    const config = {
      headers: {
        authorization: `Bearer ${user?.token}`,
      },
    };

    try {
      const addedFlight = await axios.post(
        `${BASE_URL + "/country/create"}`,
        {
          country,
          operator,
          prioriry,
        },
        config
      );

      setCountry("");
      setOperator("");
      setPriority(null);

      if (addedFlight) {
        toast.success("Country operator added successfully");
        navigate("/country");
      }
    } catch (error) {
      toast.error("Something went wrong");
    }
  };

  return (
    <div className="add-flight-container">
      <h2>Add Country Opeerator pair</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Country</label>
          <input
            type="text"
            placeholder="Enter country name"
            value={country}
            onChange={(e) => setCountry(e.target.value)}
            required
          />
        </div>
        <div className="form-group">
          <label>Operator</label>
          <input
            type="text"
            placeholder="Enter Operator name"
            value={operator}
            onChange={(e) => setOperator(e.target.value)}
            required
          />
        </div>
        <div className="form-group">
          <label>Priority</label>
          <select
            value={prioriry || ""}
            onChange={(e) => setPriority(e.target.value)}
            required
          >
            <option value="" disabled>
              Select prioriry
            </option>
            <option value={"High"}>High</option>
            <option value={"Low"}>Low</option>
            {/* {adminList.map((admin) => (
              <option key={admin._id} value={admin._id}>
                {admin.name}
              </option>
            ))} */}
          </select>
        </div>
        <div className="button-group">
          <button className="submit-btn" type="submit">
            <FiUpload /> Add
          </button>
          <button
            className="cancel-btn"
            onClick={() => {
              navigate("/");
            }}
            type="button"
          >
            <IoArrowBack />
          </button>
        </div>
      </form>
    </div>
  );
}

export default AddAssignment;
