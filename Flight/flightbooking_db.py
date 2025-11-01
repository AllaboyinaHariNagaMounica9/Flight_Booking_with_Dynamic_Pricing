import nest_asyncio
from fastapi import FastAPI, HTTPException, Depends, status, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import (
    create_engine, Column, Integer, String, Float, DateTime, DECIMAL,
    ForeignKey, func, CheckConstraint
)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker, Session
from pydantic import BaseModel, Field, EmailStr, ConfigDict
from datetime import datetime, timedelta
from typing import Optional, List
from contextlib import asynccontextmanager
import random
import uuid
import decimal
import string
import threading
import time

nest_asyncio.apply()


DATABASE_URL = "sqlite:///./infosys_flight_db.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {},
    echo=False
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



class Airline(Base):
    __tablename__ = "Airline"
    AirlineID = Column(Integer, primary_key=True, autoincrement=True)
    AirlineName = Column(String(100), nullable=False)
    ContactEmail = Column(String(100))
    ContactNumber = Column(String(15))
    flights = relationship("Flight", back_populates="airline")

class Airport(Base):
    __tablename__ = "Airport"
    AirportID = Column(Integer, primary_key=True, autoincrement=True)
    AirportName = Column(String(100), nullable=False)
    City = Column(String(50))
    Country = Column(String(50))
    IATA_Code = Column(String(3), unique=True)
    departures = relationship("Flight", back_populates="source_airport", foreign_keys="Flight.SourceAirportID")
    arrivals = relationship("Flight", back_populates="destination_airport", foreign_keys="Flight.DestinationAirportID")

class Flight(Base):
    __tablename__ = "Flight"
    FlightID = Column(Integer, primary_key=True, autoincrement=True)
    AirlineID = Column(Integer, ForeignKey("Airline.AirlineID"))
    FlightNumber = Column(String(10), unique=True, nullable=False)
    SourceAirportID = Column(Integer, ForeignKey("Airport.AirportID"))
    DestinationAirportID = Column(Integer, ForeignKey("Airport.AirportID"))
    DepartureTime = Column(DateTime)
    ArrivalTime = Column(DateTime)
    TotalSeats = Column(Integer)
    AvailableSeats = Column(Integer)
    BaseFare = Column(DECIMAL(10, 2))

    FlightStatus = Column(String(10), default='On Time')
    __table_args__ = (
        CheckConstraint(FlightStatus.in_(['On Time', 'Delayed', 'Cancelled']), name='flight_status_check'),
    )

    airline = relationship("Airline", back_populates="flights")
    source_airport = relationship("Airport", foreign_keys=[SourceAirportID], back_populates="departures")
    destination_airport = relationship("Airport", foreign_keys=[DestinationAirportID], back_populates="arrivals")
    bookings = relationship("Booking", back_populates="flight")
    pricings = relationship("DynamicPricing", back_populates="flight")

class User(Base):
    __tablename__ = "User"
    UserID = Column(Integer, primary_key=True, autoincrement=True)
    FullName = Column(String(100))
    Email = Column(String(100), unique=True)
    Password = Column(String(255))
    Phone = Column(String(15))
    Role = Column(String(10), default='User')
    __table_args__ = (
        CheckConstraint(Role.in_(['Admin', 'User']), name='user_role_check'),
    )
    bookings = relationship("Booking", back_populates="user")

class DynamicPricing(Base):
    __tablename__ = "DynamicPricing"
    PricingID = Column(Integer, primary_key=True, autoincrement=True)
    FlightID = Column(Integer, ForeignKey("Flight.FlightID"))

    Timestamp = Column(DateTime, default=datetime.utcnow)
    DemandFactor = Column(DECIMAL(5, 2))
    TimeToDepartureFactor = Column(DECIMAL(5, 2))
    SeatAvailabilityFactor = Column(DECIMAL(5, 2))
    FinalFare = Column(DECIMAL(10, 2))

    flight = relationship("Flight", back_populates="pricings")

