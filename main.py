from fastapi import FastAPI, status
from app.api.v1.classes.users.routers import user_router
from app.api.v1.auth.authentication import login_router
from app.api.v1.classes.books.routers import book_router
from app.api.v1.classes.records.routers import record_router
from app.api.v1.classes.books_returned.routers import bookreturned_router

app = FastAPI()


app.include_router(user_router, prefix='/api/v1/users', tags=['Users'])
app.include_router(login_router, prefix='/api/v1', tags=['Login'])
app.include_router(book_router, prefix='/api/v1/books', tags=['Books'])
app.include_router(record_router,prefix='/api/v1/records', tags=['Records'])
app.include_router(bookreturned_router,prefix='/api/v1/books_returned', tags=['BooksReturned'])

@app.get('/', status_code=status.HTTP_200_OK)
def home():
    return 'OK'

