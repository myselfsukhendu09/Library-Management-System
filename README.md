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

### 2. Run Flask Web App
```bash
python app_flask.py
```
Visit `http://127.0.0.1:5001` in your browser.

### 3. Run Streamlit Dashboard
```bash
streamlit run app_streamlit.py
```

## 📁 Repository Structure
- `app_flask.py`: Flask application server.
- `app_streamlit.py`: Streamlit dashboard application.
- `backend.py`: Core logic and database operations.
- `templates/`: Flask HTML templates.
- `library.db`: SQLite database (auto-generated).
