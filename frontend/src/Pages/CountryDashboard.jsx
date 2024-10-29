import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useDispatch, useSelector } from "react-redux";
import { FiUpload } from "react-icons/fi";

import "../css/register.css";
import "../css/dashboard.css";
import axios from "axios";
import CountryCard from "../Components/CountryCard";
import { toast } from "react-toastify";

const BASE_URL = import.meta.env.VITE_APP_BASE_URL;

const CountryDashboard = () => {
  const navigate = useNavigate();
  const dispatch = useDispatch();
  const { user } = useSelector((state) => state.auth);

  const [isLoading, setIsLoading] = useState(false);
  const [country, setCountry] = useState([]);
  const [isRefreshed, setIsrefreshed] = useState(false);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [formData, setFormData] = useState({
    country: "",
    operator: "",
    priority: "", // Default to medium priority
  });

  useEffect(() => {
    if (!user) {
      navigate("/login");
      return;
    }
    const fetchCountry = async () => {
      setIsLoading(true);
      const config = {
        headers: {
          authorization: `Bearer ${user?.token}`,
        },
      };

      try {
        const res = await axios.get(`${BASE_URL + "/country"}`, config);

        if (res) {
          setCountry(res.data.data);
          setIsLoading(false);
        }
      } catch (error) {
        setIsloading(false);
      }
    };
    fetchCountry();
  }, [user, dispatch, navigate, isRefreshed]);

  const changeStatus = () => {
    setIsrefreshed(!isRefreshed);
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleAddCountry = async () => {
    if (!formData.country || !formData.operator || !formData.priority) {
      toast.error("Please fill in all fields");
      return;
    }

    const config = {
      headers: {
        authorization: `Bearer ${user?.token}`,
      },
    };

    try {
      const data = await axios.post(
        `${BASE_URL}/country/create`,
        formData,
        config
      );
      if (data) {
        toast.success("New Country Operator pair added successfully");
        setIsModalOpen(false);
        setFormData({
          country: "",
          operator: "",
          priority: "",
        });
        setIsrefreshed(!isRefreshed);
      }
    } catch (error) {
      console.log(error);
      toast.error(
        error?.response?.data?.message || "Failed to add country operator pair"
      );
    }
  };
  return (
    <div className="con">
      <section className="main">
        <h1>Welcome, {user && user.name}</h1>
        <button
          className="add"
          onClick={() => {
            navigate("/");
          }}
        >
          {/* <FiUpload className="upload-icon" /> */}
          Session list
        </button>
      </section>

      <section className="show_contact">
        <h1 className="h1">Country Operator List</h1>

        <button className="add" onClick={() => setIsModalOpen(true)}>
          <FiUpload className="upload-icon" />
          Add new Operator pair
        </button>
        {/* </section> */}

        {country.length > 0 ? (
          <div className="contact">
            {country.map((con) => {
              return (
                <CountryCard
                  key={con._id}
                  con={con}
                  changeStatus={changeStatus}
                />
              );
            })}
          </div>
        ) : (
          <div
            style={{
              display: "flex",
              justifyContent: "center",
              alignItems: "center",
              height: "45vh",
              flexDirection: "column",
            }}
          >
            {isLoading ? (
              <h1 style={{ fontWeight: 500 }}>loading.. please wait</h1>
            ) : (
              <h1 style={{ fontWeight: 500 }}>
                No Country available at this moment.
              </h1>
            )}
          </div>
        )}
      </section>
      {isModalOpen && (
        <div className="modal-overlay">
          <div className="modal">
            <h2>Add New Country Operator</h2>
            <div className="modal-content">
              <div className="form-group">
                <label>Country</label>
                <input
                  type="text"
                  name="country"
                  value={formData.country}
                  onChange={handleInputChange}
                  placeholder="Enter country name"
                />
              </div>
              <div className="form-group">
                <label>Operator</label>
                <input
                  type="text"
                  name="operator"
                  value={formData.operator}
                  onChange={handleInputChange}
                  placeholder="Enter operator name"
                />
              </div>
              <div className="form-group">
                <label>Priority</label>
                <select
                  value={formData.priority || ""}
                  name="priority"
                  onChange={handleInputChange}
                  required
                >
                  <option value="" disabled>
                    Select prioriry
                  </option>
                  <option value={"High"}>High</option>
                  <option value={"Low"}>Low</option>
                </select>
              </div>
            </div>
            <div className="modal-actions">
              <button
                className="cancel-btn"
                onClick={() => {
                  setIsModalOpen(false);
                  setFormData({
                    country: "",
                    operator: "",
                    priority: "",
                  });
                }}
              >
                Cancel
              </button>
              <button className="save-btn" onClick={handleAddCountry}>
                Add Country
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default CountryDashboard;
