from flask import Flask, request, render_template, redirect, url_for, session, flash
import pymysql
import requests

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# MySQL database connection configuration
connection = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    database='DataDarsak'
)

# Google Books API Key
API_KEY = "Google_API_Key"

@app.route('/')
def home():
    if 'user_id' in session:
        return redirect(url_for("search"))
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error_message = None
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
                user = cursor.fetchone()
        except Exception as e:
            flash("Error occurred while logging in!", "danger")
            print("Error:", e)
        else:
            if user:
                session['user_id'] = user[0]
                session['email'] = user[1]
                with connection.cursor() as cursor:
                    cursor.execute("UPDATE users SET login_status = %s WHERE user_id = %s", (1, user[0]))
                    connection.commit()
                return redirect(url_for("search"))
            else:
                error_message = "Invalid email or password."
    return render_template('login.html', error_message=error_message)

@app.route('/sign_up', methods=['GET', 'POST'])
def signup():
    error_message = None
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        if confirm_password != password:
            error_message = "Passwords do not match!"
        else:
            try:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
                    existing_user = cursor.fetchone()
                    if existing_user:
                        error_message = "Username already exists!"
                    else:
                        cursor.execute("INSERT INTO users (email, password, login_status) VALUES (%s, %s, %s)", 
                                       (email, password, 0))
                        connection.commit()
                        flash("Account created successfully! Please log in.", "success")
                        return redirect(url_for("login"))
            except Exception as e:
                flash("Error occurred while signing up!", "danger")
                print("Error:", e)

    return render_template("sign_up.html", error_message=error_message)

@app.route('/logout')
def logout():
    if 'user_id' in session:
        user_id = session['user_id']
        with connection.cursor() as cursor:
            cursor.execute("UPDATE users SET login_status = %s WHERE user_id = %s", (0, user_id))
            connection.commit()
        
        session.pop('user_id', None)
        session.pop('email', None)
        flash("✔️ Successfully logged out!", "success")
    
    return redirect(url_for('home'))

@app.route('/search', methods=['GET', 'POST'])
def search():
    # Fetch trending books if the request method is GET
    if request.method == 'GET':
        url = f'https://www.googleapis.com/books/v1/volumes?q=subject:fiction&orderBy=relevance&maxResults=16&key={API_KEY}'
        response = requests.get(url)
        data = response.json()

        trending_books = []
        if 'items' in data:
            for item in data['items']:
                book_info = item['volumeInfo']
                trending_books.append({
                    'title': book_info.get('title', 'N/A'),
                    'author': ', '.join(book_info.get('authors', ['Unknown'])),
                    'description': book_info.get('description', 'No description available'),
                    'publisher': book_info.get('publisher', 'N/A'),
                    'published_year': book_info.get('publishedDate', 'N/A'),
                    'page_count': book_info.get('pageCount', 'N/A'),
                    'categories': ', '.join(book_info.get('categories', ['Uncategorized'])),
                    'isbn': ', '.join([isbn.get('identifier', 'N/A') for isbn in book_info.get('industryIdentifiers', [])]),
                    'preview_link': book_info.get('previewLink', '#'),
                    'image': book_info.get('imageLinks', {}).get('thumbnail', '/static/default_book_cover.jpg')
                })

        return render_template('search.html', trending_books=trending_books)

    # Handle POST request for search functionality
    if request.method == 'POST':
        query = request.form.get('query')
        return redirect(url_for('searched_book', query=query))


@app.route('/searched_book', methods=['GET'])
def searched_book():
    query = request.args.get('query', '')
    if query:
        url = f'https://www.googleapis.com/books/v1/volumes?q={query}&key={API_KEY}'
        response = requests.get(url)
        data = response.json()

        books = []
        if 'items' in data:
            for item in data['items']:
                book_info = item['volumeInfo']
                books.append({
                    'title': book_info.get('title', 'N/A'),
                    'author': ', '.join(book_info.get('authors', ['Unknown'])),
                    'description': book_info.get('description', 'No description available'),
                    'publisher': book_info.get('publisher', 'N/A'),
                    'published_year': book_info.get('publishedDate', 'N/A'),
                    'page_count': book_info.get('pageCount', 'N/A'),
                    'categories': ', '.join(book_info.get('categories', ['Uncategorized'])),
                    'isbn': ', '.join([isbn.get('identifier', 'N/A') for isbn in book_info.get('industryIdentifiers', [])]),
                    'preview_link': book_info.get('previewLink', '#'),
                    'image': book_info.get('imageLinks', {}).get('thumbnail', '/static/default_book_cover.jpg')
                })
        return render_template('searched_book.html', books=books)
    return render_template('searched_book.html', books=[])

if __name__ == '__main__':
    app.run(host="localhost", port=5000, debug=True)
