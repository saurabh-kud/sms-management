// import axios from "axios";
// import { useDispatch, useSelector } from "react-redux";

// const BASE_URL = import.meta.env.VITE_APP_BASE_URL;

// import React, { useState, useEffect } from "react";
// import {
//   BarChart,
//   Bar,
//   XAxis,
//   YAxis,
//   CartesianGrid,
//   Tooltip,
//   Legend,
//   ResponsiveContainer,
// } from "recharts";
// import { LayoutDashboard, Table2 } from "lucide-react";
// import "../css/graph.css";

// const Select = ({ value, onChange, options }) => {
//   const [isOpen, setIsOpen] = useState(false);

//   return (
//     <div className="select-container">
//       <button className="select-trigger" onClick={() => setIsOpen(!isOpen)}>
//         {options.find((opt) => opt.value === value)?.label || "Select country"}
//       </button>
//       {isOpen && (
//         <div className="select-content">
//           {options.map((option) => (
//             <div
//               key={option.value}
//               className="select-item"
//               onClick={() => {
//                 onChange(option.value);
//                 setIsOpen(false);
//               }}
//             >
//               {option.label}
//             </div>
//           ))}
//         </div>
//       )}
//     </div>
//   );
// };

// const DataDisplay = () => {
//   const [showGraph, setShowGraph] = useState(true);
//   const [selectedCountry, setSelectedCountry] = useState("all");
//   const [loading, setLoading] = useState(true);
//   const dispatch = useDispatch();
//   const { user } = useSelector((state) => state.auth);
//   const [data, setData] = useState(null);

//   const transformApiData = (apiResponse) => {
//     // Create a map to store the latest entry for each operator
//     const operatorMap = new Map();

//     // Iterate through each country
//     apiResponse.forEach((country) => {
//       // Iterate through operators in each country
//       country.operators.forEach((operator) => {
//         const operatorName = operator.operator.toUpperCase();
//         const currentTimestamp = new Date(operator.timestamp);

//         // Check if we already have an entry for this operator
//         const existingEntry = operatorMap.get(operatorName);

//         if (
//           !existingEntry ||
//           new Date(existingEntry.timestamp) < currentTimestamp
//         ) {
//           // Create flattened object with required fields
//           const flattenedData = {
//             timestamp: operator.timestamp,
//             country_code: country.country_code.toUpperCase(),
//             operator: operatorName,
//             attempts: operator.attempts,
//             sent: operator.sent,
//             success_rate: Number(operator.success_rate.toFixed(2)),
//             confirm_rate: Number(operator.confirm_rate.toFixed(2)),
//           };

//           // Update the map with the latest entry
//           operatorMap.set(operatorName, flattenedData);
//         }
//       });
//     });

//     // Convert map values to array for final result
//     return Array.from(operatorMap.values());
//   };

//   useEffect(() => {
//     // Fetch data from API
//     const fetchData = async () => {
//       try {
//         const config = {
//           headers: {
//             authorization: `Bearer ${user?.token}`,
//           },
//         };
//         const response = await axios.get(`${BASE_URL}/metrics`, config);
//         setData(transformApiData(response.data.data));
//         setLoading(false);

//         // setFilteredData(response.data.data);
//       } catch (error) {
//         console.error("Error fetching data", error);
//         setLoading(false);
//       }
//     };
//     fetchData();
//   }, []);

//   if (loading) {
//     return <div className="loading-state">Loading...</div>;
//   }

//   // Sort data by timestamp and take latest entries
//   const sortedData = [...data].sort(
//     (a, b) => new Date(b.timestamp) - new Date(a.timestamp)
//   );

//   // Filter data based on selected country
//   const filteredData =
//     selectedCountry === "all"
//       ? sortedData
//       : sortedData.filter((item) => item.country_code === selectedCountry);

//   // Get unique countries for select options
//   const countryOptions = [
//     { value: "all", label: "All Countries" },
//     ...Array.from(new Set(sortedData.map((item) => item.country_code))).map(
//       (country) => ({ value: country, label: country })
//     ),
//   ];