class Booking(Base):
    __tablename__ = "Booking"
    BookingID = Column(Integer, primary_key=True, autoincrement=True)
    UserID = Column(Integer, ForeignKey("User.UserID"))
    FlightID = Column(Integer, ForeignKey("Flight.FlightID"))
    BookingDate = Column(DateTime, default=datetime.utcnow)
    TotalFare = Column(DECIMAL(10, 2))
    Status = Column(String(10), default='Confirmed')
    __table_args__ = (
        CheckConstraint(Status.in_(['Confirmed', 'Cancelled']), name='booking_status_check'),
    )
    user = relationship("User", back_populates="bookings")
    flight = relationship("Flight", back_populates="bookings")
    passengers = relationship("Passenger", back_populates="booking")
    payments = relationship("Payment", back_populates="booking")

class Passenger(Base):
    __tablename__ = "Passenger"
    PassengerID = Column(Integer, primary_key=True, autoincrement=True)
    BookingID = Column(Integer, ForeignKey("Booking.BookingID"))
    PassengerName = Column(String(100))
    Age = Column(Integer)
    Gender = Column(String(10))

    SeatNumber = Column(String(5))
    __table_args__ = (
        CheckConstraint(Gender.in_(['Male', 'Female', 'Other']), name='passenger_gender_check'),
    )
    booking = relationship("Booking", back_populates="passengers")


class Payment(Base):
    __tablename__ = "Payment"
    PaymentID = Column(Integer, primary_key=True, autoincrement=True)
    BookingID = Column(Integer, ForeignKey("Booking.BookingID"))
    PaymentDate = Column(DateTime)
    Amount = Column(DECIMAL(10, 2))
    PaymentMode = Column(String(20))
    PaymentStatus = Column(String(10), default='Success')
    __table_args__ = (
        CheckConstraint(PaymentMode.in_(['CreditCard', 'DebitCard', 'UPI', 'Wallet']), name='payment_mode_check'),
        CheckConstraint(PaymentStatus.in_(['Success', 'Failed', 'Pending']), name='payment_status_check'),
    )
    booking = relationship("Booking", back_populates="payments")



Base.metadata.create_all(engine)




class AirlineSchema(BaseModel):
    AirlineID: Optional[int] = None
    AirlineName: str
    ContactEmail: Optional[EmailStr] = None
    ContactNumber: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

class AirportSchema(BaseModel):
    AirportID: Optional[int] = None
    AirportName: str
    City: str
    Country: str
    IATA_Code: str
    model_config = ConfigDict(from_attributes=True)

class FlightSchema(BaseModel):
    FlightID: Optional[int] = None
    FlightNumber: str
    AirlineID: int
    SourceAirportID: int
    DestinationAirportID: int
    DepartureTime: datetime
    ArrivalTime: datetime
    BaseFare: float
    TotalSeats: int
    AvailableSeats: int
    FlightStatus: str = 'On Time'
    model_config = ConfigDict(from_attributes=True)

class UserSchema(BaseModel):
    UserID: Optional[int] = None
    FullName: str
    Email: EmailStr
    Password: str
    Phone: Optional[str] = None
    Role: str = 'User'
    model_config = ConfigDict(from_attributes=True)

class BookingCreateSchema(BaseModel):
    UserID: int
    FlightID: int

    model_config = ConfigDict(from_attributes=True)

class PassengerCreateSchema(BaseModel):
    PassengerName: str
    Age: int
    Gender: str
    SeatNumber: str
    model_config = ConfigDict(from_attributes=True)

class CompleteBookingRequest(BaseModel):
    booking_details: BookingCreateSchema
    passengers: List[PassengerCreateSchema]

class BookingOutSchema(BaseModel):
    BookingID: int
    UserID: int
    FlightID: int
    BookingDate: datetime
    TotalFare: float
    Status: str
    passengers: List[PassengerCreateSchema]
    model_config = ConfigDict(from_attributes=True)



