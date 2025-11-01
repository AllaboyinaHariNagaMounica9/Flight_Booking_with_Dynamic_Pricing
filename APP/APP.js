import React, { useEffect, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";

const API_BASE = "http://localhost:8000"; // Change if backend hosted elsewhere

export default function FlightBookingApp() {
  const [flights, setFlights] = useState([]);
  const [filtered, setFiltered] = useState([]);
  const [query, setQuery] = useState({ from: "", to: "" });
  const [selected, setSelected] = useState(null);
  const [passengers, setPassengers] = useState([]);
  const [step, setStep] = useState("home");
  const [history, setHistory] = useState([]);
  const [paymentMethod, setPaymentMethod] = useState("card");
  const [paymentData, setPaymentData] = useState({
    cardNumber: "",
    expiry: "",
    cvv: "",
  });
  const [lastPNR, setLastPNR] = useState(null);
  const [loadingFlights, setLoadingFlights] = useState(false);

  useEffect(() => {
    loadFlights();
  }, []);

  async function loadFlights() {
    setLoadingFlights(true);
    try {
      const res = await fetch(`${API_BASE}/flights/`);
      const data = await res.json();
      const withPrices = await Promise.all(
        data.map(async (f) => {
          try {
            const p = await fetch(`${API_BASE}/pricing/${f.FlightID}`);
            const d = await p.json();
            return { ...f, BaseFare: d.price || f.BaseFare };
          } catch {
            return f;
          }
        })
      );
      setFlights(withPrices);
      setFiltered(withPrices);
    } catch (e) {
      console.error(e);
    } finally {
      setLoadingFlights(false);
    }
  }

  function searchFlights(e) {
    e.preventDefault();
    const from = query.from.trim().toUpperCase();
    const to = query.to.trim().toUpperCase();
    const res = flights.filter(
      (f) =>
        (!from || f.source_airport.IATA_Code === from) &&
        (!to || f.destination_airport.IATA_Code === to)
    );
    setFiltered(res);
    setStep("search");
  }

  function startBooking(f) {
    setSelected(f);
    setPassengers([{ name: "", age: "", gender: "Male" }]);
    setStep("book");
  }

  function addPassenger() {
    setPassengers((p) => [...p, { name: "", age: "", gender: "Male" }]);
  }

  async function processBooking(e) {
    e.preventDefault();
    const booking = {
      FlightID: selected.FlightID,
      passengers,
    };
    try {
      const res = await fetch(`${API_BASE}/booking/reserve`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(booking),
      });
      const data = await res.json();
      setLastPNR(data.BookingID || `PNR${Math.random().toString(36).slice(2, 8)}`);
      setHistory((h) => [data, ...h]);
      setStep("done");
    } catch (err) {
      console.error(err);
    }
  }

  function downloadReceipt() {
    const receipt = {
      BookingID: lastPNR,
      Flight: selected?.FlightNumber,
      Airline: selected?.airline?.AirlineName,
      Passengers: passengers,
      Time: new Date().toLocaleString(),
    };
    const blob = new Blob([JSON.stringify(receipt, null, 2)], {
      type: "application/json",
    });
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = `${lastPNR}_receipt.json`;
    link.click();
  }

  return (
    <motion.div
      className="min-h-screen bg-gradient-to-br from-sky-100 to-indigo-100"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
    >
      {/* NAVBAR */}
      <motion.nav
        className="bg-white shadow flex justify-between items-center p-4 px-8 sticky top-0 z-50"
        initial={{ y: -80 }}
        animate={{ y: 0 }}
      >
        <div className="flex items-center gap-3">
          <h1 className="text-2xl font-bold text-indigo-700">SkySwap</h1>
          <span className="hidden md:block text-gray-500 text-sm">
            Compare fares - Real-time seats - Hotels
          </span>
        </div>
        <div className="flex gap-4 text-sm">
          <motion.button
            whileHover={{ scale: 1.05 }}
            onClick={() => setStep("home")}
            className="hover:text-indigo-600"
          >
            Home
          </motion.button>
          <motion.button
            whileHover={{ scale: 1.05 }}
            onClick={() => setStep("search")}
            className="hover:text-indigo-600"
          >
            Flights
          </motion.button>
          <motion.button
            whileHover={{ scale: 1.05 }}
            onClick={() => setStep("history")}
            className="hover:text-indigo-600"
          >
            History
          </motion.button>
        </div>
      </motion.nav>

      {/* PAGES */}
      <AnimatePresence mode="wait">
        {step === "home" && (
          <motion.section
            key="home"
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0 }}
            className="p-10 text-center"
          >
            <h2 className="text-4xl font-extrabold text-indigo-700 mb-4">
              Explore the world with SkySwap
            </h2>
            <p className="text-gray-700 mb-6">
              Book flights, discover destinations, and enjoy exclusive offers.
            </p>
            <motion.button
              whileHover={{ scale: 1.05 }}
              onClick={() => setStep("search")}
              className="bg-indigo-600 text-white px-6 py-3 rounded-lg shadow-lg hover:bg-indigo-700 transition"
            >
              Search Flights
            </motion.button>
          </motion.section>
        )}

        {step === "search" && (
          <motion.section
            key="search"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="max-w-5xl mx-auto p-8"
          >
            <form
              onSubmit={searchFlights}
              className="flex flex-col md:flex-row gap-4 justify-center mb-6"
            >
              <input
                placeholder="From (IATA)"
                value={query.from}
                onChange={(e) => setQuery({ ...query, from: e.target.value })}
                className="border rounded p-2 w-full md:w-1/3 focus:ring-2 focus:ring-indigo-400"
              />
              <input
                placeholder="To (IATA)"
                value={query.to}
                onChange={(e) => setQuery({ ...query, to: e.target.value })}
                className="border rounded p-2 w-full md:w-1/3 focus:ring-2 focus:ring-indigo-400"
              />
              <button
                type="submit"
                className="bg-indigo-600 text-white px-6 py-2 rounded-lg hover:bg-indigo-700 transition"
              >
                Search
              </button>
            </form>

            {loadingFlights ? (
              <div className="text-center text-gray-500">Loading flights...</div>
            ) : filtered.length === 0 ? (
              <div className="text-center text-gray-600">No flights found.</div>
            ) : (
              <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
                {filtered.map((f) => (
                  <motion.div
                    key={f.FlightID}
                    whileHover={{ scale: 1.03 }}
                    className="p-4 rounded-xl shadow-lg bg-white bg-opacity-90 backdrop-blur"
                  >
                    <div className="flex justify-between items-center">
                      <div>
                        <div className="font-bold text-indigo-700">{f.FlightNumber}</div>
                        <div className="text-xs text-gray-500">
                          {f.source_airport.IATA_Code} to {f.destination_airport.IATA_Code}
                        </div>
                      </div>
                      <div className="font-bold text-emerald-700">Rs {f.BaseFare}</div>
                    </div>
                    <div className="mt-3 text-right">
                      <button
                        onClick={() => startBooking(f)}
                        className="bg-emerald-500 text-white px-3 py-1 rounded hover:bg-emerald-600"
                      >
                        Book
                      </button>
                    </div>
                  </motion.div>
                ))}
              </div>
            )}
          </motion.section>
        )}

        {step === "book" && selected && (
          <motion.section
            key="book"
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0 }}
            className="max-w-3xl mx-auto p-6 bg-white rounded-2xl shadow-lg mt-8"
          >
            <h2 className="text-2xl font-bold text-center text-indigo-700 mb-4">
              Passenger Details
            </h2>
            <form onSubmit={(e) => setStep("payment")}>
              {passengers.map((p, i) => (
                <div key={i} className="mb-3 border p-3 rounded-lg">
                  <input
                    placeholder="Name"
                    value={p.name}
                    onChange={(e) =>
                      setPassengers((ps) =>
                        ps.map((x, j) => (i === j ? { ...x, name: e.target.value } : x))
                      )
                    }
                    className="border p-2 rounded w-full mb-2"
                  />
                  <input
                    placeholder="Age"
                    type="number"
                    value={p.age}
                    onChange={(e) =>
                      setPassengers((ps) =>
                        ps.map((x, j) => (i === j ? { ...x, age: e.target.value } : x))
                      )
                    }
                    className="border p-2 rounded w-full mb-2"
                  />
                  <select
                    value={p.gender}
                    onChange={(e) =>
                      setPassengers((ps) =>
                        ps.map((x, j) => (i === j ? { ...x, gender: e.target.value } : x))
                      )
                    }
                    className="border p-2 rounded w-full"
                  >
                    <option>Male</option>
                    <option>Female</option>
                    <option>Other</option>
                  </select>
                </div>
              ))}
              <div className="flex justify-between mt-4">
                <button
                  type="button"
                  onClick={addPassenger}
                  className="bg-gray-100 px-4 py-2 rounded hover:bg-gray-200"
                >
                  + Add Passenger
                </button>
                <button
                  type="submit"
                  className="bg-indigo-600 text-white px-6 py-2 rounded hover:bg-indigo-700"
                >
                  Continue to Payment
                </button>
              </div>
            </form>
          </motion.section>
        )}

        {step === "payment" && (
          <motion.section
            key="payment"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="min-h-screen flex items-center justify-center"
          >
            <div className="bg-white p-8 rounded-xl shadow-lg w-full max-w-md">
              <h2 className="text-xl font-bold text-center text-indigo-700 mb-4">
                Secure Payment
              </h2>
              <form onSubmit={processBooking} className="space-y-3">
                <input
                  placeholder="Card Number"
                  value={paymentData.cardNumber}
                  onChange={(e) =>
                    setPaymentData({ ...paymentData, cardNumber: e.target.value })
                  }
                  className="border rounded p-2 w-full"
                  required
                />
                <div className="flex gap-2">
                  <input
                    placeholder="MM/YY"
                    value={paymentData.expiry}
                    onChange={(e) =>
                      setPaymentData({ ...paymentData, expiry: e.target.value })
                    }
                    className="border rounded p-2 w-1/2"
                    required
                  />
                  <input
                    placeholder="CVV"
                    type="password"
                    value={paymentData.cvv}
                    onChange={(e) =>
                      setPaymentData({ ...paymentData, cvv: e.target.value })
                    }
                    className="border rounded p-2 w-1/2"
                    required
                  />
                </div>
                <button
                  type="submit"
                  className="bg-indigo-600 text-white w-full py-2 rounded hover:bg-indigo-700"
                >
                  Pay and Confirm
                </button>
              </form>
            </div>
          </motion.section>
        )}

        {step === "done" && (
          <motion.section
            key="done"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="max-w-md mx-auto text-center mt-20 bg-gradient-to-br from-green-200 to-emerald-100 p-8 rounded-2xl shadow-xl"
          >
            <h2 className="text-2xl font-bold text-green-700 mb-2">
              Booking Confirmed
            </h2>
            <p className="text-gray-700 mb-4">
              PNR: <span className="font-mono">{lastPNR}</span>
            </p>
            <div className="flex justify-center gap-3">
              <button
                onClick={() => setStep("search")}
                className="bg-indigo-600 text-white px-5 py-2 rounded-lg hover:bg-indigo-700"
              >
                Book Another
              </button>
              <button
                onClick={downloadReceipt}
                className="bg-white border px-5 py-2 rounded-lg hover:bg-gray-100"
              >
                Download Receipt
              </button>
            </div>
          </motion.section>
        )}

        {step === "history" && (
          <motion.section
            key="history"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="max-w-3xl mx-auto p-8"
          >
            <h2 className="text-2xl font-bold text-indigo-700 mb-4">Booking History</h2>
            {history.length === 0 ? (
              <div className="text-gray-600">No previous bookings.</div>
            ) : (
              history.map((h, i) => (
                <div key={i} className="bg-white p-4 rounded-xl shadow mb-3">
                  <div className="flex justify-between">
                    <div>
                      <div className="font-bold">{h.FlightNumber}</div>
                      <div className="text-sm text-gray-500">{h.Route}</div>
                    </div>
                    <div className="font-mono text-sm">{h.BookingID}</div>
                  </div>
                </div>
              ))
            )}
          </motion.section>
        )}
      </AnimatePresence>
    </motion.div>
  );
}
