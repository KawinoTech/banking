# Banking Financial Management API

This project is a **comprehensive financial management API**, built using **FastAPI** and designed to handle a range of financial operations, including user management, transactions, loan management, term deposits, card services, and more.

---

## Features

### **User Management**
- Secure authentication and authorization using JWT and HMAC.
- Password management using bcrypt for secure hashing.

### **Financial Operations**
- **Transaction Types**: Transfers, bill payments, airtime purchases, goods purchases, and wallet top-ups.
- **Account Types**: Support for personal accounts, corporate accounts, and foreign currency accounts.

### **Loan Management**
- Supports various loan types: personal loans, business loans, and mortgages.
- Automated daily interest calculation for loan accounts.

### **Savings & Investments**
- Term deposit management with interest accrual.
- Compound interest calculations for savings accounts.

### **Card Services**
- Credit, debit, and prepaid card applications.
- Automatic handling of expiry dates and card status updates.

### **Customer Service**
- Client help request management for support ticketing.
- Issue reporting with tracking features.

### **Admin Tools**
- Customer-to-manager relationship management using many-to-many associations.

### **Security Features**
- Rate limiting using Redis to protect endpoints.
- Structured error handling and robust logging for easier debugging and error tracking.

---

## Installation

### Prerequisites

- Python 3.9 or higher
- MySQL database server
- Redis (for rate-limiting functionality)

### Installation Steps

1. **Clone the Repository**
   ```bash
   git clone https://github.com/KawinoTech/banking.git
   cd fastapi

2. **Clone the Repository**
    python -m venv venv
    source venv/bin/activate  # On macOS/Linux
    venv\Scripts\activate     # On Windows

3. **Install Dependencies**
    pip install -r requirements.txt


4. **Setup Environment Variables**
SECRET_KEY=your_secret_key
DATABASE_USERNAME=your_db_username
DATABASE_PASSWORD=your_db_password
DATABASE_HOST=localhost
DATABASE_NAME=your_db_name
ACCESS_TOKEN_EXPIRATION=30  # Token expiry in minutes

5. **Start the Server**
uvicorn main:app --reload

## Usage
### Endpoints

FastAPI automatically generates interactive API documentation, accessible at:
Swagger UI: /docs

1. **User Management**
POST /post/create: Create a new user.
POST /post/login: Authenticate a user and retrieve an access token.
GET /post/get_customers: Retrieve all customers.

2. **Transaction Management**
POST /post/transfer: Create a transfer transaction.
POST /post/paybill: Make a bill payment transaction.
POST /post/buygoods: Create a goods purchase transaction.

3. **Card Services**
POST /post/debit_card_application: Apply for a debit card.
POST /post/credit_card_application: Apply for a credit card.
POST /post/prepaid_card_application: Apply for a prepaid card.

## Configuration
This application supports environment-specific configurations using .env files. Key variables include:
SECRET_KEY: Used for cryptographic operations.
DATABASE_USERNAME, DATABASE_PASSWORD, DATABASE_HOST, DATABASE_NAME: Database connection credentials.
ACCESS_TOKEN_EXPIRATION: The expiration time (in minutes) for JWT tokens.

## Technical Highlights
1. **SQLAlchemy ORM**

Models include users, transactions, loans, and term deposits.
Support for foreign keys and relationships, enabling efficient data querying.
Connection Pooling:

Efficient use of MySQL connections via create_engine with configurable parameters like pool_size and pool_recycle.
2. **Session Management**

get_db function ensures proper opening and closing of database sessions.
3. **Rate Limiting**

Redis integration ensures API rate limiting to prevent abuse and throttling.
4. **Logging**

SQL query logging enabled during development with echo=True in the database engine.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Contact
For inquiries or support, please reach out:

Author: Jeremy Kawino (Tech Assassin)
Email: techkawino@gmail.com
GitHub: [GitHub Profile](https://github.com/KawinoTech)