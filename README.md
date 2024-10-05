# Security Course Project: SQL Injection and XSS Attacks Demonstration

## Description
This project was developed for the **Computer Security** course as part of a demonstration of web vulnerabilities. The project simulates a telecommunications company, **Communication_LTD**, and includes both a vulnerable version and a secure version to showcase how SQL Injection (SQLi) and Cross-Site Scripting (XSS) attacks can be mitigated in web applications. The frontend is built using React, the backend uses FastAPI (Python), and MySQL is used as the relational database.

## Features
- **User Registration**: New users can create accounts to access the site.
- **User Login**: Secure user login functionality.
- **Password Recovery**: Users can recover forgotten passwords through email verification.
- **Password Change**: Users can change their password securely.
- **Client Management**: Users can add, edit, and manage clients.
- **Logout Functionality**: Users can securely log out of their accounts.

## Technologies Used
- **Frontend**: React.js
- **Backend**: FastAPI (Python)
- **Database**: MySQL
- **Communication**: Axios for HTTP requests

## Installation
Follow these steps to set up and run the project locally.

### Prerequisites
- **Python 3.x**: Ensure Python is installed.
- **Node.js**: Required for running the React frontend.
- **MySQL**: Install and set up a MySQL server.
- **Git**: For cloning the repository.

### Clone the Repository
```bash
git clone https://github.com/shlomi123002/Computer-Security-Final-Project-Secure
cd Computer-Security-Final-Project-Secure
```

### Install Backend Dependencies
```bash
pip install -r requirements.txt
```

### Frontend Setup
Navigate to the frontend directory and install the required dependencies:
```bash
cd frontend
npm install
```

### Database Setup
1. Create a new MySQL database.
2. Update the database connection string in the configuration file (e.g., `.env` or `config.py`).
3. Set up the database schema (migrate if needed).

### Run the Application
1. Start the backend server:
   ```bash
   uvicorn main:app --reload
   ```
2. In a new terminal window, start the React frontend:
   ```bash
   npm start
   ```
3. Open your browser and go to `http://localhost:3000` to access the application.

## Security Vulnerabilities
This project includes both vulnerable and secure versions to demonstrate common web vulnerabilities such as SQL Injection (SQLi) and Cross-Site Scripting (XSS). It is meant for educational purposes only.

### SQL Injection Example
A demonstration of an SQL injection attack can be performed on the vulnerable version of the system by manipulating the login input.

### XSS Example
Cross-Site Scripting (XSS) attacks can be demonstrated by submitting malicious scripts in form fields that are not properly sanitized.
