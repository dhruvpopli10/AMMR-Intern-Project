from sqlalchemy.orm import Session
from . import models, schemas

def get_users(db: Session):
    return db.query(models.User).all()

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def create_user(db: Session, user: schemas.UserCreate):
    obj = models.User(name=user.name, email=user.email, phone=user.phone, wallet_balance=0.0)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def list_transactions(db: Session, user_id: int):
    return db.query(models.Transaction).filter(models.Transaction.user_id == user_id).order_by(models.Transaction.created_at.desc()).all()

def adjust_wallet(db: Session, user_id: int, payload: schemas.WalletAdjustIn):
    user = get_user(db, user_id)
    if not user:
        return None, "User not found"

    if payload.mode == "delta":
        # Add (or subtract) amount
        user.wallet_balance = round((user.wallet_balance or 0.0) + payload.amount, 2)
        txn_type = models.TxnType.credit if payload.amount >= 0 else models.TxnType.debit
        txn = models.Transaction(user_id=user_id, amount=payload.amount, type=txn_type, description=payload.description)
    else:
        # Set absolute balance; record adjustment difference for audit
        diff = round(payload.amount - (user.wallet_balance or 0.0), 2)
        user.wallet_balance = round(payload.amount, 2)
        txn = models.Transaction(user_id=user_id, amount=diff, type=models.TxnType.adjust, description=payload.description or "Set balance")

    db.add(txn)
    db.add(user)
    db.commit()
    db.refresh(user)
    db.refresh(txn)
    return user, None
