#!/usr/bin/python
# @Author   : uai-team
# @Version  : 1.0
# @Created  : 2025/07/03
# @File     : views.py
# @desc     : 路由，视图文件

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from fastapi import APIRouter, Depends
from . import models, schemas, crud, params
from core.dependencies import IdList
from apps.vadmin.auth.utils.current import FullAdminAuth
from utils.response import SuccessResponse
from apps.vadmin.auth.utils.validation.auth import Auth
from apps.education.category.models import UaiEduCategory
from apps.education.category.crud import CategoryDal
from core.database import db_getter


app = APIRouter()


###########################################################
#    仿真信息
###########################################################
@app.get("/simulation", summary="获取仿真信息列表")
async def get_simulation_list(p: params.SimulationParams = Depends(), db: AsyncSession = Depends(db_getter)):
    model = models.UaiEduSimulation
    options = [joinedload(model.categories)]
    schema = schemas.SimulationOut
    datas, count = await crud.SimulationDal(db).get_datas(
        **p.dict(),
        v_options=options,
        v_schema=schema,
        v_return_count=True)
    return SuccessResponse(datas, count=count)


@app.get("/simulation/center", summary="获取仿真信息列表")
async def get_simulation_search_list(db: AsyncSession = Depends(db_getter), pageCurrent: int = 1, pageSize: int = 20, categoryId: int = None):
    categories = await CategoryDal(db).get_category_children_id(category_type="simulation", id=categoryId)
    
    model = models.UaiEduSimulation
    schema = schemas.SimulationSimpleOut
    datas, count = await crud.SimulationDal(db).get_datas(
        page=pageCurrent,
        limit=pageSize,
        v_join=[["categories"]],
        v_where=[text(f"category_id in ({','.join(map(str, categories))})")],
        v_schema=schema,
        v_distinct=True,
        v_return_count=True)
    return SuccessResponse({"list": datas, "totalCount": count, "pageCurrent": pageCurrent, "pageSize": pageSize})


@app.post("/simulation", summary="创建仿真信息")
async def create_simulation(data: schemas.SimulationIn, auth: Auth = Depends(FullAdminAuth())):
    return SuccessResponse(await crud.SimulationDal(auth.db).create_data(data=data))


@app.delete("/simulation", summary="删除仿真信息", description="硬删除")
async def delete_simulation_list(ids: IdList = Depends(), auth: Auth = Depends(FullAdminAuth())):
    await crud.SimulationDal(auth.db).delete_datas(ids=ids.ids, v_soft=False)
    return SuccessResponse("删除成功")


@app.put("/simulation/{data_id}", summary="更新仿真信息")
async def put_simulation(data_id: int, data: schemas.SimulationIn, auth: Auth = Depends(FullAdminAuth())):
    return SuccessResponse(await crud.SimulationDal(auth.db).put_data(data_id, data))


@app.get("/simulation/{data_id}", summary="获取仿真信息")
async def get_simulation(data_id: int, db: AsyncSession = Depends(db_getter)):
    model = models.UaiEduSimulation
    options = [joinedload(model.categories)]
    schema = schemas.SimulationOut
    return SuccessResponse(await crud.SimulationDal(db).get_data(data_id, v_options=options, v_schema=schema))


@app.get("/simulation/detail/{id}", summary="获取仿真信息")
async def get_simulation_detail(id: int, db: AsyncSession = Depends(db_getter)):
    model = models.UaiEduSimulation
    options = [joinedload(model.categories)]
    schema = schemas.SimulationOut
    return SuccessResponse(await crud.SimulationDal(db).get_data(id, v_options=options, v_schema=schema))
