<h2 align='center'>Sms Management and Monitering</h2>
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
    Sms Management- manage and moniter your sms server
</p>

## api-postman-docs 🔗

[https://documenter.getpostman.com/view/38681155/2sAY4uDPkW](https://documenter.getpostman.com/view/38681155/2sAY4uDPkW)

# task

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
  <img src="./example/1.png" alt="Architecture Diagram" />
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

| Service              | Description                                     |
| -------------------- | ----------------------------------------------- |
| 📱 SMS System        | Simulates SMS submission and session management |
| 🎮 Management Server | Manages sessions and country-operator pairs     |
| 🖥️ Frontend          | User interface with real-time visualization     |
| 🗄️ Mongo Server      | Stores metrics and operational data             |
| 🔐 Postgres Server   | Manages user authentication                     |
| 📊 Prometheus Server | Collects real-time metrics                      |
| 📈 Grafana Server    | Visualizes system metrics                       |

## 🛠️ Installation

```sh

# Clone the repo
$ git clone https://github.com/saurabh-kud/sms-management

# go to sms-management directory
$ cd sms-management

# change .env.example to .env and put your own credential for teligram token and chat id if you don't provide then it just not send messages
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

# endpoint response

> [GET] Home Endpoint [/](http://localhost:8000/health)

<details open>
<summary> See response</summary>
<p>

```json
RESPONSE 200
{
    "app": "sms-managemnent",
    "version": "v0.0.1",
    "ip": "172.19.0.1",
    "uptime": 2841.2992215156555,
    "mode": "development"
}
```

</p>
</details>

> [POST] User Register Endpoint [/register](http://localhost:8000/api/register)

<details open>
<summary> See response</summary>
<p>

```json
{
    "name": "saurabh kumar",
    "email": "saurabh322001raj3@gmail.com",
    "password": "123456"
}

RESPONSE 201
{
    "status": 201,
    "message": "User registered successfully!!",
    "data": {
        "name": "saurabh kumar",
        "email": "saurabh322001raj3@gmail.com",
        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzYXVyYWJoMzIyMDAxcmFqM0BnbWFpbC5jb20iLCJleHAiOjE3MzA0NzkwOTN9.Fn9oOvPqA6QRMpWOsGFFq61s1Ei-e0JRxy3dm5C8yQU"
    }
}
```

</p>
</details>

> [POST] Login Endpoint [/login](http://localhost:8080/api/login)

<details open>
<summary> See response</summary>
<p>

```json
{
    "email": "saurabh322001raj@gmail.com",
    "password": "123456"
}

RESPONSE 200
{
    "status": 200,
    "message": "User login successfully!!",
    "data": {
        "name": "saurabh kumar",
        "email": "saurabh322001raj@gmail.com",
        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzYXVyYWJoMzIyMDAxcmFqQGdtYWlsLmNvbSIsImV4cCI6MTczMDQ4MDkxOX0.FS6niwI_aRIG_8Ya93ybeHQymyaz6_VyQiDrNsIhToI"
    }
}
```

</p>
</details>

> [GET] me Endpoint (authenticate user ) [/me](http://localhost:8080/api/me)

<details open>
<summary> See response</summary>
<p>

```json
Headers : Bearer eyJhbGciO.......


RESPONSE 200
{
    "name": "saurabh kumar",
    "email": "saurabh322001raj@gmail.com"
}
```

</p>
</details>

> [GET] Get all sessions [/sessions](http://localhost:8080/api/sessions)

<details open>
<summary> See response</summary>
<p>

```json
Headers : Bearer eyJhbGciO.......


RESPONSE 200
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
        },
        {
            "_id": "67208dd2c69a81e4db627958",
            "country": "India",
            "operator": "JIO",
            "status": "Active",
            "priority": "Low"
        },
        {
            "_id": "67208dd2c69a81e4db627959",
            "country": "India",
            "operator": "VI",
            "status": "Active",
            "priority": "Low"
        },
        {
            "_id": "67208dd2c69a81e4db62795a",
            "country": "India",
            "operator": "Tata-Docomo",
            "status": "Active",
            "priority": "Low"
        },
        {
            "_id": "67208dd2c69a81e4db62795b",
            "country": "Uzbekistan",
            "operator": "UzMobile",
            "status": "Active",
            "priority": "Low"
        },
        {
            "_id": "67208dd2c69a81e4db62795c",
            "country": "Ukraine",
            "operator": "3Mob",
            "status": "Active",
            "priority": "High"
        },
        {
            "_id": "67208dd2c69a81e4db62795d",
            "country": "Tajikistan",
            "operator": "MegaFon",
            "status": "Active",
            "priority": "High"
        }
    ]
}
```

</p>
</details>

> [POST] start Session [/session/start](http://localhost:8000/session/start)

<details open>
<summary> See response</summary>
<p>

```json
{
    "country": "IN",
    "operator": "VI"
}

