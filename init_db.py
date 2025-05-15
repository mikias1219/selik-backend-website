from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app import models, auth
from datetime import datetime

models.Base.metadata.create_all(bind=engine)

def init_db():
    db = SessionLocal()
    try:
        # Create users
        hashed_password = auth.get_password_hash("password")
        user1 = models.User(
            username="admin",
            email="admin@example.com",
            hashed_password=hashed_password,
            is_admin=True
        )
        user2 = models.User(
            username="user1",
            email="user1@example.com",
            hashed_password=auth.get_password_hash("userpass"),
            is_admin=False
        )
        db.add_all([user1, user2])

        # Create products
        product1 = models.Product(
            name="PS5 Controller",
            type="Controller",
            price=69.99,
            description="Official DualSense controller for PS5.",
            image="https://example.com/ps5_controller.jpg",
            posted_date=datetime.now()
        )
        db.add(product1)

        # # Create tutorials
        # tutorial1 = models.Tutorial(
        #     title="PS5 Cleaning Guide",
        #     content="Step-by-step guide to clean your PS5 console.",
        #     category="Cleaning",
        #     price=9.99,
        #     posted_date=datetime.now(),
        #     video_url="https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # Replace with real video
        # )
        # tutorial2 = models.Tutorial(
        #     title="PS5 SSD Upgrade",
        #     content="How to upgrade your PS5 storage with an SSD.",
        #     category="Upgrades",
        #     price=9.99,
        #     posted_date=datetime.now(),
        #     video_url="https://www.youtube.com/watch?v=7Yc3ZcrwtAA"  # Replace with real video
        # )
        # db.add_all([tutorial1, tutorial2])

        # Create services
        service1 = models.Service(
            name="PS5 Repair Service",
            category="Professional",
            price=99.99,
            description="Professional repair for PS5 hardware issues.",
            image="https://example.com/repair_service.jpg",
            video_url="https://www.youtube.com/watch?v=3b5zCFSmVvY",  # Replace with real video
            posted_date=datetime.now()
        )
        service2 = models.Service(
            name="Cleaning Kit",
            category="Kits",
            price=29.99,
            description="Complete cleaning kit for PS5 maintenance.",
            image="https://example.com/cleaning_kit.jpg",
            video_url="https://www.youtube.com/watch?v=9bZkp7q19f0",  # Replace with real video
            posted_date=datetime.now()
        )
        db.add_all([service1, service2])

        # Create a sample request
        request1 = models.Request(
            user_id=2,
            title="PS5 Fan Replacement Guide",
            description="Need a tutorial for replacing the PS5 fan.",
            status="pending",
            posted_date=datetime.now()
        )
        db.add(request1)

        db.commit()
    finally:
        db.close()

if __name__ == "__main__":
    init_db()