from fastapi import FastAPI, HTTPException, Query
from datetime import datetime, time, timedelta
from database.models import Product, Sale, InventoryUpdate
from config.db_config import conn
from faker import Faker
import random

app = FastAPI()
# Endpoint to retrieve all sales data
@app.get("/sales")
def get_all_sales():
        try:
            cursor = conn.cursor(dictionary=True)
            select_query = "SELECT * FROM sales"
            cursor.execute(select_query)
            sales = cursor.fetchall()
            cursor.close()
            return sales
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        
# Endpoint to filter sales data
@app.get("/sales/filter")
def filter_sales(
    product_id: int = Query(None, description="Filter by product ID"),
    start_date: str = Query(None, description="Start date for filtering (YYYY-MM-DD)"),
    end_date: str = Query(None, description="End date for filtering (YYYY-MM-DD)"),
):
    try:
        cursor = conn.cursor(dictionary=True)
        select_query = "SELECT * FROM sales WHERE 1"

        if product_id is not None:
            select_query += f" AND product_id = {product_id}"

        if start_date is not None:
            select_query += f" AND sale_date >= '{start_date}'"

        if end_date is not None:
            select_query += f" AND sale_date <= '{end_date}'"

        cursor.execute(select_query)
        sales = cursor.fetchall()
        cursor.close()
        return sales
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Sales analysis by date range
@app.get("/sales/analysis/")
async def sales_analysis(start_date: str, end_date: str):
    try:
        cursor = conn.cursor(dictionary=True)
        select_query = "SELECT SUM(quantity) AS total_sales FROM sales WHERE sale_date BETWEEN %s AND %s"
        cursor.execute(select_query, (start_date, end_date))
        total_sales = cursor.fetchone()
        cursor.close()
        if total_sales and total_sales['total_sales']:
            return {"total_sales": total_sales['total_sales']}
        else:
            return {"total_sales": 0}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
# Endpoint to analyze revenue on a daily basis
@app.get("/revenue/daily")
def analyze_daily_revenue(
    date: str = Query(None, description="Date for daily analysis (YYYY-MM-DD)")
):
    try:
        cursor = conn.cursor()
        if date is None:
            date = datetime.now().date()  # Default to today's date
        else:
            date = datetime.strptime(date, "%Y-%m-%d").date()

        select_query = (
            f"SELECT SUM(s.quantity * p.price) AS total_revenue " \
                           "FROM sales s " \
                           "JOIN products p ON s.product_id = p.id " \
            f"WHERE sale_date = '{date}'"
        )

        cursor.execute(select_query)
        daily_revenue = cursor.fetchone()[0]
        cursor.close()
        return {"date": date, "revenue": daily_revenue}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint to analyze revenue on a weekly basis
@app.get("/revenue/weekly")
def analyze_weekly_revenue():
    try:
        cursor = conn.cursor()
        end_date = datetime.now().date()  # Default to today's date
        start_date = end_date - timedelta(days=6)  # Calculate start date (1 week ago)

        select_query = (
            f"SELECT SUM(s.quantity * p.price) AS total_revenue " \
                           "FROM sales s " \
                           "JOIN products p ON s.product_id = p.id " \
            f"WHERE sale_date BETWEEN '{start_date}' AND '{end_date}'"
        )

        cursor.execute(select_query)
        weekly_revenue = cursor.fetchone()[0]
        cursor.close()
        return {"start_date": start_date, "end_date": end_date, "revenue": weekly_revenue}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint to analyze revenue on a monthly basis
@app.get("/revenue/monthly")
def analyze_monthly_revenue():
    try:
        cursor = conn.cursor()
        end_date = datetime.now().date()  # Default to today's date
        start_date = end_date.replace(day=1)  # Calculate start date (first day of the month)

        select_query = (
            f"SELECT SUM(s.quantity * p.price) AS total_revenue " \
                           "FROM sales s " \
                           "JOIN products p ON s.product_id = p.id " \
            f"WHERE sale_date BETWEEN '{start_date}' AND '{end_date}'"
        )

        cursor.execute(select_query)
        monthly_revenue = cursor.fetchone()[0]
        cursor.close()
        return {"start_date": start_date, "end_date": end_date, "revenue": monthly_revenue}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint to analyze revenue on an annual basis
@app.get("/revenue/annual")
def analyze_annual_revenue():
    try:
        cursor = conn.cursor()
        end_date = datetime.now().date()  # Default to today's date
        start_date = end_date.replace(month=1, day=1)  # Calculate start date (first day of the year)

        select_query = (
            f"SELECT SUM(s.quantity * p.price) AS total_revenue " \
                           "FROM sales s " \
                           "JOIN products p ON s.product_id = p.id " \
            f"WHERE sale_date BETWEEN '{start_date}' AND '{end_date}'"
        )

        cursor.execute(select_query)
        annual_revenue = cursor.fetchone()[0]
        cursor.close()
        return {"start_date": start_date, "end_date": end_date, "revenue": annual_revenue}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# Endpoint to compare revenue across different periods and categories
