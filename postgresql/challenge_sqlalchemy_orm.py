from sqlalchemy import create_engine, select, Column, String, Integer, ForeignKey
from sqlalchemy.orm import registry, relationship, Session
import os

engine = create_engine(
    f'postgresql+psycopg2://postgres:{os.environ["POSTGRESQLPASSWORD"]}@localhost/library'
)

mapper_registry = registry()
Base = mapper_registry.generate_base()


class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String)
    last_name = Column(String)

    def __repr__(self):
        return f"<Author(id={self.id}, first_name={self.first_name}, last_name={self.last_name})>"


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    num_pages = Column(Integer)

    def __repr__(self):
        return f"<Book(id={self.id}, title={self.title}, num_pages={self.num_pages})>"


class AuthorBook(Base):
    __tablename__ = "authorbooks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    author_id = Column(Integer, ForeignKey("authors.id"))
    book_id = Column(Integer, ForeignKey("books.id"))

    author = relationship("Author")
    book = relationship("Book")

    def __repr__(self):
        return f"<AuthorBook(id={self.id}, author_id={self.author_id}, book_id={self.book_id})>"


# Create tables in DB
Base.metadata.create_all(engine)


def add_book(title: str, num_pages: int, first_name: str, last_name: str):
    author = Author(first_name=first_name, last_name=last_name)
    book = Book(title=title, num_pages=num_pages)

    with Session(engine) as session:
        # Check for existing book in DB
        existing_book = session.execute(
            select(Book).filter(Book.title == title, Book.num_pages == num_pages)
        ).scalar()
        if existing_book:
            print("Book already exists!")
            return
        else:
            session.add(book)

        # Check for existing author in DB
        existing_author = session.execute(
            select(Author).filter(
                Author.first_name == first_name, Author.last_name == last_name
            )
        ).scalar()
        if existing_author:
            session.flush()
            pairing = AuthorBook(author_id=existing_author.id, book_id=book.id)
        else:
            print("Adding new author...")
            session.add(author)
            session.flush()
            pairing = AuthorBook(author_id=author.id, book_id=book.id)

        # Add entry in AuthorBook table
        session.add(pairing)
        session.commit()
        print("New pairing added!", str(pairing))


if __name__ == "__main__":
    print("Creating a new book...\n")
    title = input("What is the title of the book?\n")
    num_pages = int(input("How many pages are in the book?\n"))
    first_name = input("What is the first name of the author?\n")
    last_name = input("What is the last name of the author?\n")
    print("Creating book...\n")

    add_book(title, num_pages, first_name, last_name)

    print("Done!")
