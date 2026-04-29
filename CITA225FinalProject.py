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
        #Check if this ISBN is already in use
        if isbn in self.inventory:
            decision = input("This ISBN is already linked to a book. Do you want to OVERWRITE?: Y/N ")
            decision = decision.upper()

            #Decide to override or not
            if decision == "Y":
                self.inventory[isbn] = Book(isbn, title, author, price, quantity)

            else:
                print("Exiting Adding Book Segment Now")
                
        #Add book if isbn is free      
        else:
            self.inventory[isbn] = Book(isbn, title, author, price, quantity)

        #Adding Authors not in the database yet
        if author not in self.authors:
            self.authors.add(author)
            print("Unique author added along with book.")
            
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
    
    def restock_inventory(self, isbn, quantity):
        self.shipment.push(quantity)
        restocked = self.shipment.pop()
        self.inventory[isbn].quantity += restocked
        print(f"Restocked {restocked} copies of {self.inventory[isbn].title}")
        if isbn in self.waitlist:
            while not self.waitlist[isbn].isEmpty():
                customer_name, order_qty = self.waitlist[isbn].dequeue()
                if self.inventory[isbn].quantity >= order_qty:
                    self.inventory[isbn].quantity -= order_qty
                    total_price = self.inventory[isbn].price * order_qty
                    self.sales.append((customer_name, isbn, order_qty, total_price))
                    print(f"{customer_name}'s order has been fulfilled!")
                else:
                    self.waitlist[isbn].enqueue((customer_name, order_qty))
                    break
    #Now can remove an author if they don't have a book
    def remove_author(self):
        #Choose name
        author = input("Enter the name of the Author you want to remove: ")
        #Check if in store
        if author in self.authors:
            self.authors.discard(author)
            print("Author removed")
        #Express not in system
        else:
            print("Author not in system")

    def display_sales(self):
        if len(self.sales) == 0:
            print("No sales yet!")
        else:
            for sale in self.sales:
                customer_name, isbn, quantity, total_price = sale
                print(f"Customer: {customer_name} | ISBN: {isbn} | Quantity: {quantity} | Total: ${total_price:.2f}")

def main():
    store = Bookstore()
    while True:
        print("\n--- Bookstore Menu ---")
        print("1. Add a book")
        print("2. View inventory")
        print("3. Restock Inventory")
        print("4. Place an order")
        print("5. View total sales")
        print("6. Check unique Authors")
        print("7. Display waitlist")
        print("8. Exit")
        
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
            isbn = input("Enter ISBN: ")
            quantity = int(input("Enter quantity to restock: "))
            store.restock_inventory(isbn, quantity)
        elif choice == "4":
            customer_name = input("Enter customer name: ")
            isbn = input("Enter ISBN: ")
            quantity = int(input("Enter quantity: "))
            store.place_order(customer_name, isbn, quantity)
        elif choice == "5":
            store.display_sales()
        elif choice == "6":
            if len(store.authors) == 0:
                print("We have no authors")
            else:
                print(*store.authors)
        elif choice == "7":
            store.display_waitlist()
        elif choice == "8":
            print("Goodbye!")
            break
        elif choice == "9":
            store.remove_author()
        else:
            print("Invalid choice, try again!")
            
main()