def calculate_dynamic_price(base_fare: decimal.Decimal, seats_available: int, total_seats: int, departure: datetime, flight_number: str) -> float:
    base = float(base_fare)
    seat_ratio = seats_available / total_seats if total_seats else 0
    seat_factor = 0.4 * (1 - seat_ratio)
    days = (departure - datetime.now()).total_seconds() / 86400 if departure else 0
    if days <= 0: time_factor = 0.6
    elif days <= 1: time_factor = 0.4
    elif days <= 3: time_factor = 0.2
    elif days <= 7: time_factor = 0.1
    else: time_factor = -0.05
    demand_factor = random.uniform(-0.08, 0.25)

    tier_factor = 0.12 if "premium" in flight_number.lower() or "ai" in flight_number.lower() else -0.03
    total_multiplier = 1 + seat_factor + time_factor + demand_factor + tier_factor
    return max(round(base * total_multiplier, 2), 50.0)

def generate_transaction_id() -> str:
    return str(uuid.uuid4()).replace('-', '')[:20]


def insert_initial_data(db: Session):
    if db.query(Airline).count() == 0:
        airlines = [
            Airline(AirlineName="AirIndia", ContactEmail="info@airindia.com"),
            Airline(AirlineName="Indigo", ContactEmail="support@goindigo.in"),
            Airline(AirlineName="SpiceJet", ContactEmail="help@spicejet.com"),
        ]
        db.add_all(airlines)
        db.commit()

    if db.query(Airport).count() == 0:
        airports = [
            Airport(AirportName="Chhatrapati Shivaji Maharaj International", City="Mumbai", Country="India", IATA_Code="BOM"),
            Airport(AirportName="Indira Gandhi International", City="New Delhi", Country="India", IATA_Code="DEL"),
            Airport(AirportName="Kempegowda International", City="Bengaluru", Country="India", IATA_Code="BLR"),
        ]
        db.add_all(airports)
        db.commit()

    if db.query(Flight).count() == 0:

        ai_id = db.query(Airline.AirlineID).filter(Airline.AirlineName == "AirIndia").scalar()
        bom_id = db.query(Airport.AirportID).filter(Airport.IATA_Code == "BOM").scalar()
        del_id = db.query(Airport.AirportID).filter(Airport.IATA_Code == "DEL").scalar()

        flights = [
            Flight(FlightID=1, FlightNumber="AI101", AirlineID=ai_id, SourceAirportID=del_id, DestinationAirportID=bom_id,
                   DepartureTime=datetime.utcnow() + timedelta(days=2), ArrivalTime=datetime.utcnow() + timedelta(days=2, hours=2),
                   BaseFare=decimal.Decimal("5000.00"), TotalSeats=100, AvailableSeats=100),
        ]
        db.add_all(flights)
        db.commit()


        flight1 = db.query(Flight).filter(Flight.FlightID == 1).one()
        db.add(DynamicPricing(
            FlightID=flight1.FlightID, Timestamp=datetime.utcnow(),
            DemandFactor=decimal.Decimal("1.2"), TimeToDepartureFactor=decimal.Decimal("1.1"),
            SeatAvailabilityFactor=decimal.Decimal("0.9"), FinalFare=decimal.Decimal("5400.00")
        ))
        db.commit()

    if db.query(User).count() == 0:
        users = [
            User(FullName="Sample User", Email="user@example.com", Password="hashed_password", Role="User"),
        ]
        db.add_all(users)
        db.commit()


@asynccontextmanager
async def lifespan(app: FastAPI):

    db = SessionLocal()
    try:
        insert_initial_data(db)
    finally:
        db.close()

    yield


