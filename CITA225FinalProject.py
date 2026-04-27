from LinkedList import LinkedList
from Queue import Queue
from Stack import Stack

class Book():
    def __init__ (self, isbn, title, author, price, quantity):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.price = price
        self.quantity = quantity

class Bookstore():
    def __init__(self):
        self.inventory = {}
        self.sales = []
        self.authors = set()
        self.waitlist = {}
        self.shipment = Stack()

    def add_book(self, isbn, title, author, price, quantity):
        self.inventory[isbn] = Book(isbn, title, author, price, quantity)
        self.authors.add(author)
        print("Book added successfully!")
    
    def place_order(self, customer_name, isbn, quantity):
        if isbn in self.inventory:
            if self.inventory[isbn].quantity >= quantity:
                self.inventory[isbn].quantity -= quantity
                total_price = self.inventory[isbn].price * quantity
                self.sales.append((customer_name, isbn, quantity, total_price))
                print("Order placed successfully!")
            else:
                if isbn not in self.waitlist:
                    self.waitlist[isbn] = Queue()
                self.waitlist[isbn].enqueue((customer_name, quantity))
                print("Added to waitlist!")
        else:
            print("Book not found!")

    def display_inventory(self):
        for isbn, book in self.inventory.items():
            print(f"ISBN: {isbn} | Title: {book.title} | Author: {book.author} | Price: {book.price} | Quantity: {book.quantity}")

def main():
    store = Bookstore()
    while True:
        print("\n--- Bookstore Menu ---")
        print("1. Add a book")
        print("2. View inventory")
        print("3. Place an order")
        print("4. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == "1":
            isbn = input("Enter ISBN: ")
            title = input("Enter title: ")
            author = input("Enter author: ")
            price = float(input("Enter price: "))
            quantity = int(input("Enter quantity: "))
            store.add_book(isbn, title, author, price, quantity)
        elif choice == "2":
            store.display_inventory()
        elif choice == "3":
            customer_name = input("Enter customer name: ")
            isbn = input("Enter ISBN: ")
            quantity = int(input("Enter quantity: "))
            store.place_order(customer_name, isbn, quantity)
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice, try again!")

main()