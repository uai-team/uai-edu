from datetime import timedelta
from redis.asyncio import Redis
from fastapi import APIRouter, Depends, Request, Body
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import db_getter, redis_getter
from core.exception import CustomException
from utils import status
from utils.response import SuccessResponse, ErrorResponse
from application import settings
from .login_manage import LoginManage
from .validation import LoginForm, WXLoginForm
from apps.vadmin.record.models import VadminLoginRecord
from apps.vadmin.auth.crud import MenuDal, UserDal
from apps.vadmin.auth.models import VadminUser
from .current import FullAdminAuth
from .validation.auth import Auth
from utils.wx.oauth import WXOAuth
import jwt

app = APIRouter()


@app.post("/login", summary="账号号密码登录", description="前端登录通道，限制最多输错次数，达到最大值后将is_active=False")
async def login_for_access_token(
    request: Request,
    data: LoginForm,
    manage: LoginManage = Depends(),
    db: AsyncSession = Depends(db_getter)
):
    try:
        if data.method == "0":
            result = await manage.password_login(data, db, request)
        elif data.method == "1":
            result = await manage.sms_login(data, db, request)
        else:
            raise ValueError("无效参数")

        if not result.status:
            raise ValueError(result.msg)

        access_token = LoginManage.create_token(
            {"sub": result.user.telephone, "is_refresh": False, "password": result.user.password}
        )
        expires = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
        refresh_token = LoginManage.create_token(
            payload={"sub": result.user.telephone, "is_refresh": True, "password": result.user.password},
            expires=expires
        )
        resp = {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "is_reset_password": result.user.is_reset_password,
            "is_wx_server_openid": result.user.is_wx_server_openid
        }
        await VadminLoginRecord.create_login_record(db, data, True, request, resp)
        return SuccessResponse(resp)
    except ValueError as e:
        await VadminLoginRecord.create_login_record(db, data, False, request, {"message": str(e)})
        return ErrorResponse(msg=str(e))


@app.post("/token/refresh", summary="刷新Token")
async def token_refresh(refresh: str = Body(..., title="刷新Token")):
    error_code = status.HTTP_401_UNAUTHORIZED
    try:
        payload = jwt.decode(refresh, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        telephone: str = payload.get("sub")
        is_refresh: bool = payload.get("is_refresh")
        password: str = payload.get("password")
        if not telephone or not is_refresh or not password:
            return ErrorResponse("未认证，请您重新登录", code=error_code, status=error_code)
    except jwt.exceptions.InvalidSignatureError:
        return ErrorResponse("无效认证，请您重新登录", code=error_code, status=error_code)
    except jwt.exceptions.ExpiredSignatureError:
        return ErrorResponse("登录已超时，请您重新登录", code=error_code, status=error_code)

    access_token = LoginManage.create_token({"sub": telephone, "is_refresh": False, "password": password})
    expires = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    refresh_token = LoginManage.create_token(
        payload={"sub": telephone, "is_refresh": True, "password": password},
        expires=expires
    )
    resp = {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }
    return SuccessResponse(resp)
