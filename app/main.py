from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from .database import Base, engine, SessionLocal
from . import schemas, crud, models

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Wallet Service",
    description="""Simple wallet APIs:
- List Users (with wallet balance)
- Adjust/Set Wallet Balance (records a transaction)
- Fetch Transactions by user_id

Swagger UI: /docs
ReDoc: /redoc
""",
    version="1.0.0",
)

# CORS (open by default for demo)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/health", tags=["Meta"])
def health():
    return {"status": "ok"}

@app.get("/users", response_model=list[schemas.UserOut], tags=["Users"])
def list_users(db: Session = Depends(get_db)):
    return crud.get_users(db)

@app.post("/users", response_model=schemas.UserOut, status_code=status.HTTP_201_CREATED, tags=["Users"])
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user)

@app.post("/users/{user_id}/wallet/adjust", response_model=schemas.UserOut, tags=["Wallet"])
def adjust_wallet(user_id: int, payload: schemas.WalletAdjustIn, db: Session = Depends(get_db)):
    user, err = crud.adjust_wallet(db, user_id, payload)
    if err:
        raise HTTPException(status_code=404, detail=err)
    return user

@app.get("/users/{user_id}/transactions", response_model=list[schemas.TransactionOut], tags=["Transactions"])
def fetch_transactions(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.list_transactions(db, user_id)
