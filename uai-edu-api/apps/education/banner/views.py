#!/usr/bin/python
# @Author   : uai-team
# @Version  : 1.0
# @Created  : 2025/06/24
# @File     : views.py
# @desc     : 路由，视图文件

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends
from . import models, schemas, crud, params
from core.dependencies import IdList
from apps.vadmin.auth.utils.current import AllUserAuth, OpenAuth
from utils.response import SuccessResponse
from apps.vadmin.auth.utils.validation.auth import Auth
from core.database import db_getter


app = APIRouter()


###########################################################
#    轮播图
###########################################################
@app.get("/carousel", summary="获取轮播图列表")
async def get_carousel_list(p: params.CarouselParams = Depends(), auth: Auth = Depends(OpenAuth())):
    datas, count = await crud.CarouselDal(auth.db).get_datas(**p.dict(), v_return_count=True)
    return SuccessResponse(datas, count=count)


@app.post("/carousel", summary="创建轮播图")
async def create_carousel(data: schemas.Carousel, auth: Auth = Depends(AllUserAuth())):
    data.create_user_id = auth.user.id
    return SuccessResponse(await crud.CarouselDal(auth.db).create_data(data=data))


@app.delete("/carousel", summary="删除轮播图", description="硬删除")
async def delete_carousel_list(ids: IdList = Depends(), auth: Auth = Depends(AllUserAuth())):
    await crud.CarouselDal(auth.db).delete_datas(ids=ids.ids, v_soft=False)
    return SuccessResponse("删除成功")


@app.put("/carousel/{data_id}", summary="更新轮播图")
async def put_carousel(data_id: int, data: schemas.Carousel, auth: Auth = Depends(AllUserAuth())):
    return SuccessResponse(await crud.CarouselDal(auth.db).put_data(data_id, data))


@app.get("/carousel/{data_id}", summary="获取轮播图信息")
async def get_carousel(data_id: int, db: AsyncSession = Depends(db_getter)):
    schema = schemas.CarouselSimpleOut
    return SuccessResponse(await crud.CarouselDal(db).get_data(data_id, v_schema=schema))

