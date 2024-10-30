import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useDispatch, useSelector } from "react-redux";
import { FiUpload } from "react-icons/fi";

import SessionCard from "../Components/SessionCard";
import "../css/register.css";
import "../css/dashboard.css";
import axios from "axios";
import DataDisplay from "../Components/DataDisplay";
const BASE_URL = import.meta.env.VITE_APP_BASE_URL;

const Dashboard = () => {
  const navigate = useNavigate();
  const dispatch = useDispatch();
  const { user } = useSelector((state) => state.auth);

  const [isLoading, setIsLoading] = useState(false);
  const [sessions, setSessions] = useState([]);

  useEffect(() => {
    if (!user) {
      navigate("/login");
      return;
    }
    const fetchSessions = async () => {
      setIsLoading(true);
      const config = {
        headers: {
          authorization: `Bearer ${user?.token}`,
        },
      };

      try {
        const res = await axios.get(`${BASE_URL + "/sessions"}`, config);

        if (res) {
          setSessions(res.data.data);
          setIsLoading(false);
        }
      } catch (error) {
        setIsLoading(false);
      }
    };
    fetchSessions();
  }, [user, dispatch, navigate]);

  return (
    <div className="con">
      <section className="main">
        <h1>Welcome, {user && user.name}</h1>
        <button
          className="add"
          onClick={() => {
            navigate("/country");
          }}
        >
          {/* <FiUpload className="upload-icon" /> */}
          Country Operator pair
        </button>
      </section>

      <section className="show_contact">{<DataDisplay />}</section>
      <section className="show_contact">
        <h1 className="h1">Session List</h1>

        {sessions.length > 0 ? (
          <div className="contact">
            {sessions.map((con) => {
              return <SessionCard key={con._id} con={con} />;
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
                No Session available at this moment.
              </h1>
            )}
          </div>
        )}
      </section>
    </div>
  );
};

export default Dashboard;
