import pytest
from zeep import Client
from zeep.transports import Transport
from requests import Session

# --- Constants ---
WSDL_URL = "http://localhost:8000/?wsdl"
API_KEY = "supersecret"

@pytest.fixture(scope="module")
def soap_client():
    session = Session()
    session.headers.update({'API_KEY': API_KEY})
    transport = Transport(session=session)
    client = Client(WSDL_URL, transport=transport)
    return client

@pytest.fixture
def book_data():
    return {
        "title": "The Hobbit",
        "author": "J.R.R. Tolkien",
        "year": 1937
    }

def test_add_book(soap_client, book_data):
    isbn = soap_client.service.add_book(
        book_data["title"],
        book_data["author"],
        book_data["year"]
    )
    assert isbn is not None
    assert isinstance(isbn, str)

def test_get_book(soap_client, book_data):
    isbn = soap_client.service.add_book(
        book_data["title"],
        book_data["author"],
        book_data["year"]
    )
    result = soap_client.service.get_book(isbn)
    assert book_data["title"] in result
    assert book_data["author"] in result

def test_list_books(soap_client, book_data):
    # Add book
    soap_client.service.add_book(
        book_data["title"],
        book_data["author"],
        book_data["year"]
    )
    # List
    books = soap_client.service.list_books()
    assert isinstance(books, list)
    assert any(book_data["title"] in book for book in books)

def test_delete_book(soap_client):
    isbn = soap_client.service.add_book("TempBook", "Test Author", 2025)
    result = soap_client.service.delete_book(isbn)
    assert result == "Book deleted"
    # Try again (should not exist)
    result2 = soap_client.service.delete_book(isbn)
    assert result2 == "Book not found"

def test_get_server_time(soap_client):
    time = soap_client.service.get_server_time()
    assert "UTC" in time
