# 🎨 SkySwap Frontend – Flight Booking System (React)

This is the **frontend user interface** for the **SkySwap Flight Booking System**, built with **React**, **Tailwind CSS**, and **Framer Motion**.  
It provides an animated, interactive, and user-friendly interface for searching, booking, and managing flight reservations.

---

## ✈️ Overview

The **SkySwap Frontend** connects to the FastAPI backend and database to deliver a complete real-time flight booking simulation.  
It allows users to:

- 🔍 Search for flights between cities  
- 💸 View dynamic pricing fetched from backend APIs  
- 🧾 Book flights through an interactive multi-step form  
- 💳 Simulate payments securely  
- 📄 Download digital booking receipts (JSON format)  
- 🕓 Review booking history  

---

## 🧩 Tech Stack

| Component | Technology |
|------------|-------------|
| **Frontend Framework** | React (Functional Components + Hooks) |
| **Styling** | Tailwind CSS |
| **Animations** | Framer Motion |
| **API Integration** | Fetch API |
| **Backend Base URL** | `http://localhost:8000` (FastAPI) |

---

## ⚙️ Setup Instructions

### 1️⃣ Prerequisites
Make sure you have:
- Node.js 18+  
- npm or yarn  
- Backend running at `http://localhost:8000`  

---

### 2️⃣ Installation

Clone and install dependencies:

```bash
git clone https://github.com/your-username/FlightBooking-Frontend.git
cd FlightBooking-Frontend
npm install
````

---

### 3️⃣ Run the Frontend

```bash
npm start
```

Then open your browser at:

```
http://localhost:3000
```

The app will automatically connect to the backend (`http://localhost:8000`) for flight data and bookings.

---

## 🧠 File Structure

```
frontend/
│
├── APP.js              # Main React component (full UI + logic)
├── index.js            # App entry point
├── package.json        # Dependencies and scripts
├── public/             # Static assets
└── tailwind.config.js  # Tailwind configuration
```

---

## 💡 Features

✅ **Animated Home Page** – Smooth motion transitions using Framer Motion
✅ **Flight Search** – Users can search by IATA airport codes
✅ **Dynamic Pricing** – Real-time fare updates fetched from backend
✅ **Multi-Step Booking Flow** – Search → Booking → Payment → Confirmation
✅ **JSON Receipt Download** – Digital booking receipt generation
✅ **Booking History Page** – Displays all past reservations
✅ **Fully Responsive Design** – Works on desktop and mobile

---

## 🔗 API Integration Points

| Purpose              | Method | Endpoint               |
| -------------------- | ------ | ---------------------- |
| Fetch all flights    | `GET`  | `/flights/`            |
| Get flight pricing   | `GET`  | `/pricing/{flight_id}` |
| Create a new booking | `POST` | `/booking/reserve`     |

All APIs are fetched from the backend defined in:

```js
const API_BASE = "http://localhost:8000";
```

---

## 🎨 UI Pages

1️⃣ **Home Page** – Animated landing with a call-to-action button
2️⃣ **Flight Search Page** – Search by source and destination
3️⃣ **Booking Page** – Passenger entry and seat selection
4️⃣ **Payment Page** – Secure payment simulation
5️⃣ **Confirmation Page** – Displays generated PNR and allows receipt download
6️⃣ **History Page** – Shows previous booking details

---

## 🧾 Example Receipt (JSON)

```json
{
  "BookingID": "PNR47GFZ2",
  "Flight": "AI302",
  "Airline": "Air India",
  "Passengers": [
    { "name": "Hari", "age": 24, "gender": "Female" }
  ],
  "Time": "2025-11-01T18:23:00"
}
```

---

## 🧠 Notes

* Ensure the backend server (`FastAPI`) is **running first** before launching the frontend.
* You can edit the base API URL in `APP.js` if the backend is hosted remotely.
* The app uses **Tailwind CSS utility classes** for styling and **Framer Motion** for animations.

---

## 👩‍💻 Developer

**Name:** Hari Mounica
**College:** Sir C.R. Reddy College of Engineering (JNTUK)
**Course:** B.Tech – Computer Science Engineering (3rd Year)
**Project:** Infosys Springboard – Milestone 4 (Weeks 7–8)
**Module:** Frontend UI & API Integration

---

### ✨ “Fast. Animated. Interactive. Welcome aboard SkySwap!”

```
