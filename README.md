# 📚 Bookstore SOAP API

A simple SOAP server in Python using `Spyne`, showcasing core SOAP features including:

- WSDL auto-generation
- API key authentication
- Full CRUD for book records (in-memory)
- Server time endpoint
- Tested using `pytest` and `zeep`

---

## 🚀 Getting Started

### 🐍 1. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 📦 2. Install Dependencies

```bash
pip install spyne requests zeep pytest
```

---

## ▶️ Running the Server

```bash
python bookstore_service.py
```

The server will start at:

```
http://localhost:8000/
```

### 📄 WSDL Endpoint

```
http://localhost:8000/?wsdl
```

Use this in SoapUI or client scripts.

---

## 🧪 Running Tests

Ensure the server is running in another terminal before testing.

```bash
pytest test_bookstore.py -v
```

---

## 🧼 Endpoints Overview

| Method          | Description                  | Required Header       |
|----------------|------------------------------|------------------------|
| `add_book`     | Add a new book               | `API_KEY: supersecret` |
| `get_book`     | Get book details by ISBN     | `API_KEY: supersecret` |
| `list_books`   | List all stored books        | `API_KEY: supersecret` |
| `delete_book`  | Delete a book by ISBN        | `API_KEY: supersecret` |
| `get_server_time` | Get current server UTC time | `API_KEY: supersecret` |

---

## 📦 Example Client Script

```python
from zeep import Client
from zeep.transports import Transport
from requests import Session

session = Session()
session.headers.update({'API_KEY': 'supersecret'})
transport = Transport(session=session)
client = Client("http://localhost:8000/?wsdl", transport=transport)

isbn = client.service.add_book("Dune", "Frank Herbert", 1965)
print("Book ISBN:", isbn)
```

---

## 🧼 Security

This server uses a simple **API key via headers** for authentication.
For production, consider:

- HTTPS
- WS-Security standards
- Token-based or session-based authentication

---

## 🛠 Technologies Used

- [Spyne](https://spyne.io/) — Python SOAP framework
- [Zeep](https://docs.python-zeep.org/) — Python SOAP client
- [pytest](https://docs.pytest.org/) — testing framework
- [requests](https://docs.python-requests.org/) — HTTP sessions

## Resources
- https://github.com/pysimplesoap/pysimplesoap
- https://www.makeareadme.com/