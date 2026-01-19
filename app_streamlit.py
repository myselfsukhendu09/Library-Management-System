
import streamlit as st
import pandas as pd
import backend as db
import plotly.express as px

# Page config
st.set_page_config(page_title="BiblioTech | Library Manager", page_icon="📚", layout="wide")

# Init DB
db.init_db()

st.title("📚 BiblioTech Library Management")
st.markdown("---")

# Metrics
total_books, unique_titles = db.get_stats()
m1, m2 = st.columns(2)
m1.metric("Total Books in Stock", int(total_books))
m2.metric("Unique Titles", int(unique_titles))

st.markdown("---")

# Catalog
st.subheader("📖 Current Catalog")
catalog_df = db.get_catalog()
st.dataframe(catalog_df, use_container_width=True)

# Charts
st.subheader("📊 Collection Insights")
fig = px.bar(catalog_df, x='title', y='stock', color='author', title="Stock Level by Title")
st.plotly_chart(fig, use_container_width=True)

# Admin Operations
st.sidebar.header("Admin Actions")
action = st.sidebar.selectbox("Select Operation", ["Add New Book", "Search Catalog"])

if action == "Add New Book":
    st.sidebar.subheader("Register Book")
    with st.sidebar.form("add_book"):
        title = st.text_input("Book Title")
        author = st.text_input("Author")
        stock = st.number_input("Opening Stock", min_value=1, step=1)
        submit = st.form_submit_button("Add to Collection")
        
        if submit:
            import sqlite3
            conn = sqlite3.connect('library.db')
            c = conn.cursor()
            c.execute("INSERT INTO books (title, author, stock) VALUES (?, ?, ?)", (title, author, stock))
            conn.commit()
            conn.close()
            st.toast(f"Successfully added {title}!")
            st.rerun()

elif action == "Search Catalog":
    query = st.sidebar.text_input("Search Title or Author")
    if query:
        results = catalog_df[catalog_df['title'].str.contains(query, case=False) | 
                             catalog_df['author'].str.contains(query, case=False)]
        st.write("Search Results:")
        st.dataframe(results)
