from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker


# 1. Engine
engine = create_engine("sqlite:///test.db", echo=True)

# # 2. Base
Base = declarative_base()

# 3. Model
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    password = Column(String)


# # 4. Create table
# Base.metadata.create_all(engine)

#  Session
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

# 6. Insert
session.add(User(name="sajid", age=15,password="123"))
session.commit()

# 7. Read
users = session.query(User).all()
user = session.query(User).where(User.age<25).all()


for u in user:
    print(u.password)


for user in users:
    print(user.name)

# import asyncio
# from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
# from sqlalchemy.orm import DeclarativeBase



# DATABASE_URL = "sqlite+aiosqlite:///./test.db"

# engine = create_async_engine(
#     DATABASE_URL,
#     echo=True
# )

# SessionLocal = async_sessionmaker(
#     bind=engine,
#     class_=AsyncSession,
#     expire_on_commit=False
# )

# # 3. Base class
# class Base(DeclarativeBase):
#     pass

# class User(Base):
#     __tablename__ = "users"
#     id = Column(Integer, primary_key=True)
#     name = Column(String)
#     age = Column(Integer)


# async def init_db():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)

# async def main():

#     await init_db() 

#     async with SessionLocal() as session:
#         user = User(name="sajid", age=15)

#         session.add(user)
#         await session.commit()
#         await session.refresh(user)

#         print(user.name)

# asyncio.run(main())

