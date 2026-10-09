import csv
import os


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

    def set_available(self, count):
        if count < 0 or count > self.__copies:
            raise ValueError("Available copies must be between 0 and owned copies")
        self.__available = count

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
            print(f'"{title}" is already here - copies raised to {book.get_copies()}')
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


FIELDS = ["library", "title", "author", "copies", "on_shelf"]


def save_libraries(libraries, path):
    with open(path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(FIELDS)
        for library in libraries.values():
            for book in library.books:
                writer.writerow(
                    [
                        library.name,
                        book.title,
                        book.author,
                        book.get_copies(),
                        book.get_available(),
                    ]
                )
    total = sum(len(library.books) for library in libraries.values())
    print(f"Saved {total} entries to {path}")


def load_libraries(path):
    libraries = {}
    if not os.path.exists(path):
        print(f"No file at {path} - starting empty")
        return libraries
    with open(path, newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            library = libraries.get(row["library"])
            if library is None:
                library = Library(row["library"])
                libraries[library.name] = library
            book = Book(row["title"], row["author"], int(row["copies"]))
            book.set_available(int(row["on_shelf"]))
            library.books.append(book)
    print(f"Loaded {len(libraries)} libraries from {path}")
    return libraries


def pick_library(libraries):
    if not libraries:
        print("No libraries yet - add one first")
        return None
    names = list(libraries)
    for index, name in enumerate(names, start=1):
        print(f"{index}. {name}")
    choice = input("Pick a library number: ").strip()
    if not choice.isdigit() or not 1 <= int(choice) <= len(names):
        print("Invalid choice")
        return None
    return libraries[names[int(choice) - 1]]


def main():
    path = "libraries.csv"
    libraries = load_libraries(path)

    menu = (
        "\n1. Add library\n"
        "2. Add book\n"
        "3. View entries\n"
        "4. Borrow book\n"
        "5. Return book\n"
        "6. Save to CSV\n"
        "7. Reload from CSV\n"
        "0. Save and exit\n"
    )

    while True:
        print(menu)
        choice = input("Choose: ").strip()

        if choice == "1":
            name = input("Library name: ").strip()
            if not name:
                print("Name cannot be empty")
            elif name in libraries:
                print("That library already exists")
            else:
                libraries[name] = Library(name)
                print(f"Added library {name}")

        elif choice == "2":
            library = pick_library(libraries)
            if library is None:
                continue
            title = input("Title: ").strip()
            author = input("Author: ").strip()
            count = input("Copies: ").strip()
            if not (title and author and count.isdigit() and int(count) > 0):
                print("Title, author and a positive copy count are required")
                continue
            library.add_book(title, author, int(count))

        elif choice == "3":
            if not libraries:
                print("No libraries yet")
            for library in libraries.values():
                library.show_all()

        elif choice == "4":
            library = pick_library(libraries)
            if library is None:
                continue
            library.borrow_book(input("Title: ").strip())

        elif choice == "5":
            library = pick_library(libraries)
            if library is None:
                continue
            library.return_book(input("Title: ").strip())

        elif choice == "6":
            save_libraries(libraries, path)

        elif choice == "7":
            libraries = load_libraries(path)

        elif choice == "0":
            save_libraries(libraries, path)
            print("Bye")
            break

        else:
            print("Unknown option")


if __name__ == "__main__":
    main()
