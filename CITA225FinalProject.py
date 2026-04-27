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

def main():
    store = Bookstore()
    isbn = input("Enter ISBN: ")
    title = input("Enter title: ")
    author = input("Enter author: ")
    price = float(input("Enter price: "))
    quantity = int(input("Enter quantity: "))
    store.add_book(isbn, title, author, price, quantity)

main()