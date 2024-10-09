# Computer Security Course Final Unsecure Project: SQL Injection and XSS Attacks Demonstration 
# Develop a web system for an imaginary communication company called Comunication_LTD

## Description
This project was developed for the 
**Computer Security** course to demonstrate common web vulnerabilities through a simulated telecommunications company, 
**Communication_LTD**. The project includes both vulnerable and secure versions to showcase how attacks like 
**SQL Injection (SQLi) and Cross-Site Scripting (XSS)** can be exploited and mitigated. Additionally, we implemented custom functionality for managing 
**internet packages** and **marketing sectors**, which enhances the user experience and expands client management capabilities. The frontend uses 
**React**, the backend is built with **FastAPI** (Python), and **MySQL** is the relational database.

## Features
- **User Register**: Create accounts for new users.
- **User Login**: Secure login functionality.
- **Password Recovery**: Email verification to reset passwords.
- **Password Change**: Secure password update process.
- **Client Management**: Add, edit, and delete client records.
- **Internet Packages**: Customers can select personalized internet packages based on bandwidth, data limits, and price.
- **Sectors**: Customers are assigned to specific marketing sectors according to their target audience or region.
- **Logout**: Securely log out of the system.

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
