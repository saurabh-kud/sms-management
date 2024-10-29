import React, { useState } from "react";
import { useSelector } from "react-redux";
import axios from "axios";
import { toast } from "react-toastify";
import { FaCheckCircle, FaTimesCircle } from "react-icons/fa";
import "../css/card.css";

const BASE_URL = import.meta.env.VITE_APP_BASE_URL;

const CountryCard = ({ con, changeStatus }) => {
  const { user } = useSelector((state) => state.auth);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [formData, setFormData] = useState({
    country: con.country,
    operator: con.operator,
    priority: con.priority,
  });

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleUpdate = async () => {
    const config = {
      headers: {
        authorization: `Bearer ${user?.token}`,
      },
    };
    try {
      const data = await axios.put(
        `${BASE_URL}/country/update`,
        formData,
        config
      );
      if (data) {
        toast.success("Country Operator pair Updated");
        setIsModalOpen(false);
        changeStatus();
      }
    } catch (error) {
      console.log(error);
      toast.error(error?.response?.data?.message);
    }
  };

  const handleDelete = async () => {
    const config = {
      headers: {
        authorization: `Bearer ${user?.token}`,
      },
    };
    try {
      const payload = { country: con.country, operator: con.operator };
      const data = await axios.post(
        `${BASE_URL}/country/delete`,
        payload,
        config
      );
      if (data) {
        changeStatus();
        toast.success("Country Operator pair deleted");
      }
    } catch (error) {
      console.log(error);
      toast.error(error?.response?.data?.message);
    }
  };

  return (
    <>
      <div className="card">
        <h3>Country: {con?.country}</h3>
        <small>Operator: {con?.operator}</small>
        <h5>Priority: {con?.priority}</h5>
        <div>
          <div className="flex">
            <button className="accept" onClick={() => setIsModalOpen(true)}>
              <FaCheckCircle /> Update
            </button>
            <button className="reject" onClick={handleDelete}>
              <FaTimesCircle /> Delete
            </button>
          </div>
        </div>
      </div>

      {isModalOpen && (
        <div className="modal-overlay">
          <div className="modal">
            <h2>Update Country Operator</h2>
            <div className="modal-content">
              <div className="form-group">
                <label>Country</label>
                <input
                  type="text"
                  name="country"
                  value={formData.country}
                  disabled
                  className="disabled-input"
                />
              </div>
              <div className="form-group">
                <label>Operator</label>
                <input
                  type="text"
                  name="operator"
                  value={formData.operator}
                  disabled
                  className="disabled-input"
                />
              </div>
              <div className="form-group">
                <label>Priority</label>
                <select
                  name="priority"
                  value={formData.priority}
                  onChange={handleInputChange}
                  className="priority-select"
                >
                  <option value={"High"}>High</option>
                  <option value={"Low"}>Low</option>
                  {/* {PRIORITY_OPTIONS.map((option) => (
                    <option key={option.value} value={option.value}>
                      {option.label}
                    </option>
                  ))} */}
                </select>
              </div>
            </div>
            <div className="modal-actions">
              <button
                className="cancel-btn"
                onClick={() => {
                  setIsModalOpen(false),
                    setFormData({
                      country: con.country,
                      operator: con.operator,
                      priority: con.priority,
                    });
                }}
              >
                Cancel
              </button>
              <button className="save-btn" onClick={handleUpdate}>
                Save Changes
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
};

export default CountryCard;
