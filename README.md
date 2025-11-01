# ✈️ Flight Booking Simulator with Dynamic Pricing

A full-stack **Flight Reservation System** that simulates real-world airline booking platforms with **dynamic fare adjustments**, **concurrency-safe seat reservations**, and an **animated, user-friendly interface**.  
This project integrates a **MySQL Database**, **FastAPI Backend**, and a **React Frontend**, offering end-to-end simulation of flight bookings, dynamic pricing, and payments.

---

## 🧭 Project Overview

The **Flight Booking Simulator with Dynamic Pricing** is designed to emulate modern airline systems by integrating:
- Dynamic fare algorithms that respond to seat availability and demand.
- Concurrency-safe booking workflows.
- A structured database for flights, bookings, and fare history.
- REST APIs for full CRUD operations.
- An interactive, animated frontend for end users.

Users can:
- 🔍 Search flights and compare fares.
- 💸 View dynamic pricing in real time.
- 💺 Reserve seats and complete simulated payments.
- 🧾 Receive downloadable booking receipts.
- 📜 View booking history with PNR tracking.

---

## 🎯 Project Statement

This project demonstrates how full-stack systems can simulate airline operations using:
- Dynamic fare computation.
- Transactional booking workflow with concurrency control.
- API-based CRUD operations.
- Realistic seat availability and demand fluctuations.
- Seamless frontend–backend–database integration.

Through this project, students gain hands-on experience in:
> API development • Database design • Transactional systems • Frontend integration • Dynamic pricing logic.

---

## 🧩 System Architecture

```

Frontend (React + Tailwind + Framer Motion)
↓ Fetch API
Backend (FastAPI + SQLAlchemy)
↓ ORM
Database (MySQL)

````

---

## ⚙️ Technology Stack

| Layer | Technology | Purpose |
|--------|-------------|----------|
| **Database** | MySQL | Stores flights, bookings, passengers, fare history |
| **Backend** | FastAPI + SQLAlchemy | REST API and dynamic fare logic |
| **Frontend** | React + Tailwind CSS + Framer Motion | Animated and interactive user interface |
| **Language** | Python 3.10+, JavaScript (ES6) | Backend + Frontend |
| **ORM** | SQLAlchemy | Database abstraction layer |
| **API Docs** | FastAPI Swagger UI | Interactive API testing |
| **Environment** | Node.js + npm (Frontend) | React runtime |

---

## 🗄️ Database Module (MySQL)

### 🧱 Database: `FlightBookingDB`

**Purpose:** To store and manage airline, airport, flight, booking, and passenger data with dynamic fare tracking.

### 📋 Tables

| Table | Description |
|--------|-------------|
| **Airline** | Airline information (name, logo, tier) |
| **Airport** | IATA codes and city names |
| **Flight** | Flight number, route, base fare, departure time |
| **Booking** | PNR, flight ID, payment status, fare amount |
| **Passenger** | Passenger details linked to bookings |
| **FareHistory** | Stores historical fare data for analytics |

### 🔑 Relationships
- `Flight → Airline` (Many-to-One)
- `Booking → Flight` (Many-to-One)
- `Passenger → Booking` (Many-to-One)
- `FareHistory → Flight` (Many-to-One)

### 💾 Example SQL Query

```sql
-- Retrieve flights with current fare and remaining seats
SELECT f.FlightNumber, a.AirlineName, s.IATA_Code AS Source, d.IATA_Code AS Destination,
       f.BaseFare, (f.TotalSeats - COUNT(b.BookingID)) AS AvailableSeats
FROM Flight f
JOIN Airline a ON f.AirlineID = a.AirlineID
JOIN Airport s ON f.SourceAirportID = s.AirportID
JOIN Airport d ON f.DestinationAirportID = d.AirportID
LEFT JOIN Booking b ON f.FlightID = b.FlightID
GROUP BY f.FlightID;
````

---

## 🧮 Dynamic Pricing Logic

Dynamic fares are calculated based on:

| Factor            | Description                              |
| ----------------- | ---------------------------------------- |
| **Seat Factor**   | Remaining seat ratio affects base fare   |
| **Time Factor**   | Closer departures increase prices        |
| **Demand Factor** | Simulated random demand fluctuations     |
| **Airline Tier**  | Premium airlines apply fare multipliers  |
| **Base Fare**     | Starting price reference for computation |

**Formula Example:**

```
Dynamic Fare = BaseFare × (1 + SeatFactor + TimeFactor + DemandFactor + TierFactor)
```

---

## 🖥️ Backend Module (FastAPI)

### 🧠 Purpose

To serve RESTful APIs that handle flight listings, dynamic pricing, bookings, and payments.

### 🛠️ Tech Stack

* **FastAPI**
* **SQLAlchemy ORM**
* **MySQL Connector**
* **Pydantic Models**
* **Threading & Concurrency Locks**

### 📁 Main File

`flightbooking_db.py`

### 🚀 Key Endpoints

