📚 Book Finder – Project Usage Description
Book Finder is a Flask-based web application that allows users to explore, search, and preview books using the Google Books API. The platform also supports user registration and login with data stored in a MySQL database, offering a personalized experience with session-based access control.

🔧 Key Functionalities
🔐 User Authentication

Sign Up (/sign_up): New users can register using their email and password. The system checks for existing accounts and confirms password matching.

Login (/login): Users can log in to access book search functionalities. Successful login updates login status in the MySQL database.

Logout (/logout): Logs the user out and resets their login status in the database.

🏠 Homepage

The root URL / displays a beautifully styled landing page (index.html) with a hero section and feature highlights.

If a user is already logged in, they are redirected to the search page.

🔍 Book Search

Trending Books (/search): Displays trending fiction books fetched from Google Books API.

Custom Search (/searched_book): Users can enter keywords to search for specific books. Results include title, author, description, publisher, categories, ISBN, preview links, and cover images.

📦 Database Integration

Uses MySQL (pymysql) for storing user credentials and tracking login status.

🛠️ How to Use
Start the Server

bash
Copy
Edit
python app.py
The app will run on http://localhost:5000.

Visit Homepage

Open http://localhost:5000 in your browser.

Explore the app's features or click "Login" or "Sign Up".

User Flow

Sign Up → Create a new account.

Login → Access book browsing features.

Search → Use the search bar to find specific titles or authors.

Preview → Click "Preview Book" to open the book's details on Google Books.

Logout → End your session securely.

🖼️ UI Highlights
Colorful, responsive interface with consistent styling (Comic Sans MS, gradients, shadows).

Visual layout of books with cover images and descriptions.

Navigation bar, search bar, and result panels optimized for clarity and usability.

📦 Technologies Used
Backend: Flask (Python), PyMySQL, Google Books API

Frontend: HTML, CSS (with embedded styles)

Database: MySQL

