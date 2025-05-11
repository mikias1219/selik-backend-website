from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app import models
from app.database import engine
from app.routes import auth, products, tutorials, services, cart, purchases, requests, media
import os

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Frontend origin
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Create media directory if it doesn't exist
MEDIA_DIR = "media"
if not os.path.exists(MEDIA_DIR):
    os.makedirs(MEDIA_DIR)

# Include routers
app.include_router(auth.router, prefix="/api")
app.include_router(products.router, prefix="/api")
app.include_router(tutorials.router, prefix="/api")
app.include_router(services.router, prefix="/api")
app.include_router(cart.router, prefix="/api")
app.include_router(purchases.router, prefix="/api")
app.include_router(requests.router, prefix="/api")
app.include_router(media.router, prefix="/api")