
<h1 align="center">E-commerce-Admin-api# 👋</h1>
This is the backend API for the E-commerce Admin Dashboard, designed to provide insights into sales, revenue, and inventory status, and allow product registration.

## Features

- **Sales Status:** Retrieve, filter, and analyze sales data.
- **Revenue Analysis:** Analyze revenue on a daily, weekly, monthly, and annual basis.
- **Inventory Management:** View current inventory status, including low stock alerts, and update inventory levels.
- **Product Registration:** Register new products.

## Technologies Used

- Python
- FastAPI
- MySQL

## Getting Started

To run this project locally, follow these steps:

1. Clone the repository:

   ```bash
   git clone https://github.com/Muqqu/E-commerce-Admin-api.git

2. Set up your database and configure the database connection in config.py.
3.  Run the FastAPI application:
   uvicorn main:app --reload

4. Access the API at http://localhost:8000 in your web browser or API client.

**API Endpoints**
Sales Status: /sales/
Revenue Analysis: /revenue/
Inventory Management: /inventory/
Product Registration: /products/

Database Schema
For information about the database schema and relationships, see Database Schema.