RESPONSE 200
{
    "status": 200,
    "message": "session started successfully",
    "data": null
}
```

</p>
</details>

> [POST] stop Session [/session/start](http://localhost:8000/session/stop)

<details open>
<summary> See response</summary>
<p>

```json
{
    "country": "IN",
    "operator": "VI"
}

RESPONSE 200
{
    "status": 200,
    "message": "session stopped successfully",
    "data": null
}
```

</p>
</details>

> [POST] restart Session [/session/start](http://localhost:8000/session/restart)

<details open>
<summary> See response</summary>
<p>

```json
{
    "country": "IN",
    "operator": "VI"
}

RESPONSE 200
{
    "status": 200,
    "message": "session restarted successfully",
    "data": null
}
```

</p>
</details>

> [GET] Get all Country Operator pair [/sessions](http://localhost:8000/api/country)

<details open>
<summary> See response</summary>
<p>

```json
Headers : Bearer eyJhbGciO.......


RESPONSE 200
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
        },
        {
            "_id": "67208dd2c69a81e4db627958",
            "country": "India",
            "operator": "JIO",
            "status": "Active",
            "priority": "Low"
        },
        {
            "_id": "67208dd2c69a81e4db627959",
            "country": "India",
            "operator": "VI",
            "status": "Active",
            "priority": "Low"
        },
        {
            "_id": "67208dd2c69a81e4db62795a",
            "country": "India",
            "operator": "Tata-Docomo",
            "status": "Active",
            "priority": "Low"
        },
        {
            "_id": "67208dd2c69a81e4db62795b",
            "country": "Uzbekistan",
            "operator": "UzMobile",
            "status": "Active",
            "priority": "Low"
        },
        {
            "_id": "67208dd2c69a81e4db62795c",
            "country": "Ukraine",
            "operator": "3Mob",
            "status": "Active",
            "priority": "High"
        },
        {
            "_id": "67208dd2c69a81e4db62795d",
            "country": "Tajikistan",
            "operator": "MegaFon",
            "status": "Active",
            "priority": "High"
        }
    ]
}
```

</p>
</details>

> [POST] Create country operator pair [/country/create](http://localhost:8080/country/create)

<details open>
<summary> See response</summary>
<p>

```json
{
    "country": "Dubai",
    "operator":"dub"
}

RESPONSE 200
{
    "status": 201,
    "message": "Country operator pair created successfully",
    "data": {
        "_id": "671ca7a6b446771cab75985b",
        "country": "thai",
        "operator": "th",
        "status": "Inactive",
        "priority": "Low"
    }
}
```

</p>
</details>

> [POST] Update country operator pair [/country/update](http://localhost:8000/country/update)

<details open>
<summary> See response</summary>
<p>

```json
{
    "country": "Dubai",
    "operator":"dub",
    "priority":"High"
}

RESPONSE 200
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

</p>
</details>

