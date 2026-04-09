from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import UserCreate, UserLogin, Token, User as UserSchema, PasswordReset
from app.models import User, UserRole, UserPreference, Restaurant
from app.auth import get_password_hash, verify_password, create_access_token
from app.logger import get_logger
from app.exceptions import BadRequestException, UnauthorizedException, NotFoundException
import uuid

router = APIRouter(prefix="/auth", tags=["Authentication"])
logger = get_logger(__name__)

@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user (customer or restaurant owner)
    
    For customers:
    - role: "customer"
    - restaurant_id: not required
    
    For restaurant owners:
    - role: "owner"
    - restaurant_id: required (must be an existing restaurant)
    """
    logger.info(f"Registration attempt for email: {user_data.email} as {user_data.role.value}")
    
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        logger.warning(f"Registration failed - email already exists: {user_data.email}")
        raise BadRequestException("Email already registered")
    
    # Validate owner registration
    if user_data.role == UserRole.OWNER:
        if not user_data.restaurant_id:
            logger.warning(f"Owner registration failed - no restaurant_id provided: {user_data.email}")
            raise BadRequestException("Restaurant ID is required for owner registration")
        
        # Verify restaurant exists
        restaurant = db.query(Restaurant).filter(Restaurant.id == user_data.restaurant_id).first()
        if not restaurant:
            logger.warning(f"Owner registration failed - restaurant not found: {user_data.restaurant_id}")
            raise NotFoundException(f"Restaurant with ID {user_data.restaurant_id} not found")
        
        # Check if restaurant already has an owner
        existing_owner = db.query(User).filter(
            User.restaurant_id == user_data.restaurant_id,
            User.role == UserRole.OWNER
        ).first()
        if existing_owner:
            logger.warning(f"Owner registration failed - restaurant already has owner: {user_data.restaurant_id}")
            raise BadRequestException(f"Restaurant '{restaurant.name}' already has an owner")
    
    # Create new user
    user_id = f"u{uuid.uuid4().hex[:8]}"
    hashed_password = get_password_hash(user_data.password)
    
    new_user = User(
        id=user_id,
        email=user_data.email,
        hashed_password=hashed_password,
        role=user_data.role,
        name=user_data.name,
        phone=user_data.phone,
        address=user_data.address,
        restaurant_id=user_data.restaurant_id if user_data.role == UserRole.OWNER else None
    )
    
    db.add(new_user)
    
    # Create user preferences for customers
    if user_data.role == UserRole.CUSTOMER:
        preference = UserPreference(user_id=user_id)
        db.add(preference)
    
    db.commit()
    db.refresh(new_user)
    
    logger.info(f"User registered successfully: {user_data.email} as {user_data.role.value}")
    
    # Create access token
    access_token = create_access_token(data={"sub": new_user.id, "role": new_user.role.value})
    
    return Token(
        access_token=access_token,
        token_type="bearer",
        user=UserSchema.from_orm(new_user)
    )

@router.post("/login", response_model=Token)
async def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """Login with email and password"""
    logger.info(f"Login attempt for email: {credentials.email}")
    
    # Find user
    user = db.query(User).filter(User.email == credentials.email).first()
    if not user or not verify_password(credentials.password, user.hashed_password):
        logger.warning(f"Login failed - invalid credentials: {credentials.email}")
        raise UnauthorizedException("Invalid email or password")
    
    logger.info(f"User logged in successfully: {credentials.email}")
    
    # Create access token
    access_token = create_access_token(data={"sub": user.id, "role": user.role.value})
    
    return Token(
        access_token=access_token,
        token_type="bearer",
        user=UserSchema.from_orm(user)
    )

@router.post("/reset-password")
async def reset_password(reset_data: PasswordReset, db: Session = Depends(get_db)):
    """Reset password with old password verification"""
    logger.info(f"Password reset attempt for email: {reset_data.email}")
    
    # Find user
    user = db.query(User).filter(User.email == reset_data.email).first()
    if not user:
        logger.warning(f"Password reset failed - user not found: {reset_data.email}")
        raise UnauthorizedException("Invalid email")
    
    # Verify old password
    if not verify_password(reset_data.old_password, user.hashed_password):
        logger.warning(f"Password reset failed - incorrect old password: {reset_data.email}")
        raise UnauthorizedException("Incorrect old password")
    
    # Update password
    user.hashed_password = get_password_hash(reset_data.new_password)
    db.commit()
    
    logger.info(f"Password reset successful: {reset_data.email}")
    
    return {"message": "Password reset successful"}
