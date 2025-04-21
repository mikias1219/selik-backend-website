from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app import models, crud
from app.auth import get_password_hash
from datetime import date

def init_db():
    db = SessionLocal()
    try:
        # Create admin user
        username = "admin"
        password = "password"
        hashed_password = get_password_hash(password)
        if not crud.get_user_by_username(db, username):
            crud.create_user(db, username, hashed_password)
        print("Admin user created")

        # Create initial products
        products = [
            {
                "name": "PlayStation 5",
                "type": "Standard",
                "price": 499.99,
                "description": "Next-gen gaming with 4K visuals and lightning-fast SSD.",
                "image": "/products/ps5.jpg",
                "posted_date": date(2025, 4, 1)
            },
            {
                "name": "PlayStation 5 Slim",
                "type": "Slim",
                "price": 449.99,
                "description": "Compact design with the same powerful performance.",
                "image": "/products/ps5-slim.jpg",
                "posted_date": date(2025, 4, 10)
            }
        ]
        for product in products:
            if not db.query(models.Product).filter(models.Product.name == product["name"]).first():
                db_product = models.Product(**product)
                db.add(db_product)
        db.commit()
        print("Initial products created")

        # Create initial tutorials
        tutorials = [
            {
                "title": "How to Maintain Your PlayStation 5",
                "content": "Learn how to keep your PlayStation 5 in top condition:\n\n1. **Cleaning**: Use a soft, dry cloth to wipe the console weekly. Avoid water or harsh chemicals.\n2. **Ventilation**: Ensure the console is in a well-ventilated area to prevent overheating.\n3. **Disc Care**: Store discs in their cases to avoid scratches.\n4. **Software Updates**: Regularly check for system updates via Settings > System > System Software.\n5. **Controller Maintenance**: Clean controllers with a damp cloth and check battery levels.\n\nFor detailed support, contact our team at support@seliklabs.com.",
                "posted_date": date(2025, 4, 1)
            }
        ]
        for tutorial in tutorials:
            if not db.query(models.Tutorial).filter(models.Tutorial.title == tutorial["title"]).first():
                db_tutorial = models.Tutorial(**tutorial)
                db.add(db_tutorial)
        db.commit()
        print("Initial tutorials created")
    finally:
        db.close()

if __name__ == "__main__":
    models.Base.metadata.create_all(bind=engine)
    init_db()