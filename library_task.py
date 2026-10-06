class Book:
    def __init__(self, title, author, copies):
        if copies < 1:
            raise ValueError("A book must have at least one copy")
        self.title = title
        self.author = author
        self.__copies = copies
        self.__available = copies

    def get_copies(self):
        return self.__copies

    def get_available(self):
        return self.__available

    def add_copies(self, count):
        if count < 1:
            raise ValueError("Copy count must be at least one")
        self.__copies += count
        self.__available += count

    def borrow_copy(self):
        if self.__available == 0:
            return False
        self.__available -= 1
        return True

    def return_copy(self):
        if self.__available == self.__copies:
            return False
        self.__available += 1
        return True

    def __str__(self):
        return (
            f"{self.title} by {self.author} - "
            f"{self.__copies} owned, {self.__available} on shelf"
        )


class Library:
    def __init__(self, name):
        self.name = name
        self.books = []

    def find(self, title):
        for book in self.books:
            if book.title.lower() == title.lower():
                return book
        return None

    def add_book(self, title, author, copies):
        book = self.find(title)
        if book is not None:
            book.add_copies(copies)
            print(
                f'"{title}" is already here - copies raised to {book.get_copies()}'
            )
            return book
        book = Book(title, author, copies)
        self.books.append(book)
        print(f'Added {title} ({copies} copies)')
        return book

    def show_all(self):
        print(f"--- {self.name} ---")
        if not self.books:
            print("The library has no books yet")
            return
        for book in self.books:
            print(book)

    def borrow_book(self, title):
        book = self.find(title)
        if book is None:
            print(f'We do not have "{title}"')
            return False
        if not book.borrow_copy():
            print(f'All copies of "{title}" are out - none left on the shelf')
            return False
        print(f'Borrowed "{title}" - {book.get_available()} left on shelf')
        return True

    def return_book(self, title):
        book = self.find(title)
        if book is None:
            print(f'"{title}" does not belong to this library')
            return False
        if not book.return_copy():
            print(f'No copy of "{title}" is out on loan - nothing to return')
            return False
        print(f'Returned "{title}" - {book.get_available()} back on the shelf')
        return True


if __name__ == "__main__":
    library = Library("College Library")

    library.add_book("a", "H", 1)
    library.add_book("a", "H", 1)
    library.add_book("C", "R", 2)
    library.show_all()

    print()
    library.borrow_book("Ikigai")
    library.borrow_book("Ikigai")
    library.borrow_book("The Hobbit")

    print()
    library.return_book("Ikigai")
    library.return_book("Ikigai")
    library.return_book("Ikigai")

    print()
    library.show_all()