app = FastAPI(title="Infosys Flight Management API (SQL Match)", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/")
def root():
    return {"message": "Flight Booking API running (SQL Schema Matched)"}

@app.get("/airlines", response_model=List[AirlineSchema])
def list_airlines(db: Session = Depends(get_db)):
    return db.query(Airline).all()

@app.post("/airlines", response_model=AirlineSchema)
def create_airline(airline: AirlineSchema, db: Session = Depends(get_db)):
    new_airline = Airline(**airline.model_dump(exclude_none=True))
    db.add(new_airline)
    db.commit()
    db.refresh(new_airline)
    return new_airline

@app.get("/airports", response_model=List[AirportSchema])
def list_airports(db: Session = Depends(get_db)):
    return db.query(Airport).all()

@app.get("/flights/", response_model=List[FlightSchema])
def list_flights(db: Session = Depends(get_db)):
    return db.query(Flight).all()

@app.get("/pricing/{flight_id}", response_model=float)
def get_pricing(flight_id: int, db: Session = Depends(get_db)):
    flight = db.query(Flight).filter(Flight.FlightID == flight_id).first()
    if not flight:
        raise HTTPException(status_code=404, detail="Flight not found")

    dp = calculate_dynamic_price(flight.BaseFare, flight.AvailableSeats, flight.TotalSeats or 1, flight.DepartureTime, flight.FlightNumber)
    return dp

@app.post("/booking/reserve", response_model=BookingOutSchema, status_code=status.HTTP_201_CREATED)
def reserve_booking(payload: CompleteBookingRequest, db: Session = Depends(get_db)):
    """Handles booking creation and passenger addition in a single transaction."""


    flight = db.query(Flight).filter(Flight.FlightID == payload.booking_details.FlightID).with_for_update().first()
    if not flight:
        raise HTTPException(status_code=404, detail="Flight not found")

    required_seats = len(payload.passengers)
    if required_seats <= 0:
        raise HTTPException(status_code=400, detail="Must include at least one passenger.")

    if flight.AvailableSeats < required_seats:
        raise HTTPException(status_code=400, detail="Not enough seats available.")


    dynamic_price_per_seat = calculate_dynamic_price(flight.BaseFare, flight.AvailableSeats, flight.TotalSeats, flight.DepartureTime, flight.FlightNumber)
    total_fare = decimal.Decimal(str(dynamic_price_per_seat * required_seats))


    new_booking = Booking(
        UserID=payload.booking_details.UserID,
        FlightID=flight.FlightID,
        TotalFare=total_fare,
        Status='Confirmed'
    )
    db.add(new_booking)
    db.flush()


    passenger_models = []
    for passenger_data in payload.passengers:
        passenger = Passenger(BookingID=new_booking.BookingID, **passenger_data.model_dump())
        passenger_models.append(passenger)

    db.add_all(passenger_models)


    flight.AvailableSeats -= required_seats

    db.commit()
    db.refresh(new_booking)


    full_booking = db.query(Booking).filter(Booking.BookingID == new_booking.BookingID).one()

    return full_booking

@app.get("/bookings/{booking_id}", response_model=BookingOutSchema)
def get_booking_by_id(booking_id: int, db: Session = Depends(get_db)):
    booking = db.query(Booking).filter(Booking.BookingID == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking

@app.delete("/bookings/cancel/{booking_id}")
def cancel_booking(booking_id: int, db: Session = Depends(get_db)):
    try:
        booking = db.query(Booking).filter(Booking.BookingID == booking_id, Booking.Status != 'Cancelled').with_for_update().first()
        if not booking:
            raise HTTPException(status_code=404, detail="Active booking not found")

        flight = db.query(Flight).filter(Flight.FlightID == booking.FlightID).with_for_update().first()


        passenger_count = db.query(Passenger).filter(Passenger.BookingID == booking.BookingID).count()

        if flight and passenger_count > 0:
            flight.AvailableSeats = min(flight.TotalSeats or 0, (flight.AvailableSeats or 0) + passenger_count)

        booking.Status = "Cancelled"
        db.commit()
        return {"message": f"Booking {booking_id} cancelled. {passenger_count} seats restored.", "booking_id": booking_id}
    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Cancellation failed: {e}")
