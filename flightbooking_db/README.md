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
