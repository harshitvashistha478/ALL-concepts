"""
User Routes:
POST /users/create-test-user → creates a test user with a unique auto-generated name
GET  /users/{user_id}        → get user details
"""
import uuid
import random
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.models.models import User
from app.schemas.schemas import UserResponse

router = APIRouter(prefix="/users", tags=["Users"])

# Fun, cyberpunk-ish name parts for test users
FIRST_PARTS = ["Pixel", "Cyber", "Neon", "Quantum", "Binary", "Synth", "Volt", "Data", "Node", "Hex"]
LAST_PARTS  = ["Walker", "Coder", "Runner", "Watcher", "Seeker", "Tracer", "Rider", "Drifter", "Scout", "Spark"]


def generate_test_username() -> str:
    """Generate a unique readable username like 'PixelWalker_4821'."""
    first = random.choice(FIRST_PARTS)
    last  = random.choice(LAST_PARTS)
    suffix = random.randint(1000, 9999)
    return f"{first}{last}_{suffix}"


@router.post("/create-test-user", response_model=UserResponse)
async def create_test_user(db: AsyncSession = Depends(get_db)):
    """
    Creates a test user with an auto-generated cyberpunk name.
    No sign-up form needed — just click and get a name.
    """
    # Make sure the name is unique
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


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="User not found")
    return user