@app.get("/revenue/compare")
def compare_revenue(
    period: str = Query(None, description="Analysis period (daily, weekly, monthly, annual)"),
    category: str = Query(None, description="Product category"),
):
    try:
        cursor = conn.cursor()
        end_date = datetime.now().date()  # Default to today's date

        # Calculate start date based on the selected period
        if period == "daily":
            start_date = end_date  # For daily analysis, start and end dates are the same
        elif period == "weekly":
            start_date = end_date - timedelta(days=6)  # Calculate start date (1 week ago)
        elif period == "monthly":
            start_date = end_date.replace(day=1)  # Calculate start date (first day of the month)
        elif period == "annual":
            start_date = end_date.replace(month=1, day=1)  # Calculate start date (first day of the year)
        else:
            raise HTTPException(status_code=400, detail="Invalid analysis period")

        select_query = (
            f"SELECT SUM(s.quantity * p.price) AS total_revenue " \
                           "FROM sales s " \
                           "JOIN products p ON s.product_id = p.id " \
            f"WHERE sale_date BETWEEN '{start_date}' AND '{end_date}'"
        )

        if category is not None:
            select_query += f" AND category = '{category}'"

        select_query += " GROUP BY category"

        cursor.execute(select_query)
        revenue_data = cursor.fetchall()
        cursor.close()
        return revenue_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

# Endpoint to provide sales data by date range, product, and category
@app.get("/sales/filter")
def filter_sales(
    start_date: str = Query(None, description="Start date for filtering (YYYY-MM-DD)"),
    end_date: str = Query(None, description="End date for filtering (YYYY-MM-DD)"),
    product_id: int = Query(None, description="Product ID"),
    category: str = Query(None, description="Product category"),
):
    try:
        cursor = conn.cursor(dictionary=True)
        select_query = "SELECT * FROM sales s JOIN products p ON s.product_id = p.id WHERE 1"

        if start_date is not None:
            select_query += f" AND sale_date >= '{start_date}'"

        if end_date is not None:
            select_query += f" AND sale_date <= '{end_date}'"

        if product_id is not None:
            select_query += f" AND product_id = {product_id}"

        if category is not None:
            select_query += f" AND category = '{category}'"

        cursor.execute(select_query)
        sales_data = cursor.fetchall()
        cursor.close()
        return sales_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Create a new product
