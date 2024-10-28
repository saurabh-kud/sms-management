import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useDispatch, useSelector } from "react-redux";
import AssignmentCard from "../Components/AssignmentCard";
import "../css/register.css";
import "../css/dashboard.css";
import axios from "axios";
import { toast } from "react-toastify";
const BASE_URL = import.meta.env.VITE_APP_BASE_URL;

const DashboardAdmin = () => {
  const navigate = useNavigate();
  const dispatch = useDispatch();
  const { user } = useSelector((state) => state.auth);
  const [isLoading, setIsLoading] = useState(false);

  const [userAssignment, setUserAssignment] = useState([]);

  useEffect(() => {
    if (!user) {
      navigate("/login");
      return;
    }
    const fetchUserAssignment = async () => {
      setIsLoading(true);
      const config = {
        headers: {
          authorization: `Bearer ${user?.accessToken}`,
        },
      };
      try {
        const res = await axios.get(`${BASE_URL + "/assignments"}`, config);
        if (res) {
          setUserAssignment(res.data.data);
          setIsLoading(false);
        }
      } catch (error) {
        setIsLoading(false);
      }
    };
    fetchUserAssignment();
  }, [user, dispatch, navigate]);

  return (
    <div className="con">
      <section className="main">
        <h1>Welcome, {user && user.name} (Admin)</h1>
      </section>

      <section className="show_contact">
        <h1 className="h1">User Assignment Overview</h1>
        {userAssignment.length > 0 ? (
          <div className="contact">
            {userAssignment.map((con) => {
              return <AssignmentCard key={con._id} con={con} />;
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
                No assignments available at this moment.
              </h1>
            )}
          </div>
        )}
      </section>
    </div>
  );
};

export default DashboardAdmin;
