from datetime import datetime, timedelta
from typing import Dict, List
import random

class Seat:
    def __init__(self, seat_number: str, seat_class: str):
        self.seat_number = seat_number
        self.seat_class = seat_class
        self.is_occupied = False
        self.passenger_name = None

    def __str__(self):
        status = f"Occupied by {self.passenger_name}" if self.is_occupied else "Available"
        return f"Seat {self.seat_number} ({self.seat_class}): {status}"

class Flight:
    def __init__(self, flight_number: str, origin: str, destination: str, departure_time: datetime):
        self.flight_number = flight_number
        self.origin = origin
        self.destination = destination
        self.departure_time = departure_time
        self.seats: Dict[str, Seat] = {}
        self._initialize_seats()

    def _initialize_seats(self):
        # Initialize first class (rows 1-2)
        for row in range(1, 3):
            for col in ['A', 'B', 'E', 'F']:
                seat_number = f"{row}{col}"
                self.seats[seat_number] = Seat(seat_number, "first")

        # Initialize business class (rows 3-7)
        for row in range(3, 8):
            for col in ['A', 'B', 'E', 'F']:
                seat_number = f"{row}{col}"
                self.seats[seat_number] = Seat(seat_number, "business")

        # Initialize economy class (rows 8-30)
        for row in range(8, 31):
            for col in ['A', 'B', 'C', 'D', 'E', 'F']:
                seat_number = f"{row}{col}"
                self.seats[seat_number] = Seat(seat_number, "economy")

    def get_available_seats(self, seat_class: str = None) -> List[Seat]:
        available_seats = []
        for seat in self.seats.values():
            if not seat.is_occupied:
                if seat_class is None or seat.seat_class == seat_class:
                    available_seats.append(seat)
        return available_seats

    def get_seat(self, seat_number: str) -> Seat:
        return self.seats.get(seat_number)

    def book_seat(self, seat_number: str, passenger_name: str) -> bool:
        if seat_number not in self.seats:
            raise ValueError("Invalid seat number")
        
        seat = self.seats[seat_number]
        if seat.is_occupied:
            return False
        
        seat.is_occupied = True
        seat.passenger_name = passenger_name
        return True

    def __str__(self):
        return (f"Flight {self.flight_number}\n"
                f"From: {self.origin} To: {self.destination}\n"
                f"Departure: {self.departure_time.strftime('%Y-%m-%d %H:%M')}")

class BookingSystem:
    def __init__(self):
        self.flights: Dict[str, Flight] = {}
        self.airlines = ["AA", "UA", "DL", "BA", "LH", "SA", "NA"]  # Generate diff airline codes

    def generate_flight_number(self):
        airline = random.choice(self.airlines)
        number = random.randint(1000, 9999)
        return f"{airline}{number}"

    def generate_departure_times(self, num_flights=3):
        """Generate a list of departure times within the next 30 days"""
        departure_times = []
        for _ in range(num_flights):
            days_ahead = random.randint(1, 30)
            hours = random.randint(0, 23)
            minutes = random.choice([0, 15, 30, 45])
            departure_time = datetime.now() + timedelta(days=days_ahead)
            departure_time = departure_time.replace(hour=hours, minute=minutes)
            departure_times.append(departure_time)
        return sorted(departure_times)

    def search_flights(self, origin: str, destination: str) -> List[Flight]:
        # Clear existing flights and generate new ones for the search
        self.flights.clear()
        
        # Generate 3 flights for the requested route
        departure_times = self.generate_departure_times(3)
        
        for departure_time in departure_times:
            flight_number = self.generate_flight_number()
            flight = Flight(flight_number, origin, destination, departure_time)
            self.flights[flight_number] = flight
        
        return list(self.flights.values())

    def book_flight(self, flight_number: str, seat_number: str, passenger_name: str) -> bool:
        if flight_number not in self.flights:
            raise ValueError("Invalid flight number")
        
        success = self.flights[flight_number].book_seat(seat_number, passenger_name)
        if success:
            seat = self.flights[flight_number].get_seat(seat_number)
            print(f"\nBooking details:")
            print(seat)
        else:
            print(f"\nBooking failed: Seat {seat_number} is already occupied")
        return success

def main():
    booking_system = BookingSystem()
    
    while True:
        print("\n=== Flight Booking System ===")
        print("1. Search flights")
        print("2. View available seats")
        print("3. Book a seat")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ")
        
        if choice == "1":
            origin = input("Enter origin city: ").title()
            destination = input("Enter destination city: ").title()
            flights = booking_system.search_flights(origin, destination)
            
            if flights:
                print("\nAvailable flights:")
                for i, flight in enumerate(flights, 1):
                    print(f"\n{i}. {flight}")
            else:
                print("\nNo flights found for this route.")
                
        elif choice == "2":
            flight_number = input("Enter flight number (e.g., AA1234): ").upper()
            if flight_number in booking_system.flights:
                flight = booking_system.flights[flight_number]
                print("\nSelect seat class:")
                print("1. First Class")
                print("2. Business Class")
                print("3. Economy Class")
                
                class_choice = input("Enter your choice (1-3): ")
                seat_class = {
                    "1": "first",
                    "2": "business",
                    "3": "economy"
                }.get(class_choice)
                
                if seat_class:
                    available_seats = flight.get_available_seats(seat_class)
                    print(f"\nAvailable {seat_class} class seats:")
                    for seat in available_seats:
                        print(seat)
                else:
                    print("Invalid seat class selection.")
            else:
                print("Flight not found.")
                
        elif choice == "3":
            flight_number = input("Enter flight number (e.g., AA1234): ").upper()
            if flight_number in booking_system.flights:
                seat_number = input("Enter seat number (e.g., 15A): ").upper()
                passenger_name = input("Enter passenger name: ").title()
                
                try:
                    booking_system.book_flight(flight_number, seat_number, passenger_name)
                except ValueError as e:
                    print(f"\nError: {e}")
            else:
                print("Flight not found.")
                
        elif choice == "4":
            print("\nThank you for using our booking system!")
            break
            
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()