//   return (
//     <div className="dashboard-card">
//       <div className="card-header">
//         <div className="header-content">
//           <h2 className="dashboard-title">Latest Operator Performance</h2>
//           <div className="controls-container">
//             <Select
//               value={selectedCountry}
//               onChange={setSelectedCountry}
//               options={countryOptions}
//             />
//             <button
//               className="toggle-button"
//               onClick={() => setShowGraph(!showGraph)}
//             >
//               {showGraph ? <Table2 size={20} /> : <LayoutDashboard size={20} />}
//             </button>
//           </div>
//         </div>
//       </div>
//       <div className="card-content">
//         {showGraph ? (
//           <div className="chart-container">
//             <ResponsiveContainer width="100%" height="100%">
//               <BarChart data={filteredData}>
//                 <CartesianGrid strokeDasharray="3 3" />
//                 <XAxis dataKey="operator" />
//                 <YAxis />
//                 <Tooltip />
//                 <Legend />
//                 <Bar
//                   dataKey="success_rate"
//                   fill="#4f46e5"
//                   name="Success Rate (%)"
//                 />
//                 <Bar
//                   dataKey="confirm_rate"
//                   fill="#22c55e"
//                   name="Confirm Rate (%)"
//                 />
//               </BarChart>
//             </ResponsiveContainer>
//           </div>
//         ) : (
//           <div className="table-container">
//             <table className="dashboard-table">
//               <thead>
//                 <tr>
//                   <th>Timestamp</th>
//                   <th>Country</th>
//                   <th>Operator</th>
//                   <th className="text-right">Attempts</th>
//                   <th className="text-right">Sent</th>
//                   <th className="text-right">Success Rate (%)</th>
//                   <th className="text-right">Confirm Rate (%)</th>
//                 </tr>
//               </thead>
//               <tbody>
//                 {filteredData.map((item, index) => (
//                   <tr key={index}>
//                     <td>{new Date(item.timestamp).toLocaleString()}</td>
//                     <td>{item.country_code}</td>
//                     <td>{item.operator}</td>
//                     <td className="text-right">{item.attempts}</td>
//                     <td className="text-right">{item.sent}</td>
//                     <td className="text-right">
//                       {item.success_rate.toFixed(2)}%
//                     </td>
//                     <td className="text-right">
//                       {item.confirm_rate.toFixed(2)}%
//                     </td>
//                   </tr>
//                 ))}
//               </tbody>
//             </table>
//           </div>
//         )}
//       </div>
//     </div>
//   );
// };

// export default DataDisplay;

import React, { useState, useEffect } from "react";
import axios from "axios";
import { useDispatch, useSelector } from "react-redux";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";
import { LayoutDashboard, Table2 } from "lucide-react";
import "../css/graph.css";

const BASE_URL = import.meta.env.VITE_APP_BASE_URL;

const CustomTooltip = ({ active, payload, label }) => {
  if (active && payload && payload.length) {
    return (
      <div className="custom-tooltip">
        <p className="tooltip-label">{label}</p>
        {payload.map((entry, index) => (
          <p
            key={index}
            className={`tooltip-data ${
              entry.name === "Success Rate (%)"
                ? "tooltip-success-rate"
                : "tooltip-confirm-rate"
            }`}
          >
            {entry.name}: {entry.value.toFixed(2)}%
          </p>
        ))}
      </div>
    );
  }
  return null;
};

