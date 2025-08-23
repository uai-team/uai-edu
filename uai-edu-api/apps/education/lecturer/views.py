#!/usr/bin/python
# @Author   : uai-team
# @Version  : 1.0
# @Created  : 2025/06/28
# @File     : views.py
# @desc     : 路由，视图文件

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends
from . import models, schemas, crud, params
from core.dependencies import IdList
from apps.vadmin.auth.utils.current import FullAdminAuth
from utils.response import SuccessResponse
from apps.vadmin.auth.utils.validation.auth import Auth
from core.database import db_getter


app = APIRouter()


###########################################################
#    教师信息
###########################################################
@app.get("/lecturer", summary="获取教师信息列表")
async def get_lecturer_list(p: params.LecturerParams = Depends(), db: AsyncSession = Depends(db_getter)):
    datas, count = await crud.LecturerDal(db).get_datas(**p.dict(), v_return_count=True)
    return SuccessResponse(datas, count=count)


@app.post("/lecturer", summary="创建教师信息")
async def create_lecturer(data: schemas.Lecturer, auth: Auth = Depends(FullAdminAuth())):
    return SuccessResponse(await crud.LecturerDal(auth.db).create_data(data=data))


@app.delete("/lecturer", summary="删除教师信息", description="硬删除")
async def delete_lecturer_list(ids: IdList = Depends(), auth: Auth = Depends(FullAdminAuth())):
    await crud.LecturerDal(auth.db).delete_datas(ids=ids.ids, v_soft=False)
    return SuccessResponse("删除成功")


@app.put("/lecturer/{data_id}", summary="更新教师信息")
async def put_lecturer(data_id: int, data: schemas.Lecturer, auth: Auth = Depends(FullAdminAuth())):
    return SuccessResponse(await crud.LecturerDal(auth.db).put_data(data_id, data))


@app.get("/lecturer/{data_id}", summary="获取教师信息信息")
async def get_lecturer(data_id: int, db: AsyncSession = Depends(db_getter)):
    schema = schemas.LecturerSimpleOut
    return SuccessResponse(await crud.LecturerDal(db).get_data(data_id, v_schema=schema))