@app.post("/products/", response_model=Product)
async def create_product(product: Product):
    try:
        cursor = conn.cursor()
        insert_query = "INSERT INTO products (name, description, price) VALUES (%s, %s, %s)"
        cursor.execute(insert_query, (product.name, product.description, product.price,product.category))
        conn.commit()
        product_id = cursor.lastrowid
        cursor.close()
        return {"id": product_id, **product.dict()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Get product details by ID
@app.get("/products/{product_id}", response_model=Product)
async def get_product(product_id: int):
    try:
        cursor = conn.cursor(dictionary=True)
        select_query = "SELECT * FROM products WHERE id = %s"
        cursor.execute(select_query, (product_id,))
        product = cursor.fetchone()
        cursor.close()
        if product:
            return product
        else:
            raise HTTPException(status_code=404, detail="Product not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Record a new sale
@app.post("/sales/", response_model=Sale)
async def record_sale(sale: Sale):
    try:
        cursor = conn.cursor()
        insert_query = "INSERT INTO sales (product_id, quantity, sale_date) VALUES (%s, %s, %s)"
        cursor.execute(insert_query, (sale.product_id, sale.quantity, sale.sale_date))
        conn.commit()
        sale_id = cursor.lastrowid
        cursor.close()
        return {"id": sale_id, **sale.dict()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Revenue analysis
@app.get("/revenue/analysis/")
async def revenue_analysis(period: str, category: str = None):
    try:
        cursor = conn.cursor(dictionary=True)
        if category:
            select_query = "SELECT SUM(s.quantity * p.price) AS total_revenue " \
                           "FROM sales s " \
                           "JOIN products p ON s.product_id = p.id " \
                           "WHERE DATE_FORMAT(s.sale_date, %s) = DATE_FORMAT(NOW(), %s) " \
                           "AND p.category = %s"
            cursor.execute(select_query, (period, period, category))
        else:
            select_query = "SELECT SUM(s.quantity * p.price) AS total_revenue " \
                           "FROM sales s " \
                           "JOIN products p ON s.product_id = p.id " \
                           "WHERE DATE_FORMAT(s.sale_date, %s) = DATE_FORMAT(NOW(), %s)"
            cursor.execute(select_query, (period, period))
        total_revenue = cursor.fetchone()
        cursor.close()
        if total_revenue and total_revenue['total_revenue']:
            return {"total_revenue": total_revenue['total_revenue']}
        else:
            return {"total_revenue": 0}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
# Endpoint to view current inventory status by product ID
@app.get("/inventory/status/{product_id}")
async def get_inventory_status(product_id: int):
    try:
        cursor = conn.cursor(dictionary=True)
        select_query = "SELECT quantity FROM inventory WHERE product_id = %s"
        cursor.execute(select_query, (product_id,))
        current_quantity = cursor.fetchone()
        cursor.close()
        conn.close()

        if current_quantity:
            return {"product_id": product_id, "quantity": current_quantity["quantity"]}
        else:
            raise HTTPException(status_code=404, detail="Product not found in inventory")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint to check for low stock alerts
@app.get("/inventory/low-stock-alerts/")
async def low_stock_alerts():
    try:
        cursor = conn.cursor(dictionary=True)
        select_query = "SELECT product_id, quantity FROM inventory WHERE quantity < %s"
        cursor.execute(select_query, (10,))  # Change 10 to your desired low stock threshold
        low_stock_products = cursor.fetchall()
        cursor.close()
        conn.close()

        if low_stock_products:
            return low_stock_products
        else:
            return {"message": "No low stock products found"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# ... Other imports and setup ...

# Endpoint to update inventory levels and track changes
@app.put("/inventory/update/", response_model=InventoryUpdate)
async def update_inventory(update: InventoryUpdate):
    try:

        cursor = conn.cursor(dictionary=True)

        # Check if the product exists in inventory
        print(update.product_id)
        select_query = "SELECT quantity FROM inventory WHERE product_id = %s"
        cursor.execute(select_query, (update.product_id,))
        current_quantity = cursor.fetchone()
        print(current_quantity)

        if current_quantity:
            # Calculate the new quantity
            new_quantity = current_quantity['quantity'] + update.quantity

            # Update the inventory with the new quantity and track the change
            update_query = "UPDATE inventory SET quantity = %s WHERE product_id = %s"
            cursor.execute(update_query, (new_quantity, update.product_id))

            # Insert a record to track the change over time
            insert_change_query = "INSERT INTO inventory_changes (product_id, quantity_change) VALUES (%s, %s)"
            cursor.execute(insert_change_query, (update.product_id, update.quantity))

            conn.commit()
            cursor.close()
            conn.close()
            
            # Return the updated inventory data
            return {"product_id": update.product_id, "quantity_change": update.quantity}
        else:
            cursor.close()
            conn.close()
            raise HTTPException(status_code=404, detail="Product not found in inventory")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/populate_demo_data/products")
async def generate_fake_product(data: int = Query(None, description="How many data you want to generate"),):
    
    try:
    # Generate fake product data
        cursor = conn.cursor(dictionary=True)
        for _ in range(data):
            print(data)
            fake = Faker()
            
            product = {
                "name": fake.word(ext_word_list=["Laptop", "TV", "Phone", "Tablet"]),
                "description": fake.sentence(),
                "price": round(random.uniform(100, 1000), 2),
                "category": fake.word(ext_word_list=["Electronics", "Clothing", "Home", "Toys"]),
            }
            cursor.execute(
                    "INSERT INTO products (name, description, price, category) "
                    "VALUES (%s, %s, %s, %s)",
                    (product["name"], product["description"],product["price"] ,product["category"] ),
                )
        conn.commit()
        cursor.close()
        conn.close()
     
        print(f"Inserted {data} rows of dummy data successfully.")
        
        return "Inserted"
    except Exception as e:
        print(f"Error: {e}")        

@app.post("/populate_demo_data/sales")
async def generate_fake_sales(data: int = Query(None, description="How many data you want to generate"),):
    
    try:
    # Generate fake product data
        cursor = conn.cursor(dictionary=True)
        for _ in range(data):
            print(data)
            fake = Faker()
            
            product = {
                
                "product_id": round(random.uniform(1, 5), 2),
                "quantity": round(random.uniform(1, 10), 2),
                "sales_date": (datetime.now() - timedelta(days=random.uniform(0, 365))).strftime("%Y-%m-%d %H:%M:%S"),
            }
            cursor.execute(
                    "INSERT INTO sales(product_id, quantity, sale_date)  "
                    "VALUES (%s, %s, %s)",
                    (product["product_id"], product["quantity"],product["sales_date"]  ),
                )
        conn.commit()
        cursor.close()
        conn.close()
     
        print(f"Inserted {data} rows of dummy data successfully.")
        
        return "Inserted"
    except Exception as e:
        print(f"Error: {e}")
        

@app.post("/populate_demo_data/inventory")
async def generate_fake_inventory(data: int = Query(None, description="How many data you want to generate"),):
    
    try:
    # Generate fake product data
        cursor = conn.cursor(dictionary=True)
        for _ in range(data):
            fake = Faker()
            
            product = {
                "product_id": round(random.uniform(1, 5), 2),
                "quantity": round(random.uniform(1, 109), 2),
               
            }
            cursor.execute(
                    "INSERT INTO inventory (product_id, quantity) "
                    "VALUES (%s, %s)",
                    (product["product_id"], product["quantity"]),
                )
        conn.commit()
        cursor.close()
        conn.close()
     
        print(f"Inserted {data} rows of dummy data successfully.")
        
        return "Inserted"
    except Exception as e:
        print(f"Error: {e}")

        
   