const Select = ({ value, onChange, options }) => {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <div className="select-container">
      <button className="select-trigger" onClick={() => setIsOpen(!isOpen)}>
        {options.find((opt) => opt.value === value)?.label || "Select country"}
      </button>
      {isOpen && (
        <div className="select-content">
          {options.map((option) => (
            <div
              key={option.value}
              className="select-item"
              onClick={() => {
                onChange(option.value);
                setIsOpen(false);
              }}
            >
              {option.label}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

const DataDisplay = () => {
  const [showGraph, setShowGraph] = useState(true);
  const [selectedCountry, setSelectedCountry] = useState("all");
  const [loading, setLoading] = useState(true);
  const dispatch = useDispatch();
  const { user } = useSelector((state) => state.auth);
  const [data, setData] = useState(null);

  const transformApiData = (apiResponse) => {
    const operatorMap = new Map();

    apiResponse.forEach((country) => {
      country.operators.forEach((operator) => {
        const operatorName = operator.operator.toUpperCase();
        const currentTimestamp = new Date(operator.timestamp);

        const existingEntry = operatorMap.get(operatorName);

        if (
          !existingEntry ||
          new Date(existingEntry.timestamp) < currentTimestamp
        ) {
          const flattenedData = {
            timestamp: operator.timestamp,
            country_code: country.country_code.toUpperCase(),
            operator: operatorName,
            attempts: operator.attempts,
            sent: operator.sent,
            success_rate: Number(operator.success_rate.toFixed(2)),
            confirm_rate: Number(operator.confirm_rate.toFixed(2)),
          };

          operatorMap.set(operatorName, flattenedData);
        }
      });
    });

    return Array.from(operatorMap.values());
  };

  useEffect(() => {
    const fetchData = async () => {
      try {
        const config = {
          headers: {
            authorization: `Bearer ${user?.token}`,
          },
        };
        const response = await axios.get(`${BASE_URL}/metrics`, config);
        setData(transformApiData(response.data.data));
        setLoading(false);
      } catch (error) {
        console.error("Error fetching data", error);
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  if (loading) {
    return <div className="loading-state">Loading...</div>;
  }

  const sortedData = [...data].sort(
    (a, b) => new Date(b.timestamp) - new Date(a.timestamp)
  );

  const filteredData =
    selectedCountry === "all"
      ? sortedData
      : sortedData.filter((item) => item.country_code === selectedCountry);

  const countryOptions = [
    { value: "all", label: "All Countries" },
    ...Array.from(new Set(sortedData.map((item) => item.country_code))).map(
      (country) => ({ value: country, label: country })
    ),
  ];

  return (
    <div className="dashboard-card">
      <div className="card-header">
        <div className="header-content">
          <h2 className="dashboard-title">Latest Operator Performance</h2>
          <div className="controls-container">
            <Select
              value={selectedCountry}
              onChange={setSelectedCountry}
              options={countryOptions}
            />
            <button
              className="toggle-button"
              onClick={() => setShowGraph(!showGraph)}
            >
              {showGraph ? <Table2 size={20} /> : <LayoutDashboard size={20} />}
            </button>
          </div>
        </div>
      </div>
      <div className="card-content">
        {showGraph ? (
          <div className="chart-container">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={filteredData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="operator" />
                <YAxis />
                <Tooltip content={<CustomTooltip />} />
                <Legend />
                <Bar
                  dataKey="success_rate"
                  fill="#4f46e5"
                  name="Success Rate (%)"
                />
                <Bar
                  dataKey="confirm_rate"
                  fill="#22c55e"
                  name="Confirm Rate (%)"
                />
              </BarChart>
            </ResponsiveContainer>
          </div>
        ) : (
          <div className="table-container">
            <table className="dashboard-table">
              <thead>
                <tr>
                  <th>Timestamp</th>
                  <th>Country</th>
                  <th>Operator</th>
                  <th className="text-right">Attempts</th>
                  <th className="text-right">Sent</th>
                  <th className="text-right">Success Rate (%)</th>
                  <th className="text-right">Confirm Rate (%)</th>
                </tr>
              </thead>
              <tbody>
                {filteredData.map((item, index) => (
                  <tr key={index}>
                    <td>{new Date(item.timestamp).toLocaleString()}</td>
                    <td>{item.country_code}</td>
                    <td>{item.operator}</td>
                    <td className="text-right">{item.attempts}</td>
                    <td className="text-right">{item.sent}</td>
                    <td className="text-right">
                      {item.success_rate.toFixed(2)}%
                    </td>
                    <td className="text-right">
                      {item.confirm_rate.toFixed(2)}%
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
};

export default DataDisplay;
