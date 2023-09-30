from sqlalchemy.orm import Session
from database.models import Product, Sale
from datetime import datetime
from random import randint

def populate_demo_data(db: Session):
    # Add demo products
    products = [
        Product(name="Product 1", description="Description 1", price=10.99),
        Product(name="Product 2", description="Description 2", price=19.99),
    ]
    db.bulk_save_objects(products)
    db.commit()

    # Add demo sales
    for product_id in range(1, 3):
        for _ in range(10):
            sale = Sale(product_id=product_id, sale_date=datetime.now(), quantity=randint(1, 10))
            db.add(sale)
    db.commit()

if __name__ == "__main__":
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from database.models import Base
    DATABASE_URL = "mysql+mysqlconnector://username:password@localhost/dbname"
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    populate_demo_data(db)
    db.close()
