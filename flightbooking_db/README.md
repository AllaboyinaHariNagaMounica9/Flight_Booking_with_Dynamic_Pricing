# ⚙️ Flight Booking Backend API (FastAPI)

This is the **backend service** for the **SkySwap Flight Booking System**, developed using **FastAPI** and **SQLAlchemy** with **SQLite/MySQL** support.  
It provides all API endpoints for **flight search**, **dynamic pricing**, **booking**, and **passenger management**.

---

## 🧩 Overview

The backend manages all database operations for:
- Airlines, Airports, and Flights  
- User registration and authentication  
- Bookings and Passengers  
- Dynamic pricing calculation  
- Payment and cancellation handling  

---

## 🛠️ Tech Stack

| Component | Technology |
|------------|-------------|
| **Framework** | FastAPI |
| **ORM** | SQLAlchemy |
| **Database** | SQLite (default) / MySQL (optional) |
| **Models Validation** | Pydantic |
| **Concurrency** | Uvicorn + Async lifespan |
| **Cross-Origin Access** | CORS Middleware enabled |

---

## 📂 Project Structure

```

backend/
│
├── flightbooking_db.py     # Main FastAPI backend file
├── infosys_flight_db.db    # SQLite database (auto-created)
└── requirements.txt         # Python dependencies

````

---

## ⚙️ Setup Instructions

### 1️⃣ Install Dependencies
Make sure Python 3.10+ is installed.

```bash
pip install fastapi uvicorn sqlalchemy pydantic email-validator python-multipart
````

### 2️⃣ Run the Server

Start the backend with:

```bash
uvicorn flightbooking_db:app --reload
```

### 3️⃣ Server Running At

```
http://127.0.0.1:8000
```

You can view the **interactive API documentation** here:

* Swagger UI → [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* ReDoc → [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 🗄️ Database

The backend uses **SQLAlchemy ORM** to manage the database models.
It automatically creates tables upon first run.

### 🧱 Tables Created

| Table            | Description                                  |
| ---------------- | -------------------------------------------- |
| `Airline`        | Stores airline details                       |
| `Airport`        | Stores airport info and IATA codes           |
| `Flight`         | Stores flight data, times, fares             |
| `User`           | Stores user login and role                   |
| `Booking`        | Stores bookings linked to flights and users  |
| `Passenger`      | Stores passenger details under each booking  |
| `Payment`        | Stores payment details for each booking      |
| `DynamicPricing` | Stores and calculates real-time flight fares |

---

## 💡 Key Features

✅ **Dynamic Pricing**
Automatically adjusts flight fare based on seat availability, time to departure, and demand.

✅ **Transaction-Safe Booking**
Ensures atomic creation of bookings and passengers in one transaction.

✅ **Automatic Data Seeding**
Initial airlines, airports, and flights are auto-inserted when the app starts.

✅ **Booking Management**
Supports booking creation, retrieval, and cancellation with seat restoration.

✅ **CORS Enabled**
Allows frontend (React) to access APIs without restriction.

---

## 🔗 API Endpoints

| Method   | Endpoint                        | Description                          |
| -------- | ------------------------------- | ------------------------------------ |
| `GET`    | `/`                             | Root check – API health              |
| `GET`    | `/airlines`                     | Get all airlines                     |
| `POST`   | `/airlines`                     | Add new airline                      |
| `GET`    | `/airports`                     | Get all airports                     |
| `GET`    | `/flights/`                     | Fetch all flights                    |
| `GET`    | `/pricing/{flight_id}`          | Get dynamic fare for a flight        |
| `POST`   | `/booking/reserve`              | Create a new booking with passengers |
| `GET`    | `/bookings/{booking_id}`        | Retrieve booking details             |
| `DELETE` | `/bookings/cancel/{booking_id}` | Cancel a booking and restore seats   |

---

## 🧮 Dynamic Pricing Logic

The fare is calculated based on:

* **Seat Availability Ratio**
* **Time to Departure**
* **Random Demand Factor**
* **Airline Tier Factor**

```python
def calculate_dynamic_price(base_fare, seats_available, total_seats, departure, flight_number):
    seat_ratio = seats_available / total_seats
    seat_factor = 0.4 * (1 - seat_ratio)
    days = (departure - datetime.now()).total_seconds() / 86400
    # Time sensitivity
    if days <= 0: time_factor = 0.6
    elif days <= 1: time_factor = 0.4
    elif days <= 3: time_factor = 0.2
    elif days <= 7: time_factor = 0.1
    else: time_factor = -0.05
    demand_factor = random.uniform(-0.08, 0.25)
    tier_factor = 0.12 if "premium" in flight_number.lower() or "ai" in flight_number.lower() else -0.03
    total_multiplier = 1 + seat_factor + time_factor + demand_factor + tier_factor
    return max(round(base_fare * total_multiplier, 2), 50.0)
```

---

## 🔒 Example Booking Flow

1️⃣ Fetch available flights
`GET /flights/`

2️⃣ Get price for a flight
`GET /pricing/{flight_id}`

3️⃣ Create a booking with passengers
`POST /booking/reserve`

```json
{
  "booking_details": { "UserID": 1, "FlightID": 1 },
  "passengers": [
    { "PassengerName": "Ravi", "Age": 25, "Gender": "Male", "SeatNumber": "12A" }
  ]
}
```

4️⃣ Cancel a booking
`DELETE /bookings/cancel/1`

---

## 🧠 Notes

* If no data exists, default airlines, airports, and flights are auto-generated.
* You can easily switch to MySQL by updating this line:

  ```python
  DATABASE_URL = "mysql+pymysql://root:password@localhost/FlightBookingDB"
  ```
* The backend and frontend communicate using JSON APIs.

---

## 📦 Example Response

```json
{
  "BookingID": 1,
  "UserID": 1,
  "FlightID": 1,
  "BookingDate": "2025-11-01T14:23:00",
  "TotalFare": 5400.0,
  "Status": "Confirmed",
  "passengers": [
    { "PassengerName": "Ravi", "Age": 25, "Gender": "Male", "SeatNumber": "12A" }
  ]
}
```

---

## 👩‍💻 Developer

**Name:** Hari Mounica
**College:** Sir C.R. Reddy College of Engineering (JNTUK)
**Course:** B.Tech CSE (3rd Year)
**Project:** Infosys Springboard Milestone 4 – Backend Module
**Framework:** FastAPI
**Database:** SQLite / MySQL

---

### ✨ "Fast, Reliable, and Smart Flight Management with SkySwap API"

```
