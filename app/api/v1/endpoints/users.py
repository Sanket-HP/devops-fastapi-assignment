from typing import List
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
import logging

from app.api.deps import get_db, get_cache
from app.models.user import User as DBUser
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.services.cache import CacheService

logger = logging.getLogger(__name__)
router = APIRouter()

CACHE_KEY_USERS_LIST = "users:list"

@router.get("", response_model=List[UserResponse])
def read_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    cache: CacheService = Depends(get_cache),
):
    # Cache key includes pagination params to prevent cache pollution
    cache_key = f"{CACHE_KEY_USERS_LIST}:{skip}:{limit}"
    
    # Attempt to retrieve from cache
    cached_data = cache.get(cache_key)
    if cached_data is not None:
        logger.info(f"Cache hit for key '{cache_key}'")
        return cached_data

    logger.info(f"Cache miss for key '{cache_key}'. Fetching from DB.")
    users = db.query(DBUser).offset(skip).limit(limit).all()
    
    # Serialize results to Pydantic schemas, dump to dicts, then cache
    serialized_users = [UserResponse.model_validate(u).model_dump() for u in users]
    cache.set(cache_key, serialized_users, expire_seconds=300)
    
    return users

@router.get("/{id}", response_model=UserResponse)
def read_user(
    id: int,
    db: Session = Depends(get_db),
):
    user = db.query(DBUser).filter(DBUser.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {id} not found"
        )
    return user

@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    user_in: UserCreate,
    db: Session = Depends(get_db),
    cache: CacheService = Depends(get_cache),
):
    # Verify email uniqueness
    existing_user = db.query(DBUser).filter(DBUser.email == user_in.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    db_user = DBUser(
        email=user_in.email,
        name=user_in.name,
        is_active=user_in.is_active
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # Invalidate cache lists
    cache.clear_pattern(f"{CACHE_KEY_USERS_LIST}:*")
    logger.info("New user created. Users list cache invalidated.")
    
    return db_user

@router.put("/{id}", response_model=UserResponse)
def update_user(
    id: int,
    user_in: UserUpdate,
    db: Session = Depends(get_db),
    cache: CacheService = Depends(get_cache),
):
    db_user = db.query(DBUser).filter(DBUser.id == id).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {id} not found"
        )
        
    update_data = user_in.model_dump(exclude_unset=True)
    
    # Verify email uniqueness if being updated
    if "email" in update_data and update_data["email"] != db_user.email:
        existing_user = db.query(DBUser).filter(DBUser.email == update_data["email"]).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
            
    for field, value in update_data.items():
        setattr(db_user, field, value)
        
    db.commit()
    db.refresh(db_user)
    
    # Invalidate cache lists
    cache.clear_pattern(f"{CACHE_KEY_USERS_LIST}:*")
    logger.info(f"User {id} updated. Users list cache invalidated.")
    
    return db_user

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    id: int,
    db: Session = Depends(get_db),
    cache: CacheService = Depends(get_cache),
):
    db_user = db.query(DBUser).filter(DBUser.id == id).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {id} not found"
        )
    
    db.delete(db_user)
    db.commit()
    
    # Invalidate cache lists
    cache.clear_pattern(f"{CACHE_KEY_USERS_LIST}:*")
    logger.info(f"User {id} deleted. Users list cache invalidated.")
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)
