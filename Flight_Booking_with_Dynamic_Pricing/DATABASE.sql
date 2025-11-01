CREATE DATABASE FlightBookingDB;
USE FlightBookingDB;

CREATE TABLE Airline (
    AirlineID INT IDENTITY PRIMARY KEY,
    AirlineName VARCHAR(100) NOT NULL,
    ContactEmail VARCHAR(100),
    ContactNumber VARCHAR(15)
);
CREATE TABLE Airport (
    AirportID INT IDENTITY PRIMARY KEY,
    AirportName VARCHAR(100) NOT NULL,
    City VARCHAR(50),
    Country VARCHAR(50),
    IATA_Code CHAR(3) UNIQUE
);
CREATE TABLE Flight (
    FlightID INT IDENTITY PRIMARY KEY,
    AirlineID INT,
    FlightNumber VARCHAR(10) UNIQUE NOT NULL,
    SourceAirportID INT,
    DestinationAirportID INT,
    DepartureTime DATETIME,
    ArrivalTime DATETIME,
    TotalSeats INT,
    AvailableSeats INT,
    BaseFare DECIMAL(10,2),
    FOREIGN KEY (AirlineID) REFERENCES Airline(AirlineID),
    FOREIGN KEY (SourceAirportID) REFERENCES Airport(AirportID),
    FOREIGN KEY (DestinationAirportID) REFERENCES Airport(AirportID)
);
CREATE TABLE [User] (
    UserID INT IDENTITY(1,1) PRIMARY KEY,
    FullName VARCHAR(100),
    Email VARCHAR(100) UNIQUE,
    Password VARCHAR(255),
    Phone VARCHAR(15),
    Role VARCHAR(10) DEFAULT 'User' CHECK (Role IN ('Admin', 'User'))
);
CREATE TABLE DynamicPricing (
    PricingID INT IDENTITY PRIMARY KEY,
    FlightID INT,
    Timestamp DATETIME,
    DemandFactor DECIMAL(5,2),
    TimeToDepartureFactor DECIMAL(5,2),
    SeatAvailabilityFactor DECIMAL(5,2),
    FinalFare DECIMAL(10,2),
    FOREIGN KEY (FlightID) REFERENCES Flight(FlightID)
);
CREATE TABLE Booking (
    BookingID INT IDENTITY(1,1) PRIMARY KEY,
    UserID INT,
    FlightID INT,
    BookingDate DATETIME,
    TotalFare DECIMAL(10,2),
    Status VARCHAR(10) DEFAULT 'Confirmed' CHECK (Status IN ('Confirmed', 'Cancelled')),
    FOREIGN KEY (UserID) REFERENCES [User](UserID),
    FOREIGN KEY (FlightID) REFERENCES Flight(FlightID)
);
CREATE TABLE Passenger (
    PassengerID INT IDENTITY PRIMARY KEY,
    BookingID INT,
    PassengerName VARCHAR(100),
    Age INT,
    Gender VARCHAR(10) CHECK (Gender IN ('Male','Female','Other')),
    SeatNumber VARCHAR(5),
    FOREIGN KEY (BookingID) REFERENCES Booking(BookingID)
);
CREATE TABLE Payment (
    PaymentID INT IDENTITY(1,1) PRIMARY KEY,
    BookingID INT,
    PaymentDate DATETIME,
    Amount DECIMAL(10,2),
    PaymentMode VARCHAR(20) CHECK (PaymentMode IN ('CreditCard','DebitCard','UPI','Wallet')),
    PaymentStatus VARCHAR(10) DEFAULT 'Success' CHECK (PaymentStatus IN ('Success','Failed','Pending')),
    FOREIGN KEY (BookingID) REFERENCES Booking(BookingID)
);
UPDATE Flight
SET AvailableSeats = AvailableSeats - 2
WHERE FlightNumber = 'AI101';

DELETE FROM Passenger
WHERE PassengerID = 5;

ALTER TABLE Flight
ADD FlightStatus VARCHAR(10) DEFAULT 'On Time' CHECK (FlightStatus IN ('On Time','Delayed','Cancelled'));

INSERT INTO DynamicPricing 
    (FlightID, Timestamp, DemandFactor, TimeToDepartureFactor, SeatAvailabilityFactor, FinalFare)
VALUES 
    (1, GETDATE(), 1.2, 1.1, 0.9, 5400.00);

SELECT U.FullName, B.BookingID, F.FlightNumber, B.Status
FROM [User] U
JOIN Booking B ON U.UserID = B.UserID
JOIN Flight F ON F.FlightID = B.FlightID;

SELECT F.FlightNumber, A.AirlineName
FROM Flight F
LEFT JOIN Airline A ON F.AirlineID = A.AirlineID;

SELECT B.BookingID, U.FullName, P.PaymentStatus
FROM Booking B
RIGHT JOIN Payment P ON B.BookingID = P.BookingID
JOIN [User] U ON B.UserID = U.UserID;

SELECT U.FullName, A.AirlineName, F.FlightNumber, D.FinalFare
FROM [User] U
JOIN Booking B ON U.UserID = B.UserID
JOIN Flight F ON B.FlightID = F.FlightID
JOIN Airline A ON F.AirlineID = A.AirlineID
JOIN DynamicPricing D ON F.FlightID = D.FlightID
WHERE B.Status = 'Confirmed';

CREATE VIEW FlightSummary AS
SELECT F.FlightNumber, A.AirlineName, F.DepartureTime, F.AvailableSeats, F.BaseFare
FROM Flight F
JOIN Airline A ON F.AirlineID = A.AirlineID;

SELECT name AS FlightBookingDB
FROM sys.databases;


USE FlightBookingDB;
GO

SELECT TABLE_NAME
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_TYPE = 'BASE TABLE';

SELECT TABLE_NAME, COLUMN_NAME, DATA_TYPE, IS_NULLABLE
FROM INFORMATION_SCHEMA.COLUMNS
ORDER BY TABLE_NAME;

-- View data in User table
SELECT * FROM [User];

-- View data in Flight table
SELECT * FROM Flight;

-- View data in Booking table
SELECT * FROM Booking;

-- View data in Passenger table
SELECT * FROM Passenger;

-- View data in Payment table
SELECT * FROM Payment;

-- View data in DynamicPricing table
SELECT * FROM DynamicPricing;

SELECT TOP 10 * FROM Booking;

SELECT t.name AS TableName,
       SUM(p.rows) AS TotalRows
FROM sys.tables t
JOIN sys.partitions p 
  ON t.object_id = p.object_id
WHERE p.index_id IN (0,1)  -- 0 = Heap, 1 = Clustered
GROUP BY t.name
ORDER BY t.name;

