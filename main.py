from fastapi import FastAPI, Depends, HTTPException, Response, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import sessionmaker, Session, declarative_base, Mapped, mapped_column
from sqlalchemy import create_engine, String, Integer
from dotenv import load_dotenv
from typing import Annotated
from pydantic import BaseModel, EmailStr
from cryptography.fernet import Fernet, InvalidToken
from io import BytesIO
from PIL import Image
import os

load_dotenv(dotenv_path="important.env")

# AuthX setup (simplified)
from authx import AuthX, AuthXConfig

config = AuthXConfig()
config.JWT_SECRET_KEY = os.getenv("jwt_secret_key")
config.JWT_ACCESS_COOKIE_NAME = "my_access_token"
config.JWT_TOKEN_LOCATION = ["cookies"]
security = AuthX(config=config)

# Database setup
user = os.getenv("user")
password = os.getenv("password")
host = os.getenv("host", "127.0.0.1")
port = os.getenv("port", "5432")
db_name = os.getenv("db_name")
database_url = f"postgresql://{user}:{password}@{host}:{port}/{db_name}"
engine = create_engine(database_url)
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)

# Fernet setup
hasher_key = os.getenv("fernet_secret_key").encode("utf-8")
fernet = Fernet(hasher_key)

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    unfilled_subscribes: Mapped[int] = mapped_column(Integer, default=0)
    url: Mapped[str] = mapped_column(String, nullable=False)

    def set_password(self, password: str):
        self.hashed_password = fernet.encrypt(password.encode()).decode()
        return self

    def set_email(self, email: str):
        self.email = email
        return self

    def set_username(self, username: str):
        self.username = username
        return self

class UserLoginSchema(BaseModel):
    username: str
    email: EmailStr
    password: str

# Create tables
try:
    Base.metadata.create_all(engine)
    print("✅ Database connected and tables created.")
except Exception as e:
    print(f"❌ Database connection failed: {e}")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- API Routes ---

@app.post("/signup/{url}")
def signup(creds: UserLoginSchema, url: str, db: db_dependency):
    existing_user = db.query(User).filter_by(username=creds.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists.")
    user = User().set_username(creds.username).set_email(creds.email).set_password(creds.password)
    user.url = url
    db.add(user)
    db.commit()
    db.refresh(user)
    print(f"✅ User created: {user.username} | Email: {user.email}")
    return {"msg": "User registered successfully."}

@app.post("/login/{url}")
def login(creds: UserLoginSchema, url: str, db: db_dependency, response: Response):
    user = db.query(User).filter_by(username=creds.username).first()
    if user:
        try:
            decrypted_password = fernet.decrypt(user.hashed_password.encode()).decode()
            if decrypted_password == creds.password:
                token = security.create_access_token(uid=url)
                response.set_cookie(config.JWT_ACCESS_COOKIE_NAME, token)
                return {"access_token": token}
        except InvalidToken:
            pass
    raise HTTPException(status_code=401, detail="User not authorized!")

@app.get("/url-from-username/{username}")
def get_url_by_username(username: str, db: db_dependency):
    user = db.query(User).filter_by(username=username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    return user.url

@app.get("/username-from-url/{url}")
def get_username_by_url(url: str, db: db_dependency):
    user = db.query(User).filter_by(url=url).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    return user.username

@app.post("/upload-screenshot")
async def upload_screenshot(file: UploadFile = File(...)):
    image_bytes = await file.read()
    uploaded_image = Image.open(BytesIO(image_bytes))
    reference_image = Image.open("subscribed.png")  # Make sure 'subscribed.png' exists

    from pyautogui import locate

    location = locate(reference_image, uploaded_image)
    if location:
        return {"found": True, "msg": "Subscribed text found!"}
    else:
        return {"found": False, "msg": "Subscribed text not found."}
