from spyne import Application, rpc, ServiceBase, Unicode, Integer, Iterable, Fault
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from datetime import datetime
from wsgiref.simple_server import make_server


books = {}

# --- Middleware-like utility: simple API key validation ---
def validate_api_key(ctx):
    api_key = ctx.transport.req_env.get('HTTP_API_KEY')
    if api_key != 'supersecret':
        raise Fault(faultstring="Unauthorized")


def log_request(ctx, method):
    print(f"[{datetime.now()}] {method} called by {ctx.transport.req_env.get('REMOTE_ADDR')}")


class BookstoreService(ServiceBase):

    @rpc(Unicode, Unicode, Integer, _returns=Unicode)
    def add_book(ctx, title, author, year):
        """Add a book and return its generated ISBN."""
        validate_api_key(ctx)
        log_request(ctx, "add_book")

        isbn = f"{title[:3].upper()}{year}"
        books[isbn] = {"title": title, "author": author, "year": year}
        return isbn

    @rpc(Unicode, _returns=Unicode)
    def get_book(ctx, isbn):
        """Retrieve a book by ISBN."""
        validate_api_key(ctx)
        log_request(ctx, "get_book")

        book = books.get(isbn)
        if not book:
            return "Book not found"
        return f"{book['title']} by {book['author']} ({book['year']})"

    @rpc(_returns=Iterable(Unicode))
    def list_books(ctx):
        """List all books."""
        validate_api_key(ctx)
        log_request(ctx, "list_books")

        for isbn, book in books.items():
            yield f"{isbn}: {book['title']} by {book['author']}"

    @rpc(Unicode, _returns=Unicode)
    def delete_book(ctx, isbn):
        """Delete a book by ISBN."""
        validate_api_key(ctx)
        log_request(ctx, "delete_book")

        if isbn in books:
            del books[isbn]
            return "Book deleted"
        return "Book not found"

    @rpc(_returns=Unicode)
    def get_server_time(ctx):
        """Return the current server time (UTC)."""
        validate_api_key(ctx)
        log_request(ctx, "get_server_time")

        return datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")


application = Application(
    [BookstoreService],
    tns='spyne.bookstore',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11()
)


wsgi_app = WsgiApplication(application)

if __name__ == "__main__":
    print("SOAP server running at: http://localhost:8000/?wsdl")
    server = make_server("0.0.0.0", 8000, wsgi_app)
    server.serve_forever()
