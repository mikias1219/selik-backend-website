from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.models import Base, User, Product, Tutorial, Service, Request
from app.auth import get_password_hash

Base.metadata.create_all(bind=engine)

def init_db():
    db = SessionLocal()
    try:
        # Create users
        if not db.query(User).first():
            users = [
                User(
                    username="admin",
                    email="admin@seliklabs.com",
                    hashed_password=get_password_hash("password"),
                    is_admin=True
                ),
                User(
                    username="user1",
                    email="user1@seliklabs.com",
                    hashed_password=get_password_hash("userpass"),
                    is_admin=False
                ),
            ]
            db.add_all(users)
            db.commit()
            print("Users created")

        # Create products
        if not db.query(Product).first():
            products = [
                Product(
                    name="PlayStation 5",
                    type="Standard",
                    price=499.99,
                    description="Next-gen gaming with 4K visuals and lightning-fast SSD.",
                    image="/products/ps5.jpg",
                    posted_date="2025-04-01"
                ),
                Product(
                    name="PlayStation 5 Slim",
                    type="Slim",
                    price=449.99,
                    description="Compact design with the same powerful performance.",
                    image="/products/ps5-slim.jpg",
                    posted_date="2025-04-10"
                ),
            ]
            db.add_all(products)
            db.commit()
            print("Products created")

        # Create tutorials
        if not db.query(Tutorial).first():
            tutorials = [
                Tutorial(
                    title="How to Clean Your PlayStation 5",
                    content="Steps:\n1. Use a soft, dry cloth.\n2. Clean vents with compressed air.",
                    category="Cleaning",
                    price=9.99,
                    posted_date="2025-04-01",
                    video_url="https://www.youtube.com/embed/VIDEO_ID_1"
                ),
                Tutorial(
                    title="How to Upgrade PS5 SSD",
                    content="Steps:\n1. Purchase compatible SSD.\n2. Follow installation guide.",
                    category="Upgrades",
                    price=9.99,
                    posted_date="2025-04-10",
                    video_url="https://www.youtube.com/embed/VIDEO_ID_2"
                ),
                Tutorial(
                    title="PS5 Fan Replacement",
                    content="Steps:\n1. Open console carefully.\n2. Replace fan unit.",
                    category="Repair",
                    price=9.99,
                    posted_date="2025-04-15",
                    video_url="https://www.youtube.com/embed/VIDEO_ID_3"
                ),
            ]
            db.add_all(tutorials)
            db.commit()
            print("Tutorials created")

        # Create services
        if not db.query(Service).first():
            services = [
                Service(
                    name="PS5 Cleaning Kit",
                    category="Kits",
                    price=29.99,
                    description="Professional cleaning kit for PS5 maintenance.",
                    image="/services/cleaning-kit.jpg",
                    video_url="https://www.youtube.com/embed/VIDEO_ID_1"
                ),
                Service(
                    name="PS5 Repair Service",
                    category="Professional",
                    price=99.99,
                    description="Professional repair for PS5 hardware issues.",
                    video_url="https://www.youtube.com/embed/VIDEO_ID_3"
                ),
            ]
            db.add_all(services)
            db.commit()
            print("Services created")

        # Create sample request
        if not db.query(Request).first():
            user = db.query(User).filter(User.username == "user1").first()
            request = Request(
                user_id=user.id,
                title="Request for PS5 Controller Repair Tutorial",
                description="Please provide a tutorial on fixing PS5 controller drift.",
                posted_date="2025-04-20",
                status="pending"
            )
            db.add(request)
            db.commit()
            print("Sample request created")

    finally:
        db.close()

if __name__ == "__main__":
    init_db()