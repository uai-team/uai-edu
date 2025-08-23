#!/usr/bin/python
# @Author   : uai-team
# @Version  : 1.0
# @Created  : 2025/06/25
# @File     : views.py
# @desc     : 路由，视图文件

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from fastapi import APIRouter, Depends
from . import models, schemas, crud, params
from core.dependencies import IdList
from apps.vadmin.auth.utils.current import FullAdminAuth
from apps.education.course.models import UaiEduCourse
from apps.education.course.schemas import CourseSimpleOut
from apps.education.course.crud import CourseDal
from utils.response import SuccessResponse
from apps.vadmin.auth.utils.validation.auth import Auth
from core.database import db_getter


app = APIRouter()


###########################################################
#    专区信息
###########################################################
@app.get("/zone", summary="获取专区信息列表")
async def get_zone_list(p: params.ZoneParams = Depends(), db: AsyncSession = Depends(db_getter)):
    datas, count = await crud.ZoneDal(db).get_datas(**p.dict(), v_return_count=True)
    return SuccessResponse(datas, count=count)


@app.get("/zone/course", summary="获取专区信息列表")
async def get_zone_with_course(p: params.ZoneParams = Depends(), db: AsyncSession = Depends(db_getter)):
    datas, count = await crud.ZoneDal(db).get_datas(**p.dict(), v_return_count=True)
    for zone in datas:
        model = UaiEduCourse
        schema = CourseSimpleOut
        courses, count = await CourseDal(db).get_datas(
            limit=12,
            v_join=[["zones"]],
            v_where=[text(f"zone_id = {zone['id']}")],
            v_schema=schema,
            v_return_count=True)
        zone["courses"] = courses
    return SuccessResponse(datas, count=count)


@app.get("/zone/options", summary="获取专区信息选择项")
async def get_zone_options(p: params.ZoneParams = Depends(), db: AsyncSession = Depends(db_getter)):
    datas = await crud.ZoneDal(db).get_zone_options(**p.dict())
    return SuccessResponse(datas)


@app.post("/zone", summary="创建专区信息")
async def create_zone(data: schemas.Zone, auth: Auth = Depends(FullAdminAuth())):
    return SuccessResponse(await crud.ZoneDal(auth.db).create_data(data=data))


@app.delete("/zone", summary="删除专区信息", description="硬删除")
async def delete_zone_list(ids: IdList = Depends(), auth: Auth = Depends(FullAdminAuth())):
    await crud.ZoneDal(auth.db).delete_datas(ids=ids.ids, v_soft=False)
    return SuccessResponse("删除成功")


@app.put("/zone/{data_id}", summary="更新专区信息")
async def put_zone(data_id: int, data: schemas.Zone, auth: Auth = Depends(FullAdminAuth())):
    return SuccessResponse(await crud.ZoneDal(auth.db).put_data(data_id, data))


@app.get("/zone/{data_id}", summary="获取专区信息信息")
async def get_zone(data_id: int, db: AsyncSession = Depends(db_getter)):
    schema = schemas.ZoneSimpleOut
    return SuccessResponse(await crud.ZoneDal(db).get_data(data_id, v_schema=schema))
