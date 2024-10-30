<div align="center">
  
# 📱 SMS Management System
<p align="center">
<a href="https://github.com/saurabh-kud"><img title="Author" src="https://img.shields.io/badge/Author-saurabh-kud--red.svg?style=for-the-badge&logo=github"></a>
</p>

<p align="center">
<a href="https://github.com/saurabh-kud"><img title="Followers" src="https://img.shields.io/github/followers/saurabh-kud?color=teal&style=flat-square"></a>
<a href="https://github.com/saurabh-kud/sms-management/network/members"><img title="Forks" src="https://img.shields.io/github/forks/saurabh-kud/sms-management?color=lightgrey&style=flat-square"></a>
<a href="https://github.com/saurabh-kud/sms-management/issues"><img title="issues" src="https://img.shields.io/github/issues/saurabh-kud/sms-management?style=flat-square">
</a>

</p>

<p align="center">
  <strong>🚀 Dynamically Manage & Monitor Your SMS Server Infrastructure</strong>
</p>

<p align="center">
  <em>SMS management system for handling multi-country operations, real-time monitoring, and automated control.</em>
</p>

</div>

## 📚 API Documentation

Comprehensive API documentation is available through Postman:
[📘 API Documentation](https://documenter.getpostman.com/view/38681155/2sAY4uDPkW)

# 📝 task

Your task is to build a web-based dashboard that dynamically manages and monitors the
SMSsystem running on a Linux server. The system consists of multiple Python programs (5-6
programs) that trigger SMS messages to multiple countries- telecom operators pairs using
phone numbers. Once an SMS is triggered, the programs communicate with an SMS Gateway
API to verify message delivery and submit the status back if the message is received.

The system manages over 100+ country-operator pairs, with the goal of sending 10 SMS
per minute per country, irrespective of how many operators belong to that country. These
country-operator pairs are dynamic and must be managed based on real-time SMS success
rates. Some pairs are designated as high-priority and must always remain active regardless of
their success rate.

Each Python program runs independently using screen sessions, with each screen session
handling one or more country-operator pairs. Your job is to develop a dynamic management
system that enables:

- Control over program execution (start/stop/restart sessions)
- Monitoring SMS performance metrics in real-time
- Adding, updating, and prioritizing country-operator pairs
- Automatic alerts for critical failures or low success rates

---

## 🏗️ Architecture

<div align="center">
  <img src="./examples/arch.png" alt="Architecture Diagram" />
</div>

## 🛠️ Tech Stack

### Backend

- 🐍 Python
- ⚡ FastAPI

### Database

- 🐘 PostgreSQL
- 🍃 MongoDB

### Visualization

- 📊 Grafana
- 📈 Prometheus

### Frontend

- ⚛️ React
- 🎨 JavaScript

## 🚀 Microservices

| Service              | Description                                            |
| -------------------- | ------------------------------------------------------ |
| 📱 SMS System        | Simulates SMS submission and session screen management |
| 🎮 Management Server | Manages sessions and country-operator pairs            |
| 🖥️ Frontend          | User interface with real-time visualization            |
| 🗄️ Mongo Server      | Stores metrics and operational data                    |
| 🔐 Postgres Server   | Manages user authentication                            |
| 📊 Prometheus Server | Collects real-time metrics                             |
| 📈 Grafana Server    | Visualizes system metrics                              |

## 🛠️ Installation

```sh

# Clone the repo
$ git clone https://github.com/saurabh-kud/sms-management

# go to sms-management directory
$ cd sms-management

# change .env.example to .env and put your own credential for teligram token and chat id if you don't provide then it will not send alert messages
$ .env.example --> .env

# run docker compose
$ docker compose -f docker-compose.yml -p sms-stack up -d --build --force-recreate --remove-orphans


```

## 🔗 Access Points

| Service     | URL                            | Credentials |
| ----------- | ------------------------------ | ----------- |
| Frontend    | http://localhost:5173          | -           |
| Backend API | http://localhost:8000/api/docs | -           |
| Prometheus  | http://localhost:9090          | -           |
| Grafana     | http://localhost:3000          | admin/admin |

> 📘 **Note**: After running the container for very first you have to wait for 2 min to get real-time metrices

---

## 🎨 Grafana Dashboard Setups

- Open URL `http://localhost:3000` with default credential admin/admin
- Click on add your first datasouce put `http://sms-stack-prometheus-1:9090` on connection url and click on save and test
- Now click on build Dashboard on next page click on import dashboard
- Now import `grafana_dashboard.json` file from main cloned directory and import
- You can see now all the metrices like sms sent, success rate and all..

---

## 🔌 API Endpoints

### 🔐 Authentication

<details>
<summary><code>POST</code> <code><b>/api/register</b></code> <code>Register new user</code></summary>

#### Request Body

```json
{
  "name": "saurabh kumar",
  "email": "saurabh322001raj3@gmail.com",
  "password": "123456"
}
```

#### Response

```json
{
  "status": 201,
  "message": "User registered successfully!!",
  "data": {
    "name": "saurabh kumar",
    "email": "saurabh322001raj3@gmail.com",
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }
}
```

</details>

<details>
<summary><code>POST</code> <code><b>/api/login</b></code> <code>User login</code></summary>

#### Request Body

```json
{
  "email": "saurabh322001raj@gmail.com",
  "password": "123456"
}
```

#### Response

```json
{
  "status": 200,
  "message": "User login successfully!!",
  "data": {
    "name": "saurabh kumar",
    "email": "saurabh322001raj@gmail.com",
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }
}
```

</details>

<details>
<summary><code>GET</code> <code><b>/api/me</b></code> <code>Get authenticated user</code></summary>

#### Headers

```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

#### Response

```json
{
  "name": "saurabh kumar",
  "email": "saurabh322001raj@gmail.com"
}
```

</details>

### 📱 Session Management

<details>
<summary><code>GET</code> <code><b>/api/sessions</b></code> <code>Get all sessions</code></summary>

#### Headers

```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

#### Response

```json
{
  "status": 200,
  "message": "session fetched successfully",
  "data": [
    {
      "_id": "67208dd2c69a81e4db627957",
      "country": "India",
      "operator": "Airtel",
      "status": "Active",
      "priority": "High"
    }
    // ... more sessions
  ]
}
```

</details>

<details>
<summary><code>POST</code> <code><b>/session/start</b></code> <code>Start a session</code></summary>

#### Request Body

```json
{
  "country": "IN",
  "operator": "VI"
}
```

#### Response

```json
{
  "status": 200,
  "message": "session started successfully",
  "data": null
}
```

</details>

<details>
<summary><code>POST</code> <code><b>/session/stop</b></code> <code>Stop a session</code></summary>

#### Request Body

```json
{
  "country": "IN",
  "operator": "VI"
}
```

#### Response

```json
{
  "status": 200,
  "message": "session stopped successfully",
  "data": null
}
```

</details>

<details>
<summary><code>POST</code> <code><b>/session/restart</b></code> <code>Restart a session</code></summary>

#### Request Body

```json
{
  "country": "IN",
  "operator": "VI"
}
```

#### Response

```json
{
  "status": 200,
  "message": "session restarted successfully",
  "data": null
}
```

</details>

### 🌍 Country-Operator Management

<details>
<summary><code>GET</code> <code><b>/api/country</b></code> <code>Get all country-operator pairs</code></summary>

#### Headers

```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

#### Response

```json
{
  "status": 200,
  "message": "Country Operator pair fetched successfully",
  "data": [
    {
      "_id": "67208dd2c69a81e4db627957",
      "country": "India",
      "operator": "Airtel",
      "status": "Active",
      "priority": "High"
    }
    // ... more pairs
  ]
}
```

</details>

<details>
<summary><code>POST</code> <code><b>/country/create</b></code> <code>Create country-operator pair</code></summary>

#### Request Body

```json
{
  "country": "Dubai",
  "operator": "dub"
}
```

#### Response

```json
{
  "status": 201,
  "message": "Country operator pair created successfully",
  "data": {
    "_id": "671ca7a6b446771cab75985b",
    "country": "Dubai",
    "operator": "dub",
    "status": "Inactive",
    "priority": "Low"
  }
}
```

</details>

<details>
<summary><code>POST</code> <code><b>/country/update</b></code> <code>Update country-operator pair</code></summary>

#### Request Body

```json
{
  "country": "Dubai",
  "operator": "dub",
  "priority": "High"
}
```

#### Response

```json
{
  "status": 200,
  "message": "Country operator pair updated successfully",
  "data": {
    "_id": "671ca75db446771cab75985a",
    "country": "Dubai",
    "operator": "dub",
    "status": "Inactive",
    "priority": "High"
  }
}
```

</details>

<details>
<summary><code>POST</code> <code><b>/country/delete</b></code> <code>Delete country-operator pair</code></summary>

#### Request Body

```json
{
  "country": "Dubai",
  "operator": "dub"
}
```

#### Response

```json
{
  "status": 200,
  "message": "Country operator pair deleted successfully",
  "data": null
}
```

</details>

### 📊 Metrics & Monitoring

<details>
<summary><code>GET</code> <code><b>/api/metrics</b></code> <code>Get real-time analytics</code></summary>

#### Response

```json
{
  "status": 200,
  "message": "Data fetched successfully",
  "data": [
    {
      "country_code": "India",
      "operators": [
        {
          "operator": "JIO",
          "attempts": 30,
          "sent": 20,
          "received": 0,
          "confirmed": 18,
          "success_rate": 66.67,
          "SMS_success_rate": 0,
          "confirm_rate": 90.0,
          "timestamp": "2024-10-29 07:26:48"
        }
        // ... more operators
      ]
    }
    // ... more countries
  ]
}
```

</details>

<details>
<summary><code>GET</code> <code><b>/metrics</b></code> <code>Get Prometheus metrics</code></summary>

#### Sample Response

```
# HELP sms_attempts Number of SMS attempts
# TYPE sms_attempts gauge
sms_attempts{country="India",operator="JIO"} 30.0
sms_attempts{country="Tajikistan",operator="MegaFon"} 30.0

# HELP sms_sent Number of SMS sent
# TYPE sms_sent gauge
sms_sent{country="India",operator="JIO"} 25.0
sms_sent{country="Tajikistan",operator="MegaFon"} 25.0

# ... more metrics
```

</details>

### 🎯 Quick Reference

| Category     | Endpoint           | Method | Description                 |
| ------------ | ------------------ | ------ | --------------------------- |
| 🔐 Auth      | `/api/register`    | POST   | Register new user           |
| 🔐 Auth      | `/api/login`       | POST   | User login                  |
| 🔐 Auth      | `/api/me`          | GET    | Get authenticated user      |
| 📱 Sessions  | `/api/sessions`    | GET    | List all sessions           |
| 📱 Sessions  | `/session/start`   | POST   | Start a session             |
| 📱 Sessions  | `/session/stop`    | POST   | Stop a session              |
| 📱 Sessions  | `/session/restart` | POST   | Restart a session           |
| 🌍 Countries | `/api/country`     | GET    | List country-operator pairs |
| 🌍 Countries | `/country/create`  | POST   | Create new pair             |
| 🌍 Countries | `/country/update`  | POST   | Update existing pair        |
| 🌍 Countries | `/country/delete`  | POST   | Delete a pair               |
| 📊 Metrics   | `/api/metrics`     | GET    | Get real-time analytics     |
| 📊 Metrics   | `/metrics`         | GET    | Get Prometheus metrics      |

---

> 📘 **Note**: All authenticated endpoints require a valid JWT token in the Authorization header.

## 📸 Screenshots

<details>
<summary>⚡ Running Screen Session  </summary>
<div align="center">
  <img src="./examples/screen.png" alt="Screen session" />
</div>
</details>

<details>
<summary>⚡ Message simulation  </summary>
<div align="center">
  <img src="./examples/sim.png" alt="Screen session" />
</div>
</details>

<details>
<summary>📈 Main Dashboard </summary>
<div align="center">
  <img src="./examples/graph.png" alt="Graph Dashboard" />
</div>
</details>

<details>
<summary>📋 Table View Dashboard </summary>
<div align="center">
  <img src="./examples/table.png" alt="Table View Dashboard" />
</div>
</details>

<details>
<summary>📝 Session List </summary>
<div align="center">
  <img src="./examples/session.png" alt="Session list" />
</div>
</details>

<details>
<summary>🔗 Country Operator Pair List </summary>
<div align="center">
  <img src="./examples/pair.png" alt="Country list" />
</div>
</details>

<details>
<summary>➕ Add New Country Operator Pair</summary>
<div align="center">
  <img src="./examples/add.png" alt="Add Country" />
</div>
</details>

<details>
<summary>✏️ Update Country Operator Pair</summary>
<div align="center">
  <img src="./examples/update.png" alt="Update Country" />
</div>
</details>

<details>
<summary>📝 Register</summary>
<div align="center">
  <img src="./examples/register.png" alt="register" />
</div>
</details>

<details>
<summary>🔑 Login</summary>
<div align="center">
  <img src="./examples/login.png" alt="login" />
</div>
</details>

<details>
<summary>📊 teligram Sms Alert</summary>
<div align="center">
  <img src="./examples/sms.jpg" alt="Sms alert" />
</div>
</details>

<details>
<summary>📊 Grafana Dashboard</summary>
<div align="center">
  <img src="./examples/grafana.png" alt="Grafana Dashboard" />
</div>
</details>

<details>
<summary>📈 Prometheus Dashboard</summary>
<div align="center">
  <img src="./example/prom.png" alt="Prometheus Dashboard" />
</div>
</details>

<summary>📺 Watch video of demonstrating all features</summary>
<br/>

[![Youtube video](./examples/graph.png)](https://www.youtube.com/watch?v=QW85MvgaEPQ)

## 👨‍💻 Author

<div align="center">
<img src="https://github.com/saurabh-kud.png" width="100px" style="border-radius: 50%;" alt="Saurabh Kumar"/>

**Saurabh Kumar**

[![GitHub](https://img.shields.io/badge/GitHub-%40saurabh--kud-blue?style=social&logo=github)](https://github.com/saurabh-kud)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-%40saurabh--kud-blue?style=social&logo=linkedin)](https://www.linkedin.com/in/saurabh-kud/)

</div>

## 📝 License

Copyright © 2024 [Saurabh Kumar](https://github.com/saurabh-kud).  
This project is [MIT](LICENSE) licensed.

---

<div align="center">

Made with ❤️ by [Saurabh Kumar](https://github.com/saurabh-kud)

</div>
