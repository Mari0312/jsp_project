from fastapi import HTTPException, status, APIRouter, Depends

from utils import verify_password, create_access_token, create_refresh_token
from database import User, RevokedTokenModel
from deps import get_current_user, token_data
from schemas import UserAuth, UserOut, TokenSchema, UserSignup, TokenPayload

router = APIRouter(prefix='/authorization')


@router.post('/signup', summary="Create new user", response_model=UserOut)
async def create_user(data: UserSignup):
    # querying database to check if user already exist
    user = User.find_by_email(data.email)
    if user is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exist"
        )
    user = User(**dict(data)).save()
    return UserOut.from_orm(user)


@router.post('/login', summary="Create access and refresh tokens for user", response_model=TokenSchema)
async def login(form_data: UserAuth):
    user = User.find_by_email(form_data.email)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )

    hashed_pass = user.hashed_password
    if not verify_password(form_data.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )

    return {
        "access_token": create_access_token(user.email),
        "refresh_token": create_refresh_token(user.email),
    }


@router.post("/refresh")
def post(user: User = Depends(get_current_user)):
    """Method for refreshing access token. Returns new access token."""
    access_token = create_access_token(user.email, **user.additional_claims)
    return {'access_token': access_token}


@router.post("/logout-access")
def logout_access(token_data: TokenPayload = Depends(token_data)):
    try:
        RevokedTokenModel(jti=token_data.jti).save()
        return {'message': f'Access token {token_data.jti} has been revoked'}
    except Exception as e:
        return {
                   "message": "Something went wrong while revoking token",
                   "error": repr(e)
               }, 500
