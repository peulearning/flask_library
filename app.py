from flask import Flask, render_template, flash, redirect, url_for, request
from flask_mysqldb import MySQL
from wtforms import Form, validators, StringField, FloatField, IntegerField, DateField, SelectField
from datetime import datetime

app = Flask(__name__)

# MySQL config
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1020'
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_DB'] = 'librarydb'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# Initialize MySQL
mysql = MySQL(app)

# HomePage
@app.route("/")
def index():
    return render_template("index.html")

# Members
@app.route('/members')
def members():
    # Create MySQLCursor
    cur = mysql.connection.cursor()

    # Execute SQL Query
    cur.execute("SELECT * FROM members")
    members = cur.fetchall()

    # Render Template
    return render_template('members.html', members=members)

    # Close DB Connection
    cur.close()

# View Details of Member by ID
@app.route('/member/<string:id>')
def view_member(id):
    # Create MySQLCursor
    cur = mysql.connection.cursor()

    # Execute SQL Query
    cur.execute("SELECT * FROM members WHERE id=%s", [id])
    member = cur.fetchone()

    # Render Template
    if member:
        return render_template('view_member_details.html', member=member)
    else:
        msg = 'This Member Does Not Exist'
        return render_template('view_member_details.html', warning=msg)

    # Close DB Connection
    cur.close()

