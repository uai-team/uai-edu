#!/usr/bin/python
# @Author   : uai-team
# @Version  : 1.0
# @Created  : 2025/07/07
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
#    教材信息
###########################################################
@app.get("/book", summary="获取教材信息列表")
async def get_book_list(p: params.BookParams = Depends(), db: AsyncSession = Depends(db_getter)):
    model = models.UaiEduBook
    options = [joinedload(model.categories)]
    schema = schemas.BookOut
    datas, count = await crud.BookDal(db).get_datas(
        **p.dict(),
        v_options=options,
        v_schema=schema,
        v_return_count=True)
    return SuccessResponse(datas, count=count)


@app.get("/book/center", summary="获取教材信息列表")
async def get_book_search_list(db: AsyncSession = Depends(db_getter), pageCurrent: int = 1, pageSize: int = 20, categoryId: int = None):
    categories = await CategoryDal(db).get_category_children_id(category_type="book", id=categoryId)
    
    model = models.UaiEduBook
    schema = schemas.BookSimpleOut
    datas, count = await crud.BookDal(db).get_datas(
        page=pageCurrent,
        limit=pageSize,
        v_join=[["categories"]],
        v_where=[text(f"category_id in ({','.join(map(str, categories))})")],
        v_schema=schema,
        v_distinct=True,
        v_return_count=True)
    return SuccessResponse({"list": datas, "totalCount": count, "pageCurrent": pageCurrent, "pageSize": pageSize})


@app.post("/book", summary="创建教材信息")
async def create_book(data: schemas.BookIn, auth: Auth = Depends(FullAdminAuth())):
    return SuccessResponse(await crud.BookDal(auth.db).create_data(data=data))


@app.delete("/book", summary="删除教材信息", description="硬删除")
async def delete_book_list(ids: IdList = Depends(), auth: Auth = Depends(FullAdminAuth())):
    await crud.BookDal(auth.db).delete_datas(ids=ids.ids, v_soft=False)
    return SuccessResponse("删除成功")


@app.put("/book/{data_id}", summary="更新教材信息")
async def put_book(data_id: int, data: schemas.BookIn, auth: Auth = Depends(FullAdminAuth())):
    return SuccessResponse(await crud.BookDal(auth.db).put_data(data_id, data))


@app.get("/book/{data_id}", summary="获取教材信息信息")
async def get_book(data_id: int, db: AsyncSession = Depends(db_getter)):
    model = models.UaiEduBook
    options = [joinedload(model.categories)]
    schema = schemas.BookOut
    return SuccessResponse(await crud.BookDal(db).get_data(data_id, v_options=options, v_schema=schema))


@app.get("/book/detail/{id}", summary="获取教材信息")
async def get_book_detail(id: int, db: AsyncSession = Depends(db_getter)):
    model = models.UaiEduBook
    options = [joinedload(model.categories)]
    schema = schemas.BookOut
    return SuccessResponse(await crud.BookDal(db).get_data(id, v_options=options, v_schema=schema))
