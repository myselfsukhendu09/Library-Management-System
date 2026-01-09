from flask import Flask, render_template, request, redirect, url_for, flash
from backend import LibraryBackend

app = Flask(__name__)
app.secret_key = "library_secret"
lib = LibraryBackend()

@app.route('/')
def index():
    books = lib.get_books()
    return render_template('index.html', books=books)

@app.route('/add_book', methods=['POST'])
def add_book():
    title = request.form.get('title')
    author = request.form.get('author')
    isbn = request.form.get('isbn')
    category = request.form.get('category')
    quantity = int(request.form.get('quantity', 1))
    
    success, message = lib.add_book(title, author, isbn, category, quantity)
    flash(message, "success" if success else "danger")
    return redirect(url_for('index'))

@app.route('/members')
def members():
    members_list = lib.get_members()
    return render_template('members.html', members=members_list)

@app.route('/add_member', methods=['POST'])
def add_member():
    name = request.form.get('name')
    email = request.form.get('email')
    success, message = lib.add_member(name, email)
    flash(message, "success" if success else "danger")
    return redirect(url_for('members'))

@app.route('/transactions')
def transactions():
    trans = lib.get_transactions()
    books = lib.get_books()
    members_list = lib.get_members()
    return render_template('transactions.html', transactions=trans, books=books, members=members_list)

@app.route('/issue', methods=['POST'])
def issue():
    book_id = request.form.get('book_id')
    member_id = request.form.get('member_id')
    success, message = lib.issue_book(book_id, member_id)
    flash(message, "success" if success else "danger")
    return redirect(url_for('transactions'))

@app.route('/return/<int:tid>')
def return_book(tid):
    success, message = lib.return_book(tid)
    flash(message, "success" if success else "danger")
    return redirect(url_for('transactions'))

if __name__ == '__main__':
    app.run(debug=True, port=5001)
