const books = [
  "To Kill a Mockingbird by Harper Lee",
    "The tail of peter rabbit",
    "1984 by George Orwell",
    "The Great Gatsby by F. Scott Fitzgerald",
    "The Catcher in the Rye by J.D. Salinger",
    "Pride and Prejudice by Jane Austen",
    "Moby-Dick by Herman Melville",
    "War and Peace by Leo Tolstoy",
    "The Hobbit by J.R.R. Tolkien",
  ];
  
  document.getElementById("searchButton").addEventListener("click", () => {
    const searchInput = document.getElementById("searchInput").value.toLowerCase();
    const resultsDiv = document.getElementById("searchResults");
  
    resultsDiv.innerHTML = ""; 
  
    if (searchInput.trim() === "") {
      resultsDiv.innerHTML = "<p>Please enter a search term.</p>";
      return;
    }
  
    const filteredBooks = books.filter((book) =>
      book.toLowerCase().includes(searchInput)
    );
  
    if (filteredBooks.length > 0) {
      filteredBooks.forEach((book) => {
        const bookDiv = document.createElement("div");
        bookDiv.textContent = book;
        resultsDiv.appendChild(bookDiv);
      });
    } else {
      resultsDiv.innerHTML = "<p>No books found.</p>";
    }
  });
  