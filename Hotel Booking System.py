from datetime import datetime, date
import re

def validate_date(date_str):
    """Validate date format and ensure it's not in the past"""
    try:
        booking_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        if booking_date < date.today():
            print("Error: Cannot book for past dates!")
            return False
        return True
    except ValueError:
        print("Error: Invalid date format! Please use YYYY-MM-DD format.")
        return False

def validate_number(num_str, min_val=1, max_val=10):
    """Validate if input is a valid number within range"""
    try:
        num = int(num_str)
        if min_val <= num <= max_val:
            return True
        else:
            print(f"Error: Number must be between {min_val} and {max_val}!")
            return False
    except ValueError:
        print("Error: Please enter a valid number!")
        return False

def validate_payment(card_number, cvv, expiry):
    """Basic payment validation"""
    if not re.match(r'^\d{16}$', card_number):
        print("Error: Card number must be 16 digits!")
        return False
    if not re.match(r'^\d{3}$', cvv):
        print("Error: CVV must be 3 digits!")
        return False
    if not re.match(r'^(0[1-9]|1[0-2])\/\d{2}$', expiry):
        print("Error: Expiry must be in MM/YY format!")
        return False
    return True

def get_room_types():
    """Return available room types with prices"""
    return {
        1: {"type": "Standard Room", "price": 100},
        2: {"type": "Deluxe Room", "price": 150},
        3: {"type": "Suite", "price": 250},
        4: {"type": "Presidential Suite", "price": 500}
    }

def get_addons():
    """Return available add-ons with prices"""
    return {
        1: {"name": "Breakfast", "price": 25},
        2: {"name": "Airport Transfer", "price": 50},
        3: {"name": "Spa Package", "price": 100},
        4: {"name": "City Tour", "price": 75},
        5: {"name": "Late Checkout", "price": 30}
    }

def display_room_types():
    """Display available room types"""
    room_types = get_room_types()
    print("\n--- Available Room Types ---")
    for key, value in room_types.items():
        print(f"{key}. {value['type']} - ${value['price']}/night")

def display_addons():
    """Display available add-ons"""
    addons = get_addons()
    print("\n--- Available Add-ons ---")
    for key, value in addons.items():
        print(f"{key}. {value['name']} - ${value['price']}")

def get_valid_input(prompt, validator, *args):
    """Generic function to get valid input with validation"""
    while True:
        user_input = input(prompt).strip()
        if validator(user_input, *args):
            return user_input

def get_yes_no_input(prompt):
    """Get yes/no input from user"""
    while True:
        choice = input(prompt).strip().lower()
        if choice in ['yes', 'y']:
            return True
        elif choice in ['no', 'n']:
            return False
        else:
            print("Please enter 'yes' or 'no'")

def get_room_selections(num_rooms):
    """Get room type selections for each room"""
    room_types = get_room_types()
    selected_rooms = []
    
    for i in range(num_rooms):
        display_room_types()
        room_choice = get_valid_input(f"\nSelect room type for Room {i+1} (1-4): ", validate_number, 1, 4)
        room_num = int(room_choice)
        selected_rooms.append(room_types[room_num])
        print(f"Room {i+1}: {room_types[room_num]['type']} selected!")
    
    return selected_rooms

def get_addon_selections():
    """Get add-on selections from user"""
    addons = get_addons()
    selected_addons = []
    
    while True:
        display_addons()
        print("6. Confirm add-on selection")
        
        addon_input = input("\nSelect add-on (1-6): ").strip()
        
        if addon_input == "6":
            break
        elif validate_number(addon_input, 1, 5):
            addon_num = int(addon_input)
            addon_item = addons[addon_num]
            selected_addons.append(addon_item)
            print(f"Added: {addon_item['name']} - ${addon_item['price']}")
    
    return selected_addons

def get_payment_details():
    """Get and validate payment details"""
    while True:
        print("\n--- PAYMENT DETAILS ---")
        card_number = input("Enter credit card number (16 digits): ").strip()
        cvv = input("Enter CVV (3 digits): ").strip()
        expiry = input("Enter expiry date (MM/YY): ").strip()
        
        if validate_payment(card_number, cvv, expiry):
            print("Payment details validated successfully!")
            return card_number

def display_receipt(booking_date, num_pax, num_rooms, selected_rooms, selected_addons, card_number):
    """Display booking receipt"""
    print("\n" + "="*50)
    print("               BOOKING RECEIPT")
    print("="*50)
    print(f"Booking Date: {booking_date}")
    print(f"Number of Guests: {num_pax}")
    print(f"Number of Rooms: {num_rooms}")
    
    print("\n--- ROOM DETAILS ---")
    room_total = sum(room['price'] for room in selected_rooms)
    for i, room in enumerate(selected_rooms, 1):
        print(f"Room {i}: {room['type']} - ${room['price']}/night")
    
    addon_total = 0
    if selected_addons:
        print("\n--- ADD-ON SERVICES ---")
        addon_total = sum(addon['price'] for addon in selected_addons)
        for addon in selected_addons:
            print(f"- {addon['name']} - ${addon['price']}")
    
    total_cost = room_total + addon_total
    
    print(f"\n--- COST BREAKDOWN ---")
    print(f"Room Total: ${room_total}")
    print(f"Add-on Total: ${addon_total}")
    print(f"GRAND TOTAL: ${total_cost}")
    print(f"\nPayment Method: Credit Card ending in {card_number[-4:]}")
    print("\nBooking confirmed! Thank you for choosing our hotel!")
    print("="*50)

# Main Program
print("="*50)
print("     WELCOME TO HOTEL BOOKING SYSTEM")
print("="*50)

while True:
    print("\n--- MAIN MENU ---")
    print("1. Book Room")
    print("2. Exit")
    choice = input("Please select an option (1 or 2): ").strip()
    if choice == "2":
        print("\nThank you for using our Hotel Booking System!")
        print("Goodbye!")
        break
    elif choice == "1":
        print("\n--- STARTING BOOKING PROCESS ---")
        # Get booking details
        booking_date = get_valid_input("\nEnter booking date (YYYY-MM-DD): ", validate_date)
        num_pax = int(get_valid_input("\nEnter number of guests (1-10): ", validate_number, 1, 10))
        num_rooms = int(get_valid_input(f"\nEnter number of rooms needed (1-{num_pax}): ", validate_number, 1, num_pax))
        
        # Get room selections
        selected_rooms = get_room_selections(num_rooms)
        
        # Get add-ons if requested
        selected_addons = []
        if get_yes_no_input("\nWould you like to add any services? (yes/no): "): selected_addons = get_addon_selections()
            
        # Get payment details
        card_number = get_payment_details()
        
        # Display receipt if requested
        if get_yes_no_input("\nWould you like to display the receipt? (yes/no): "):
            display_receipt(booking_date, num_pax, num_rooms, selected_rooms, selected_addons, card_number)
        else:
            print("\nBooking confirmed! Thank you for choosing our hotel!")
        input("Press Any key to end the program...")
        print("Thank you for using our Hotel Booking System!")
        break
    else:
        print("Invalid choice! Please select 1 or 2.")