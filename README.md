\# HemoBank - Blood Bank Management System



\## Project Overview

A full-stack web application for managing blood donations and inventory using Flask backend and PostgreSQL database.



\## Technology Stack

\- \*\*Frontend:\*\* HTML5, CSS3, JavaScript

\- \*\*Backend:\*\* Flask (Python)

\- \*\*Database:\*\* PostgreSQL

\- \*\*ORM:\*\* SQLAlchemy



\## Database Schema



\### Tables:

1\. \*\*donors\*\* - Stores blood donor information

&nbsp;  - id, name, age, email, phone, blood\_type, address, registered\_on, last\_donation



2\. \*\*donations\*\* - Records blood donations

&nbsp;  - id, donor\_id, donation\_date, quantity\_ml, hemoglobin, blood\_pressure, notes



3\. \*\*blood\_inventory\*\* - Manages blood stock

&nbsp;  - id, blood\_type, quantity\_ml, donation\_id, donation\_date, expiry\_date, status



\## Features

✅ Register blood donors

✅ Record blood donations

✅ Manage blood inventory

✅ Track 90-day donation rule

✅ Monitor blood expiry dates

✅ View real-time dashboard statistics

✅ Search and filter donors by blood type



\## How to Run



\### Prerequisites

\- Python 3.8+

\- PostgreSQL 15+

\- pip (Python package manager)



\### Setup

1\. Clone repository

2\. Create virtual environment: `python -m venv venv`

3\. Activate: `venv\\Scripts\\activate`

4\. Install dependencies: `pip install -r requirements.txt`

5\. Configure `.env` file with database credentials

6\. Run: `python app.py`

7\. Open: http://localhost:5000



\## API Endpoints



\### Donors

\- GET `/api/donors` - Get all donors

\- POST `/api/donors/register` - Register new donor

\- GET `/api/donors/<id>` - Get donor details

\- PUT `/api/donors/<id>` - Update donor

\- DELETE `/api/donors/<id>` - Delete donor



\### Donations

\- POST `/api/donations/record` - Record donation

\- GET `/api/donations` - Get all donations

\- GET `/api/donations/donor/<donor\_id>` - Get donor's donations



\### Inventory

\- GET `/api/inventory` - Get blood inventory

\- GET `/api/inventory/blood-type/<type>` - Get by blood type

\- PUT `/api/inventory/use/<id>` - Mark as used



\### Dashboard

\- GET `/api/dashboard/stats` - Get statistics



\## Database Constraints

\- 90-day minimum between donations per donor

\- Blood expires in 35 days

\- Email and phone must be unique

\- Age between 18-65

\- Hemoglobin minimum 12.5 g/dL



\## Author

Eugintony



\## Date

February 2026

