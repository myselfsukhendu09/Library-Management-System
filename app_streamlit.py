import streamlit as st
import pandas as pd
from backend import LibraryBackend
from datetime import datetime

# Page config
st.set_page_config(page_title="BiblioTech Dash", page_icon="📚", layout="wide")

# Custom CSS
st.markdown("""
<style>
    .main { background-color: #f0f2f6; }
    .stMetric { background-color: white; padding: 15px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }
</style>
""", unsafe_allow_html=True)

lib = LibraryBackend()

st.title("📚 BiblioTech Dashboard")
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Catalog", "Members", "Circulation", "Insights"])

if page == "Catalog":
    st.header("📖 Library Catalog")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Add New Book")
        title = st.text_input("Title")
        author = st.text_input("Author")
        isbn = st.text_input("ISBN")
        cat = st.selectbox("Category", ["Fiction", "Non-Fiction", "Self-Help", "Tech", "Science"])
        qty = st.number_input("Total Quantity", min_value=1, value=1)
        if st.button("Add to Catalog"):
            success, msg = lib.add_book(title, author, isbn, cat, qty)
            if success: st.success(msg)
            else: st.error(msg)
            
    with col2:
        st.subheader("Book Inventory")
        query = st.text_input("Search by title or author")
        if query:
            books = lib.search_books(query)
        else:
            books = lib.get_books()
        
        if books:
            df = pd.DataFrame(books, columns=["ID", "Title", "Author", "ISBN", "Category", "Total", "Available"])
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No books found.")

elif page == "Members":
    st.header("👥 Member Management")
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Register Member")
        name = st.text_input("Full Name")
        email = st.text_input("Email Address")
        if st.button("Register"):
            success, msg = lib.add_member(name, email)
            if success: st.success(msg)
            else: st.error(msg)
            
    with col2:
        st.subheader("Active Members")
        members = lib.get_members()
        if members:
            df = pd.DataFrame(members, columns=["ID", "Name", "Email", "Joined Date"])
            st.dataframe(df, use_container_width=True)

elif page == "Circulation":
    st.header("🔄 Circulation & Borrowing")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Issue Book")
        books = lib.get_books()
        members = lib.get_members()
        
        book_opt = {f"{b[1]} (ISBN: {b[3]})": b[0] for b in books if b[6] > 0}
        member_opt = {f"{m[1]} ({m[2]})": m[0] for m in members}
        
        sel_book = st.selectbox("Select Book", list(book_opt.keys()))
        sel_member = st.selectbox("Select Member", list(member_opt.keys()))
        
        if st.button("Confirm Issue"):
            success, msg = lib.issue_book(book_opt[sel_book], member_opt[sel_member])
            if success: st.success(msg)
            else: st.error(msg)
            
    with col2:
        st.subheader("Transaction History")
        trans = lib.get_transactions()
        if trans:
            df = pd.DataFrame(trans, columns=["ID", "Book", "Member", "Issued", "Returned", "Status"])
            st.dataframe(df, use_container_width=True)
            
            st.divider()
            st.subheader("Process Return")
            issued_trans = {f"{t[1]} borrowed by {t[2]} (ID: {t[0]})": t[0] for t in trans if t[5] == 'Issued'}
            if issued_trans:
                tid = st.selectbox("Select Transaction", list(issued_trans.keys()))
                if st.button("Confirm Return"):
                    success, msg = lib.return_book(issued_trans[tid])
                    if success: st.success(msg)
                    else: st.error(msg)
            else:
                st.info("No active borrowings.")

elif page == "Insights":
    st.header("📊 Library Insights")
    books = lib.get_books()
    members = lib.get_members()
    trans = lib.get_transactions()
    
    m1, m2, m3 = st.columns(3)
    m1.metric("Total Books", sum(b[5] for b in books))
    m2.metric("Active Members", len(members))
    m3.metric("Checked Out", len([t for t in trans if t[5] == 'Issued']))
    
    st.divider()
    if books:
        st.subheader("Availability Distribution")
        df_books = pd.DataFrame(books, columns=["ID", "Title", "Author", "ISBN", "Category", "Total", "Available"])
        st.bar_chart(df_books.set_index("Title")["Available"])
