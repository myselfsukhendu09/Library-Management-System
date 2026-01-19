# 📚 BiblioTech | Advanced Library Management System

A professional, dual-interface library management system featuring a Flask web application and a Streamlit analytics dashboard.

## ✨ Key Features
- **Book Management**: Full CRUD operations for library catalog.
- **Member Registration**: Track library users and joining dates.
- **Automated Circulation**: Real-time tracking of book issuing and returns with stock updates.
- **Dual Interface**:
  - **Flask App**: Professional web UI for daily operations.
  - **Streamlit Dash**: Interactive analytics and inventory management.
- **SQLite Persistence**: Robust local database storage.

## 🛠️ Tech Stack
- **Backend**: Python 3, SQLite
- **Web App**: Flask, Bootstrap 5, Jinja2
- **Analytics**: Streamlit, Pandas

## 🚀 How to Run

### 1. Install Dependencies
```bash
pip install flask streamlit pandas
```

### 2. Launch Application
To start the library management portal:
```bash
streamlit run app_streamlit.py
```
*Note: This portal handles both catalog browsing and collection management.*

## 📁 Repository Structure
- `app_flask.py`: Flask application server.
- `app_streamlit.py`: Streamlit dashboard application.
- `backend.py`: Core logic and database operations.
- `templates/`: Flask HTML templates.
- `library.db`: SQLite database (auto-generated).
