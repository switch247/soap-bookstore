from zeep import Client
from zeep.transports import Transport
from requests import Session

# --- Setup with API Key Header ---
session = Session()
session.headers.update({'API_KEY': 'supersecret'})
transport = Transport(session=session)

# --- Connect to WSDL ---
client = Client("http://localhost:8000/?wsdl", transport=transport)

# --- Test Calls ---
print("✅ Adding a book...")
isbn = client.service.add_book("Dune", "Frank Herbert", 1965)
print("ISBN:", isbn)

print("\n📖 Getting the book...")
print(client.service.get_book(isbn))

print("\n📚 Listing all books...")
books = client.service.list_books()
for book in books:
    print("-", book)

print("\n❌ Deleting the book...")
print(client.service.delete_book(isbn))

print("\n⏰ Server Time:")
print(client.service.get_server_time())
