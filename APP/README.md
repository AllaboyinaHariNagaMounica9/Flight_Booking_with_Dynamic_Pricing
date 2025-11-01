# 🗄️ FlightBookingDB – Database Documentation

This document describes the **MySQL database** structure for the **SkySwap Flight Booking System**, used in the Infosys Springboard Milestone 4 project.

The database stores all flight, airline, airport, and booking information required for the **backend (FastAPI)** and **frontend (React)** integration.

---

## 🧩 Database Overview

**Database Name:** `FlightBookingDB`

This database is designed to support:
- Real-time flight information
- Airline and airport data
- Passenger and booking details
- Dynamic pricing simulation

---

## 📊 Database Schema

### 1. 🛫 **Airlines Table**
Stores airline company information.

| Column | Type | Constraints | Description |
|---------|------|--------------|--------------|
| `AirlineID` | INT | PRIMARY KEY, AUTO_INCREMENT | Unique airline ID |
| `AirlineName` | VARCHAR(100) | NOT NULL | Name of the airline |
| `Logo` | VARCHAR(255) | NULL | Airline logo URL |

---

### 2. 🏢 **Airports Table**
Stores details about airports and their IATA codes.

| Column | Type | Constraints | Description |
|---------|------|--------------|--------------|
| `AirportID` | INT | PRIMARY KEY, AUTO_INCREMENT | Unique airport ID |
| `AirportName` | VARCHAR(100) | NOT NULL | Airport name |
| `IATA_Code` | VARCHAR(10) | UNIQUE, NOT NULL | IATA airport code (e.g., DEL, HYD) |
| `City` | VARCHAR(100) | NOT NULL | City name of the airport |

---

### 3. ✈️ **Flights Table**
Holds flight-related information, linked to both **Airlines** and **Airports**.

| Column | Type | Constraints | Description |
|---------|------|--------------|--------------|
| `FlightID` | INT | PRIMARY KEY, AUTO_INCREMENT | Unique flight ID |
| `FlightNumber` | VARCHAR(10) | UNIQUE, NOT NULL | Flight number (e.g., SKY301) |
| `AirlineID` | INT | FOREIGN KEY REFERENCES `Airlines(AirlineID)` | Airline operating the flight |
| `SourceAirportID` | INT | FOREIGN KEY REFERENCES `Airports(AirportID)` | Origin airport |
| `DestinationAirportID` | INT | FOREIGN KEY REFERENCES `Airports(AirportID)` | Destination airport |
| `DepartureTime` | DATETIME | NOT NULL | Scheduled departure time |
| `ArrivalTime` | DATETIME | NOT NULL | Scheduled arrival time |
| `TotalSeats` | INT | NOT NULL | Total available seats |
| `BaseFare` | DECIMAL(10,2) | NOT NULL | Base fare for the flight |
| `FlightStatus` | VARCHAR(20) | DEFAULT 'On Time' | Current flight status |

---

### 4. 👤 **Bookings Table**
Stores user bookings and passenger details.

| Column | Type | Constraints | Description |
|---------|------|--------------|--------------|
| `BookingID` | VARCHAR(20) | PRIMARY KEY | Unique booking ID or PNR |
| `FlightID` | INT | FOREIGN KEY REFERENCES `Flights(FlightID)` | Flight booked |
| `PassengerName` | VARCHAR(100) | NOT NULL | Name of the passenger |
| `Age` | INT | NULL | Passenger age |
| `Gender` | VARCHAR(10) | NULL | Gender of passenger |
| `SeatNumber` | VARCHAR(10) | NULL | Assigned seat number |
| `BookingTime` | DATETIME | DEFAULT CURRENT_TIMESTAMP | Timestamp of booking |
| `FarePaid` | DECIMAL(10,2) | NULL | Fare paid at the time of booking |

---

## 🔗 Relationships

- Each **Flight** belongs to one **Airline**  
- Each **Flight** departs from one **Airport** and arrives at another  
- Each **Booking** is linked to one **Flight**  

**ER Diagram Summary:**
```

Airlines (1) ────< Flights >──── (1) Airports
|
|
V
Bookings

````

---

## ⚙️ Setup Instructions

### 1️⃣ Create Database
```bash
CREATE DATABASE FlightBookingDB;
USE FlightBookingDB;
````

### 2️⃣ Import SQL File

Run this command in MySQL CLI or any SQL client:

```bash
SOURCE DATABASE.sql;
```

This will automatically create all tables and sample data if included.

---

## 🧾 Example Queries

### 🔍 View all flights

```sql
SELECT f.FlightNumber, a.AirlineName, s.City AS Source, d.City AS Destination, f.BaseFare
FROM Flights f
JOIN Airlines a ON f.AirlineID = a.AirlineID
JOIN Airports s ON f.SourceAirportID = s.AirportID
JOIN Airports d ON f.DestinationAirportID = d.AirportID;
```

### 🧍 Passenger Bookings

```sql
SELECT BookingID, PassengerName, SeatNumber, FarePaid, BookingTime
FROM Bookings
ORDER BY BookingTime DESC;
```

---

## 🧠 Notes

* Ensure MySQL server is running before backend startup.
* The backend (`flightbooking_db.py`) connects to this database using environment credentials:

  ```python
  MYSQL_USER = "root"
  MYSQL_PASSWORD = "yourpassword"
  MYSQL_DB = "FlightBookingDB"
  MYSQL_HOST = "localhost"
  ```
* You can modify or extend the schema for additional features like **cancellations**, **payments**, or **seat management**.

---

## 🏁 Summary

This database serves as the **core data layer** for the SkySwap Flight Booking System.
It provides structured and relational storage for:

* Flight scheduling
* Passenger management
* Booking history
* Airline and airport data

It ensures reliable integration with the FastAPI backend and React frontend for a complete flight booking experience.

---

**Developer:** Hari Mounica
**College:** Sir C.R. Reddy College of Engineering (JNTUK)
**Project:** Infosys Springboard – Milestone 4 (Weeks 7–8)
**Module:** Database Design and Integration

```
