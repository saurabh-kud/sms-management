import React, { useState } from "react";
import "../css/card.css";
import axios from "axios";
import { useSelector } from "react-redux";
import { toast } from "react-toastify";
import { FaCheckCircle, FaTimesCircle } from "react-icons/fa";
const BASE_URL = import.meta.env.VITE_APP_BASE_URL;

const SessionCard = ({ con }) => {
  const { user } = useSelector((state) => state.auth);
  const [assignmentStatus, setAssignmentStatus] = useState(con?.status);

  const handleStart = async () => {
    const config = {
      headers: {
        authorization: `Bearer ${user?.token}`,
      },
    };
    try {
      const payload = { country: con.country, operator: con.operator };
      const data = await axios.post(
        `${BASE_URL}/session/start`,
        payload,
        config
      );
      if (data) {
        toast.success("Session Started");
        setAssignmentStatus("Active");
      }
    } catch (error) {
      toast.error("Something went wrong");
    }
  };

  const handleStop = async () => {
    const config = {
      headers: {
        authorization: `Bearer ${user?.token}`,
      },
    };
    console.log(config);
    try {
      const payload = { country: con.country, operator: con.operator };

      const data = await axios.post(
        `${BASE_URL}/session/stop`,
        payload,
        config
      );
      if (data) {
        toast.success("Session Stopeed");
        setAssignmentStatus("Inactive");
      }
    } catch (error) {
      console.log(error);
      toast.error(error?.response?.data?.message);
    }
  };

  const handleRestart = async () => {
    const config = {
      headers: {
        authorization: `Bearer ${user?.token}`,
      },
    };
    try {
      const payload = { country: con.country, operator: con.operator };

      const data = await axios.post(
        `${BASE_URL}/session/restart`,
        payload,
        config
      );
      if (data) {
        toast.success("Session restarted");
        setAssignmentStatus("Active");
      }
    } catch (error) {
      toast.error("Something went wrong");
    }
  };

  return (
    <div className="card">
      <h3>Session name: {`${con?.country}_${con.operator}`}</h3>
      <h3>Country: {con?.country}</h3>
      <small>Operator: {con?.operator}</small>
      <h5>Status: {assignmentStatus}</h5>
      <h5>Priority: {con?.priority}</h5>

      <div>
        {assignmentStatus === "Inactive" ? (
          <div className="flex">
            <button className="accept" onClick={handleStart}>
              <FaCheckCircle /> Start
            </button>
          </div>
        ) : (
          <div className="flex">
            <button className="reject" onClick={handleStop}>
              <FaTimesCircle /> Stop
            </button>
            <button className="accept" onClick={handleRestart}>
              <FaCheckCircle /> Restart
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default SessionCard;