# Define Add-Member-Form
class AddMember(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    email = StringField('Email', [validators.length(min=6, max=50)])

# Add Member
@app.route('/add_member', methods=['GET', 'POST'])
def add_member():
    # Get form data from request
    form = AddMember(request.form)

    # To handle POST request to route

    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        outstanding_debt = 0  # Set outstanding_debt to 0
        amount_spent = 0  # Set amount_spent to 0

        # Create MySQLCursor
        cur = mysql.connection.cursor()

        # Execute SQL Query
        cur.execute("INSERT INTO members (name, email, outstanding_debt, amount_spent) VALUES (%s, %s, %s, %s)", (name, email, outstanding_debt, amount_spent))

        # Commit to DB
        mysql.connection.commit()

        # Close DB Connection
        cur.close()

        # Flash Success Message
        flash("New Member Added", "success")

        # Redirect to show all members
        return redirect(url_for('members'))

    # To handle GET request to route
    return render_template('add_member.html', form=form)

# Edit Member by ID
@app.route('/edit_member/<string:id>', methods=['GET', 'POST'])
def edit_member(id):
    # Get form data from request
    form = AddMember(request.form)

    # Create MySQLCursor
    cur = mysql.connection.cursor()

    # To get existing field values of selected member
    cur.execute("SELECT name,email FROM members WHERE id=%s", [id])
    member = cur.fetchone()

    # To handle POST request to route
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data

        # Execute SQL Query
        cur.execute(
            "UPDATE members SET name=%s, email=%s WHERE id=%s", (name, email, id))

        # Commit to DB
        mysql.connection.commit()

        # Close DB Connection
        cur.close()

        # Flash Success Message
        flash("Member Updated", "success")

        # Redirect to show all members
        return redirect(url_for('members'))

    # To handle GET request to route
    return render_template('edit_member.html', form=form, member=member)

# Delete Member by ID
@app.route('/delete_member/<string:id>', methods=['POST'])
def delete_member(id):
    # Create MySQLCursor
    cur = mysql.connection.cursor()


    # Check for related records in the transactions table
    cur.execute("SELECT COUNT(*) FROM transactions WHERE member_id = %s", [id])

    result = cur.fetchone()

    if result is not None:
        count = result[0]
        print(f"Count of related records in transactions table: {count}")
        if count > 0:

            # There are related records in the transactions table, so delete them first

            cur.execute("DELETE FROM transactions WHERE member_id = %s", [id])

            print(f"Deleted {cur.rowcount} related records from transactions table")

    # Delete the member from the members table
    cur.execute("DELETE FROM members WHERE id = %s", [id])

    print(f"Deleted {cur.rowcount} rows from members table")
    # Commit to DB
    mysql.connection.commit()

    # Close DB Connection
    cur.close()

    # Flash Success Message
    flash("Member Deleted", "success")

    # Redirect to show all members
    return redirect(url_for('members'))

# Books
@app.route('/books')
def books():
    # Create MySQLCursor
    cur = mysql.connection.cursor()

    # Execute SQL Query
    cur.execute("SELECT id,title,author,total_quantity,available_quantity,rented_count FROM books")
    books = cur.fetchall()

    # Render Template
    return render_template('books.html', books=books)

    # Close DB Connection
    cur.close()

# View Details of Book by ID
@app.route('/book/<string:id>')
def view_book(id):
    # Create MySQLCursor
    cur = mysql.connection.cursor()

    # Execute SQL Query
    cur.execute("SELECT * FROM books WHERE id=%s", [id])
    book = cur.fetchone()

    # Render Template
    if book:
        return render_template('view_book_details.html', book=book)
    else:
        msg = 'This Book Does Not Exist'
        return render_template('view_book_details.html', warning=msg)

    # Close DB Connection
    cur.close()

# Define Add-Book-Form
class AddBook(Form):
    id = StringField('Book ID', [validators.Length(min=1, max=11)])
    title = StringField('Title', [validators.Length(min=2, max=255)])
    author = StringField('Author(s)', [validators.Length(min=2, max=255)])
    average_rating = FloatField(
        'Average Rating', [validators.NumberRange(min=0, max=5)])
    isbn = StringField('ISBN', [validators.Length(min=10, max=10)])
    isbn13 = StringField('ISBN13', [validators.Length(min=13, max=13)])
    language_code = StringField('Language', [validators.Length(min=1, max=3)])
    num_pages = IntegerField('No. of Pages', [validators.NumberRange(min=1)])
    ratings_count = IntegerField(
        'No. of Ratings', [validators.NumberRange(min=0)])
    text_reviews_count = IntegerField(
        'No. of Text Reviews', [validators.NumberRange(min=0)])
    publication_date = DateField(
        'Publication Date', [validators.InputRequired()])
    publisher = StringField('Publisher', [validators.Length(min=2, max=255)])
    total_quantity = IntegerField(
        'Total No. of Books', [validators.NumberRange(min=1)])

# Add Book
@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    # Get form data from request
    form = AddBook(request.form)

    # To handle POST request to route
    if request.method == 'POST' and form.validate():
        # Create MySQLCursor
        cur = mysql.connection.cursor()

        # Execute SQL Query
        cur.execute("INSERT INTO books (id,title,author,average_rating,isbn,isbn13,language_code,num_pages,ratings_count,text_reviews_count,publication_date,publisher,total_quantity,available_quantity, rented_count) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", [
            form.id.data,
            form.title.data,
            form.author.data,
            form.average_rating.data,
            form.isbn.data,
            form.isbn13.data,
            form.language_code.data,
            form.num_pages.data,
            form.ratings_count.data,
            form.text_reviews_count.data,
            form.publication_date.data,
            form.publisher.data,
            form.total_quantity.data,
            form.total_quantity.data,
            0
        ]) # Padrão rented_count definido como 0

        # Commit to DB
        mysql.connection.commit()

        # Close DB Connection
        cur.close()

        # Flash Success Message
        flash("New Book Added", "success")

        # Redirect to show all books
        return redirect(url_for('books'))

    # To handle GET request to route
    return render_template('add_book.html', form=form)

# Edit Book by ID
@app.route('/edit_book/<string:id>', methods=['GET', 'POST'])
def edit_book(id):
    # Get form data from request
    form = AddBook(request.form)

    # Create MySQLCursor
    cur = mysql.connection.cursor()

    # To get existing values of selected book
    cur.execute("SELECT * FROM books WHERE id=%s", [id])
    book = cur.fetchone()

    # To handle POST request to route
    if request.method == 'POST' and form.validate():
        # Calculate new available_quantity (No. of books available to be rented)
        available_quantity = book['available_quantity'] + \
            (form.total_quantity.data - book['total_quantity'])

        # Execute SQL Query
        cur.execute("UPDATE books SET id=%s,title=%s,author=%s,average_rating=%s,isbn=%s,isbn13=%s,language_code=%s,num_pages=%s,ratings_count=%s,text_reviews_count=%s,publication_date=%s,publisher=%s,total_quantity=%s,available_quantity=%s WHERE id=%s", [
            form.id.data,
            form.title.data,
            form.author.data,
            form.average_rating.data,
            form.isbn.data,
            form.isbn13.data,
            form.language_code.data,
            form.num_pages.data,
            form.ratings_count.data,
            form.text_reviews_count.data,
            form.publication_date.data,
            form.publisher.data,
            form.total_quantity.data,
            available_quantity,
            id])

        # Commit to DB
        mysql.connection.commit()

        # Close DB Connection
        cur.close()

        # Flash Success Message
        flash("Book Updated", "success")

        # Redirect to show all books
        return redirect(url_for('books'))

    # To handle GET request to route
    # To render edit book form
    return render_template('edit_book.html', form=form, book=book)

# Delete Book by ID
@app.route('/delete_book/<string:id>', methods=['POST'])
def delete_book(id):
    # Create MySQLCursor
    cur = mysql.connection.cursor()

    # Execute SQL Query
    cur.execute("DELETE FROM books WHERE id=%s", [id])

    # Commit to DB
    mysql.connection.commit()

    # Close DB Connection
    cur.close()

    # Flash Success Message
    flash("Book Deleted", "success")

    # Redirect to show all books
    return redirect(url_for('books'))

# Transactions
@app.route('/transactions')
def transactions():
    # Create MySQLCursor
    cur = mysql.connection.cursor()

    # Execute SQL Query
    cur.execute("SELECT * FROM transactions")
    transactions = cur.fetchall()

    # To handle empty fields
    for transaction in transactions:
        for key, value in transaction.items():
            if value is None:
                transaction[key] = "-"

    # Render Template
    return render_template('transactions.html', transactions=transactions)

    # Close DB Connection
    cur.close()

# Define Issue-Book-Form
class IssueBook(Form):
    book_id = SelectField('Book ID', choices=[])
    member_id = SelectField('Member ID', choices=[])
    per_day_fee = FloatField('Per Day Renting Fee', [
                             validators.NumberRange(min=1)])

# Issue Book
@app.route('/issue_book', methods=['GET', 'POST'])
def issue_book():
    # Get form data from request
    form = IssueBook(request.form)

    # Create MySQLCursor
    cur = mysql.connection.cursor()

    # Create choices list for SelectField in form
    cur.execute("SELECT id, title FROM books")
    books = cur.fetchall()
    book_ids_list = [(book['id'], book['title']) for book in books]

    cur.execute("SELECT id, name FROM members")
    members = cur.fetchall()
    member_ids_list = [(member['id'], member['name']) for member in members]

    form.book_id.choices = book_ids_list
    form.member_id.choices = member_ids_list

    # To handle POST request to route
    if request.method == 'POST' and form.validate():
        # Get the no of books available to be rented
        cur.execute("SELECT available_quantity FROM books WHERE id=%s", [
                    form.book_id.data])
        available_quantity = cur.fetchone()['available_quantity']

        # Check if book is available to be rented/issued
        if available_quantity < 1:
            error = 'No copies of this book are available to be rented'
            return render_template('issue_book.html', form=form, error=error)

        # Execute SQL Query to create transaction
        cur.execute("INSERT INTO transactions (book_id,member_id,per_day_fee) VALUES (%s, %s, %s)", [
            form.book_id.data,
            form.member_id.data,
            form.per_day_fee.data,
        ])

        # Update available quantity, rented count of book
        cur.execute(
            "UPDATE books SET available_quantity=available_quantity-1, rented_count=rented_count+1 WHERE id=%s", [form.book_id.data])

        # Commit to DB
        mysql.connection.commit()

        # Close DB Connection
        cur.close()

        # Flash Success Message
        flash("Book Issued", "success")

        # Redirect to show all transactions
        return redirect(url_for('transactions'))

    # To handle GET request to route
    return render_template('issue_book.html', form=form)

# Define Issue-Book-Form
class ReturnBook(Form):
    amount_paid = FloatField('Amount Paid', [validators.NumberRange(min=0)])

# Return Book by Transaction ID
@app.route('/return_book/<string:transaction_id>', methods=['GET', 'POST'])
def return_book(transaction_id):
    # Get form data from request
    form = ReturnBook(request.form)

    # Create MySQLCursor
    cur = mysql.connection.cursor()

    # To get existing values of selected transaction
    cur.execute("SELECT * FROM transactions WHERE id=%s", [transaction_id])
    transaction = cur.fetchone()

    # Calculate Total Charge
    date = datetime.now()
    difference = date - transaction['borrowed_on']
    difference = difference.days
    total_charge = difference * transaction['per_day_fee']

    # To handle POST request to route
    if request.method == 'POST' and form.validate():
        # Calculate debt for this transaction based on amount_paid
        transaction_debt = total_charge - form.amount_paid.data

        # Check if outstanding_debt + transaction_debt exceeds Rs.500
        cur.execute("SELECT outstanding_debt,amount_spent FROM members WHERE id=%s", [
                    transaction['member_id']])
        result = cur.fetchone()
        outstanding_debt = result['outstanding_debt']
        amount_spent = result['amount_spent']
        if outstanding_debt + transaction_debt > 500:
            error = 'Outstanding Debt Cannot Exceed Rs.500'
            return render_template('return_book.html', form=form, error=error)

        # Update returned_on, total_charge, amount_paid for this transaction
        cur.execute("UPDATE transactions SET returned_on=%s,total_charge=%s,amount_paid=%s WHERE id=%s", [
            date,
            total_charge,
            form.amount_paid.data,
            transaction_id
        ])

        # Update outstanding_debt and amount_spent for this member
        cur.execute("UPDATE members SET outstanding_debt=%s, amount_spent=%s WHERE id=%s", [
            outstanding_debt+transaction_debt,
            amount_spent+form.amount_paid.data,
            transaction['member_id']
        ])

        # Update available_quantity for this book
        cur.execute(
            "UPDATE books SET available_quantity=available_quantity+1 WHERE id=%s", [transaction['book_id']])

        # Commit to DB
        mysql.connection.commit()

        # Close DB Connection
        cur.close()

        # Flash Success Message
        flash("Book Returned", "success")

        # Redirect to show all transactions
        return redirect(url_for('transactions'))

    # To handle GET request to route
    return render_template('return_book.html', form=form, total_charge=total_charge, difference=difference, transaction=transaction)

# Reports
@app.route('/reports')
def reports():
    # Create MySQLCursor
    cur = mysql.connection.cursor()

    # Execute SQL Query to get 5 highest paying customers
    cur.execute("SELECT id,name,amount_spent FROM members ORDER BY amount_spent DESC LIMIT 5")
    members = cur.fetchall()

    # Execute SQL Query to get 5 most popular books
    cur.execute("SELECT id,title,author,total_quantity,available_quantity,rented_count FROM books ORDER BY rented_count DESC LIMIT 5")
    books = cur.fetchall()

    # Render Template
    return render_template('reports.html', members=members, books=books)

    # Close DB Connection
    cur.close()

# Define Search-Form
class SearchBook(Form):
    title = StringField('Title', [validators.Length(min=2, max=255)])
    author = StringField('Author(s)', [validators.Length(min=2, max=255)])

# Search
@app.route('/search_book', methods=['GET', 'POST'])
def search_book():
    # Get form data from request
    form = SearchBook(request.form)

    # To handle POST request to route
    if request.method == 'POST' and form.validate():
        # Create MySQLCursor
        cur = mysql.connection.cursor()
        title = '%' + form.title.data + '%'
        author = '%' + form.author.data + '%'
        # Check if book with same ID already exists
        cur.execute("SELECT * FROM books WHERE title LIKE %s AND author LIKE %s", [title, author])
        books = cur.fetchall()

        # Close DB Connection
        cur.close()

        # Render Template
        return render_template('search_book.html', form=form, books=books)

    # To handle GET request to route
    return render_template('search_book.html', form=form)

# Run Server
if __name__ == '__main__':
    app.secret_key = "secret"
    app.run(debug=True)

if __name__ == "__main__":
    app.run(debug=True)