| Endpoint                    | Method | Description                             |
| --------------------------- | ------ | --------------------------------------- |
| `/flights/`                 | GET    | Retrieve all flights with dynamic fares |
| `/pricing/{flight_no}`      | GET    | Get updated price for a flight          |
| `/fare-history/{flight_no}` | GET    | Fetch flight's price history            |
| `/booking/reserve`          | POST   | Reserve a seat and generate PNR         |
| `/bookings/pay/{pnr}`       | POST   | Simulate payment for booking            |
| `/bookings/confirm/{pnr}`   | POST   | Confirm booking                         |
| `/bookings/cancel/{pnr}`    | DELETE | Cancel booking and restore seat         |
| `/bookings/`                | GET    | Retrieve all bookings                   |
| `/bookings/{pnr}`           | GET    | Get booking by PNR                      |

### 🧰 Run Backend

```bash
# Install dependencies
pip install fastapi uvicorn sqlalchemy mysql-connector-python pydantic

# Run server
uvicorn flightbooking_db:app --reload
```

**Backend runs on:**
➡️ `http://localhost:8000`

---

## 🎨 Frontend Module (React)

### 🧠 Purpose

To create a responsive, animated interface that connects with backend APIs for flight search, booking, and payment simulation.

### 🛠️ Tech Stack

* React (Hooks)
* Tailwind CSS
* Framer Motion (animations)
* Fetch API (backend integration)

### 📁 Key File

`APP.js`

### 🌟 Core Features

* Animated home and navigation transitions
* Search flights by IATA codes
* Real-time dynamic fare updates
* Passenger entry form
* Secure simulated payments
* JSON receipt download
* Booking history and PNR display

### ⚙️ Run Frontend

```bash
cd frontend
npm install
npm start
```

Access in browser:
➡️ `http://localhost:3000`

---

## 📊 Milestones

### **Milestone 1: Database & Sample Data**

* Designed schema for airlines, airports, flights, passengers, and bookings.
* Implemented sample data with realistic relationships.
* Practiced SQL joins, constraints, and transactions.

### **Milestone 2: Flight Search & Dynamic Pricing**

* Built REST APIs for flight retrieval and pricing.
* Added dynamic fare algorithm using seat availability, time to departure, and demand.
* Implemented background simulation for demand fluctuations.
* Stored fare history for analytics.

### **Milestone 3: Booking Workflow & Transaction Management**

* Developed multi-step booking: flight selection → passenger info → payment.
* Implemented concurrency-safe seat reservations using transactions and row locks.
* Generated unique PNRs for confirmed bookings.
* Added endpoints for booking confirmation and cancellation.

### **Milestone 4: Frontend UI & API Integration**

* Built animated, responsive frontend with React and Tailwind CSS.
* Integrated backend APIs for live flight data and booking operations.
* Implemented multi-step booking with JSON receipt downloads.
* Completed project polish and testing.

---

## 📄 Example Booking Receipt (JSON)

```json
{
  "BookingID": "PNR6G2ZKP",
  "Flight": "AI302",
  "Airline": "Air India",
  "Passengers": [
    { "name": "Hari Mounica", "age": 24, "gender": "Female" }
  ],
  "DynamicFare": 5345.5,
  "Time": "2025-11-01 18:45:00"
}
```

---

## 🧑‍💻 Developer Details

**Name:** Hari Mounica
**College:** Sir C.R. Reddy College of Engineering (JNTUK)
**Course:** B.Tech – Computer Science Engineering (3rd Year)
**Project:** Infosys Springboard – Flight Booking Simulator with Dynamic Pricing

**Modules Covered:**

* 🗄️ Database Design (MySQL)
* ⚙️ Backend API Development (FastAPI)
* 🎨 Frontend Development & Integration (React)

---

## 📁 Project Structure

```
FlightBookingSimulator/
│
├── DATABASE.sql           # MySQL schema and sample data
├── flightbooking_db.py    # FastAPI backend with dynamic pricing logic
├── frontend/
│   ├── APP.js             # React frontend (animated booking UI)
│   ├── package.json
│   └── tailwind.config.js
└── README.md              # Project documentation
```

---

## 🏁 Final Output Summary

| Module          | Technology                       | Description                                        |
| --------------- | -------------------------------- | -------------------------------------------------- |
| **Database**    | MySQL                            | Stores flights, bookings, passengers, fare history |
| **Backend**     | FastAPI                          | Provides RESTful APIs and dynamic pricing          |
| **Frontend**    | React + Tailwind + Framer Motion | Animated user interface                            |
| **Integration** | Fetch API                        | Connects frontend with backend                     |
| **Receipt**     | JSON File                        | Downloadable booking confirmation                  |

---

## ✨ Conclusion

**Flight Booking Simulator with Dynamic Pricing** successfully demonstrates:

* Real-world airline booking system simulation.
* Dynamic fare computation based on availability and demand.
* Full-stack integration between MySQL, FastAPI, and React.
* Animated, user-friendly booking experience.

---

> ✈️ *“Fly Smart. Book Fast. Experience Dynamic Pricing with SkySwap.”*

```