> [POST] Delete country operator pair [/country/delete](http://localhost:8000/country/delete)

<details open>
<summary> See response</summary>
<p>

```json
{
    "country": "Dubai",
    "operator":"dub"
}

RESPONSE 200
{
    "status": 200,
    "message": "Country operator pair deleted successfully",
    "data": null
}
```

</p>
</details>

> [GET] Real-time analytics [/api/metrics](http://localhost:8000/api/metrics)

<details open>
<summary> See response</summary>
<p>

```json

RESPONSE 200
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
                    "success_rate": 66.66666666666666,
                    "SMS_success_rate": 0,
                    "confirm_rate": 90.0,
                    "timestamp": "2024-10-29 07:26:48"
                },
                {
                    "operator": "Airtel",
                    "attempts": 30,
                    "sent": 27,
                    "received": 0,
                    "confirmed": 23,
                    "success_rate": 90.0,
                    "SMS_success_rate": 0,
                    "confirm_rate": 85.18518518518519,
                    "timestamp": "2024-10-29 07:27:01"
                },
                {
                    "operator": "VI",
                    "attempts": 30,
                    "sent": 28,
                    "received": 0,
                    "confirmed": 27,
                    "success_rate": 93.33333333333333,
                    "SMS_success_rate": 0,
                    "confirm_rate": 96.42857142857143,
                    "timestamp": "2024-10-29 07:27:04"
                },
                {
                    "operator": "Tata-Docomo",
                    "attempts": 30,
                    "sent": 29,
                    "received": 0,
                    "confirmed": 24,
                    "success_rate": 96.66666666666667,
                    "SMS_success_rate": 0,
                    "confirm_rate": 82.75862068965517,
                    "timestamp": "2024-10-29 07:27:06"
                }
            ]
        },
        {
            "country_code": "Tajikistan",
            "operators": [
                {
                    "operator": "MegaFon",
                    "attempts": 30,
                    "sent": 23,
                    "received": 0,
                    "confirmed": 20,
                    "success_rate": 76.66666666666667,
                    "SMS_success_rate": 0,
                    "confirm_rate": 86.95652173913044,
                    "timestamp": "2024-10-29 07:26:54"
                },

            ]
        },
        {
            "country_code": "Ukraine",
            "operators": [
                {
                    "operator": "3Mob",
                    "attempts": 30,
                    "sent": 25,
                    "received": 0,
                    "confirmed": 22,
                    "success_rate": 83.33333333333334,
                    "SMS_success_rate": 0,
                    "confirm_rate": 88.0,
                    "timestamp": "2024-10-29 07:26:58"
                }
            ]
        },
        {
            "country_code": "Uzbekistan",
            "operators": [
                {
                    "operator": "UzMobile",
                    "attempts": 30,
                    "sent": 27,
                    "received": 0,
                    "confirmed": 25,
                    "success_rate": 90.0,
                    "SMS_success_rate": 0,
                    "confirm_rate": 92.5925925925926,
                    "timestamp": "2024-10-29 07:27:02"
                }
            ]
        }
    ]
}
```

</p>
</details>

> [GEt] Prometheus metrics [/metrics](http://localhost:8000/country/delete)

<details open>
<summary> See response</summary>
<p>

```json


RESPONSE 200
# HELP python_gc_objects_collected_total Objects collected during gc
# TYPE python_gc_objects_collected_total counter
python_gc_objects_collected_total{generation="0"} 5649.0
python_gc_objects_collected_total{generation="1"} 4707.0
python_gc_objects_collected_total{generation="2"} 1743.0
# HELP python_gc_objects_uncollectable_total Uncollectable objects found during GC
# TYPE python_gc_objects_uncollectable_total counter
python_gc_objects_uncollectable_total{generation="0"} 0.0
python_gc_objects_uncollectable_total{generation="1"} 0.0
python_gc_objects_uncollectable_total{generation="2"} 0.0
# HELP python_gc_collections_total Number of times this generation was collected
# TYPE python_gc_collections_total counter
python_gc_collections_total{generation="0"} 380.0
python_gc_collections_total{generation="1"} 34.0
python_gc_collections_total{generation="2"} 3.0
# HELP python_info Python platform information
# TYPE python_info gauge
python_info{implementation="CPython",major="3",minor="11",patchlevel="10",version="3.11.10"} 1.0
# HELP process_virtual_memory_bytes Virtual memory size in bytes.
# TYPE process_virtual_memory_bytes gauge
process_virtual_memory_bytes 1.256259584e+09
# HELP process_resident_memory_bytes Resident memory size in bytes.
# TYPE process_resident_memory_bytes gauge
process_resident_memory_bytes 1.0692608e+08
# HELP process_start_time_seconds Start time of the process since unix epoch in seconds.
# TYPE process_start_time_seconds gauge
process_start_time_seconds 1.73018952305e+09
# HELP process_cpu_seconds_total Total user and system CPU time spent in seconds.
# TYPE process_cpu_seconds_total counter
process_cpu_seconds_total 38.11
# HELP process_open_fds Number of open file descriptors.
# TYPE process_open_fds gauge
process_open_fds 25.0
# HELP process_max_fds Maximum number of open file descriptors.
# TYPE process_max_fds gauge
process_max_fds 1.048576e+06
# HELP sms_attempts Number of SMS attempts
# TYPE sms_attempts gauge
sms_attempts{country="India",operator="JIO"} 30.0
sms_attempts{country="Tajikistan",operator="MegaFon"} 30.0
sms_attempts{country="Ukraine",operator="3Mob"} 30.0
sms_attempts{country="India",operator="Airtel"} 30.0
sms_attempts{country="Uzbekistan",operator="UzMobile"} 30.0
sms_attempts{country="India",operator="VI"} 30.0
sms_attempts{country="India",operator="Tata-Docomo"} 30.0
# HELP sms_sent Number of SMS sent
# TYPE sms_sent gauge
sms_sent{country="India",operator="JIO"} 25.0
sms_sent{country="Tajikistan",operator="MegaFon"} 25.0
sms_sent{country="Ukraine",operator="3Mob"} 28.0
sms_sent{country="India",operator="Airtel"} 29.0
sms_sent{country="Uzbekistan",operator="UzMobile"} 28.0
sms_sent{country="India",operator="VI"} 26.0
sms_sent{country="India",operator="Tata-Docomo"} 30.0
# HELP sms_received Number of SMS received
# TYPE sms_received gauge
sms_received{country="India",operator="JIO"} 0.0
sms_received{country="Tajikistan",operator="MegaFon"} 0.0
sms_received{country="Ukraine",operator="3Mob"} 0.0
sms_received{country="India",operator="Airtel"} 0.0
sms_received{country="Uzbekistan",operator="UzMobile"} 0.0
sms_received{country="India",operator="VI"} 0.0
sms_received{country="India",operator="Tata-Docomo"} 0.0
# HELP sms_confirmed Number of SMS confirmed
# TYPE sms_confirmed gauge
sms_confirmed{country="India",operator="JIO"} 24.0
sms_confirmed{country="Tajikistan",operator="MegaFon"} 22.0
sms_confirmed{country="Ukraine",operator="3Mob"} 25.0
sms_confirmed{country="India",operator="Airtel"} 26.0
sms_confirmed{country="Uzbekistan",operator="UzMobile"} 27.0
sms_confirmed{country="India",operator="VI"} 23.0
sms_confirmed{country="India",operator="Tata-Docomo"} 28.0
# HELP sms_success_rate Success rate of SMS
# TYPE sms_success_rate gauge
sms_success_rate{country="India",operator="JIO"} 83.33333333333334
sms_success_rate{country="Tajikistan",operator="MegaFon"} 83.33333333333334
sms_success_rate{country="Ukraine",operator="3Mob"} 93.33333333333333
sms_success_rate{country="India",operator="Airtel"} 96.66666666666667
sms_success_rate{country="Uzbekistan",operator="UzMobile"} 93.33333333333333
sms_success_rate{country="India",operator="VI"} 86.66666666666667
sms_success_rate{country="India",operator="Tata-Docomo"} 100.0
# HELP sms_confirm_rate Confirm rate of SMS
# TYPE sms_confirm_rate gauge
sms_confirm_rate{country="India",operator="JIO"} 96.0
sms_confirm_rate{country="Tajikistan",operator="MegaFon"} 88.0
sms_confirm_rate{country="Ukraine",operator="3Mob"} 89.28571428571429
sms_confirm_rate{country="India",operator="Airtel"} 89.65517241379311
sms_confirm_rate{country="Uzbekistan",operator="UzMobile"} 96.42857142857143
sms_confirm_rate{country="India",operator="VI"} 88.46153846153845
sms_confirm_rate{country="India",operator="Tata-Docomo"} 93.33333333333333
```

</p>
</details>

## 📸 Screenshots

<details>
<summary>📊 Grafana Dashboard</summary>
<div align="center">
  <img src="./example/2.png" alt="Grafana Dashboard" />
</div>
</details>

<details>
<summary>📈 Prometheus Dashboard</summary>
<div align="center">
  <img src="./example/3.png" alt="Prometheus Dashboard" />
</div>
</details>

<details>
<summary>🐰 RabbitMQ Dashboard</summary>
<div align="center">
  <img src="./example/4.png" alt="RabbitMQ Dashboard" />
</div>
</details>

<details>
<summary>📝 Logging</summary>
<div align="center">
  <img src="./example/5.png" alt="Logging" />
</div>
</details>

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
