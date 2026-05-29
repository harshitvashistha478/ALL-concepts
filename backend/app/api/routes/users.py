import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.models.user import User
from app.schemas.schema import UserResponse
from app.utils.users_extras import generate_test_username

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/create-test-user", response_model=UserResponse)
async def create_test_user(db: AsyncSession = Depends(get_db)):
    try:
        while True:
            name = generate_test_username()
            existing = await db.execute(select(User).where(User.name == name))
            if not existing.scalar_one_or_none():
                break

        user = User(id=str(uuid.uuid4()), name=name)
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user
    
    except Exception as e:
        from fastapi import HTTPException
        raise HTTPException(status_code=500, detail=f"Error creating test user: {e}")


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: str, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        if not user:
            from fastapi import HTTPException
            raise HTTPException(status_code=404, detail="User not found")
        return user
    
    except Exception as e:
        from fastapi import HTTPException
        raise HTTPException(status_code=500, detail=f"Error retrieving user: {e}")
