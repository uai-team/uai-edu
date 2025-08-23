#!/usr/bin/python
# @Author   : uai-team
# @Version  : 1.0
# @Created  : 2025/06/25
# @File     : views.py
# @desc     : 路由，视图文件

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends
from . import models, schemas, crud, params
from core.dependencies import IdList
from apps.vadmin.auth.utils.current import AllUserAuth, FullAdminAuth, OpenAuth
from utils.response import SuccessResponse
from apps.vadmin.auth.utils.validation.auth import Auth
from core.database import db_getter


app = APIRouter()


###########################################################
#    类目信息
###########################################################
@app.get("/category", summary="获取类目树列表")
async def get_category_list(params: params.CategoryParams = Depends(), db: AsyncSession = Depends(db_getter)):
    datas = await crud.CategoryDal(db).get_tree_list(1, **params.dict())
    return SuccessResponse(datas)


@app.get("/category/options", summary="获取类目树选择项，添加/修改类目时使用")
async def get_category_options(params: params.CategoryParams = Depends(), db: AsyncSession = Depends(db_getter)):
    datas = await crud.CategoryDal(db).get_tree_list(mode=2, **params.dict())
    return SuccessResponse(datas)


@app.post("/category", summary="创建类目信息")
async def create_category(data: schemas.Category, auth: Auth = Depends(FullAdminAuth())):
    return SuccessResponse(await crud.CategoryDal(auth.db).create_data(data=data))


@app.delete("/category", summary="删除类目信息", description="硬删除")
async def delete_category_list(ids: IdList = Depends(), auth: Auth = Depends(FullAdminAuth())):
    await crud.CategoryDal(auth.db).delete_datas(ids=ids.ids, v_soft=False)
    return SuccessResponse("删除成功")


@app.put("/category/{data_id}", summary="更新类目信息")
async def put_category(data_id: int, data: schemas.Category, auth: Auth = Depends(FullAdminAuth())):
    return SuccessResponse(await crud.CategoryDal(auth.db).put_data(data_id, data))


@app.get("/category/{data_id}", summary="获取类目信息信息")
async def get_category(data_id: int, db: AsyncSession = Depends(db_getter)):
    schema = schemas.CategorySimpleOut
    return SuccessResponse(await crud.CategoryDal(db).get_data(data_id, v_schema=schema))

