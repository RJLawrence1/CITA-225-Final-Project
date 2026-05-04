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
        #Dictionary to store ISBN as keey
        self.inventory = {}

        #List to track sales
        self.sales = []

        #Sets of unique authors
        self.authors = set()

        #Dictionary of queues  
        self.waitlist = {}

        #Stack of shipment bxes
        self.shipment = Stack()

        # Linked List of waitlist
        self.waitlist_log = LinkedList()

    def add_book(self, isbn, title, author, price, quantity):
        #Check if this ISBN is already in use
        if isbn in self.inventory:
            decision = input("This ISBN is already linked to a book. Do you want to OVERWRITE?: Y/N ")
            decision = decision.upper()

            #Decide to override or not
            if decision == "Y":
                old_author = self.inventory[isbn].author

                #Remove old author from unique authors
                self.authors.discard(old_author)
                self.inventory[isbn] = Book(isbn, title, author, price, quantity)

                #Add new author if logical
                if author not in self.authors:
                    self.authors.add(author)
                    print("Unique author added along with book")
                print("Book added successfully")
            else:
                print("Exiting Adding Book Segment Now")
                return

        #Add book if isbn is free      
        else:
            self.inventory[isbn] = Book(isbn, title, author, price, quantity)
            if author not in self.authors:
                self.authors.add(author)
                print("Unique author added along with book")
            print("Book added successfully")
    
    def place_order(self, customer_name, isbn, quantity):
        # Processes a customer order. If in stock, fulfills immediately.
        # If out of stock, adds customer to the waitlist queue.
        if isbn in self.inventory:
            if self.inventory[isbn].quantity >= quantity:
                self.inventory[isbn].quantity -= quantity
                total_price = self.inventory[isbn].price * quantity
                self.sales.append((customer_name, isbn, quantity, total_price))
                print("Order placed successfully")
            else:
                if isbn not in self.waitlist:
                    self.waitlist[isbn] = Queue()
                self.waitlist[isbn].enqueue((customer_name, quantity))
                self.waitlist_log.add(f"{customer_name} waiting for ISBN {isbn}")
                print("Added to waitlist")
        else:
            print("Book not found")

    def display_inventory(self):
        # Displays all books currently in the inventory dictionary.
        if len(self.inventory) == 0:
            print("No books in inventory yet"
        else:
            for isbn, book in self.inventory.items():
                print(f"ISBN: {isbn} | Title: {book.title} | Author: {book.author} | Price: {book.price} | Quantity: {book.quantity}")
    
    def restock_inventory(self, isbn, quantity):
        # Restocks a book using a stack to simulate shipment boxes.
        # Automatically fulfills waitlisted customers after restocking.
        if isbn not in self.inventory:
            print("Book not found")
            return
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
                    print(f"{customer_name}'s order has been fulfilled")
                else:
                    self.waitlist[isbn].enqueue((customer_name, order_qty))
                    break
            if self.waitlist[isbn].isEmpty():
                del self.waitlist[isbn]

    def remove_book(self):
        # Removes a book from inventory by ISBN.
        # Also removes the author from the set if they have no other books.
        isbn = input("Enter the ISBN of the book you want to remove: ")
        if isbn in self.inventory:
            old_author = self.inventory[isbn].author  # grab the author before deleting
            del self.inventory[isbn]  # remove the book
            # check if that author still has other books
            author_still_has_books = any(book.author == old_author for book in self.inventory.values())
            if not author_still_has_books:
                self.authors.discard(old_author)
                print(f"{old_author} removed from authors list too")
            print("Book removed")
        else:
            print("Book not found")

    def display_sales(self):
        # Displays all completed sales records including total price.
        if len(self.sales) == 0:
            print("No sales")
        else:
            for sale in self.sales:
                customer_name, isbn, quantity, total_price = sale
                print(f"Customer: {customer_name} | ISBN: {isbn} | Quantity: {quantity} | Total: ${total_price:.2f}")
    
    def display_waitlist(self):
        # Shows waitlisted customers for each book using a queue.
        if len(self.waitlist) == 0:
            print("No waitlists")
        else:
            for isbn, queue in self.waitlist.items():
                if queue.getSize() > 0:
                    print(f"\nISBN: {isbn} | Customers waiting: {queue.getSize()}")
                    for entry in self.waitlist_log:
                        if isbn in entry:
                            print(f"  - {entry}")

def main():
    store = Bookstore()
    while True:
        print("\n--- Bookstore Menu ---")
        print("1. Add a book")
        print("2. Remove a book")
        print("3. View inventory")
        print("4. Restock Inventory")
        print("5. Place an order")
        print("6. View total sales")
        print("7. Display waitlist")
        print("8. Check unique Authors")
        print("9. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == "1":
            isbn = input("Enter ISBN: ")
            title = input("Enter title: ")
            author = input("Enter author: ")
            price = float(input("Enter price: "))
            quantity = int(input("Enter quantity: "))
            store.add_book(isbn, title, author, price, quantity)
        elif choice == "2":
            store.remove_book()
        elif choice == "3":
            store.display_inventory()
        elif choice == "4":
            isbn = input("Enter ISBN: ")
            quantity = int(input("Enter quantity to restock: "))
            store.restock_inventory(isbn, quantity)
        elif choice == "5":
            customer_name = input("Enter customer name: ")
            isbn = input("Enter ISBN: ")
            quantity = int(input("Enter quantity: "))
            store.place_order(customer_name, isbn, quantity)
        elif choice == "6":
            store.display_sales()
        elif choice == "7":
            store.display_waitlist()
        elif choice == "8":
            if len(store.authors) == 0:
                print("We have no authors")
            else:
                print(*store.authors)
        elif choice == "9":
            print("Goodbye")
            break
        else:
            print("Invalid choice, try again")
            
main() 
