# from datetime import datetime, timedelta, timezone
# from typing import Annotated, Set
# from fastapi import FastAPI, Depends, HTTPException, status
# from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# from pydantic import BaseModel, EmailStr
# from passlib.context import CryptContext
# import jwt
# from sqlalchemy import create_engine, Column, Integer, String
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker, Session
# from fastapi.security import OAuth2PasswordBearer
# from fastapi.middleware.trustedhost import TrustedHostMiddleware
# from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
# SECRET_KEY = "your-super-secret-key-change-this-in-production"
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30

# # --- DATABASE SETUP ---
# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base = declarative_base()


# class DBUser(Base):
#     __tablename__ = "users"
#     id = Column(Integer, primary_key=True, index=True)
#     username = Column(String, unique=True, index=True, nullable=False)
#     email = Column(String, unique=True, index=True, nullable=False)
#     hashed_password = Column(String, nullable=False)

# Base.metadata.create_all(bind=engine)

# # --- SECURITY & UTILS ---
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# # In-memory blacklist for logged-out tokens (Use Redis/DB in production)
# TOKEN_BLACKLIST: Set[str] = set()

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# def hash_password(password: str) -> str:
#     return pwd_context.hash(password)

# def verify_password(plain_password: str, hashed_password: str) -> bool:
#     return pwd_context.verify(plain_password, hashed_password)

# def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
#     to_encode = data.copy()
#     expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))
#     to_encode.update({"exp": expire})
#     return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# # --- PYDANTIC SCHEMAS ---
# class UserCreate(BaseModel):
#     username: str
#     email: EmailStr
#     password: str

# class UserLogin(BaseModel):
#     username: str
#     password: str

# class UserResponse(BaseModel):
#     id: int
#     username: str
#     email: EmailStr

#     class Config:
#         from_attributes = True

# class Token(BaseModel):
#     access_token: str
#     token_type: str

# # --- DEPENDENCY FOR PROTECTED ROUTES ---
# def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)) -> DBUser:
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
    
#     if token in TOKEN_BLACKLIST:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED, 
#             detail="Token has been invalidated (Logged out)."
#         )

#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username: str = payload.get("sub")
#         if username is None:
#             raise credentials_exception
#     except jwt.PyJWTError:
#         raise credentials_exception
        
#     user = db.query(DBUser).filter(DBUser.username == username).first()
#     if user is None:
#         raise credentials_exception
#     return user


# app = FastAPI(title="FastAPI Auth App")
# app.add_middleware(HTTPSRedirectMiddleware)
# app.add_middleware(
#     TrustedHostMiddleware, 
#     allowed_hosts=["*"]
# )
# @app.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
# def signup(user_in: UserCreate, db: Session = Depends(get_db)):
#     if db.query(DBUser).filter(DBUser.username == user_in.username).first():
#         raise HTTPException(status_code=400, detail="Username already registered")
#     if db.query(DBUser).filter(DBUser.email == user_in.email).first():
#         raise HTTPException(status_code=400, detail="Email already registered")
    
#     db_user = DBUser(
#         username=user_in.username,
#         email=user_in.email,
#         hashed_password=hash_password(user_in.password)
#     )
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user

# # @app.post("/login",)
# # def login(username: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
# #     user = db.query(DBUser).filter(DBUser.username == form_data.username).first()
# #     if not user or not verify_password(form_data.password, user.hashed_password):
# #         raise HTTPException(
# #             status_code=status.HTTP_401_UNAUTHORIZED,
# #             detail="Incorrect username or password",
# #             headers={"WWW-Authenticate": "Bearer"},
# #         )
    
# #     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
# #     access_token = create_access_token(
# #         data={"sub": user.username}, expires_delta=access_token_expires
# #     )
# #     return {"access_token": access_token, "token_type": "bearer"}

# @app.post("/login-with-oauth")
# def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

#     user = db.query(DBUser).filter(
#         DBUser.username == form_data.username
#     ).first()

#     if not user:
#         raise HTTPException(status_code=400, detail="Invalid credentials email")

#     if not verify_password(form_data.password, user.hashed_password):
#         raise HTTPException(status_code=401, detail="Invalid credentials password")

#     token = create_access_token({"sub": user.username})

#     return {
#         "access_token": token,
#         "token_type": "bearer"
#     }


# @app.post("/login",)
# def login(user:UserLogin, db: Session = Depends(get_db)):
#     usercheck = db.query(DBUser).filter(DBUser.username == user.username).first()
#     if not user or not verify_password(user.password, usercheck.hashed_password):
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect username or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
    
#     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(
#         data={"sub": user.username}, expires_delta=access_token_expires
#     )
#     return {"access_token": access_token, "token_type": "bearer"}


# @app.post("/logout")
# def logout(token: Annotated[str, Depends(oauth2_scheme)]):
#     # Add the current token to the blacklist
#     TOKEN_BLACKLIST.add(token)
#     return {"detail": "Successfully logged out"}

# @app.get("/me", response_model=UserResponse)
# def read_users_me(current_user: Annotated[DBUser, Depends(get_current_user)]):
#     return current_user




from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World from inside a secure Docker container!"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}