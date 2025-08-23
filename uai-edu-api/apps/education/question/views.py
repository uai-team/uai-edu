#!/usr/bin/python
# @Author   : uai-team
# @Version  : 1.0
# @Created  : 2025/07/22
# @File     : views.py
# @desc     : 路由，视图文件

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from fastapi import APIRouter, Depends
from . import models, schemas, crud, params
from core.dependencies import IdList
from apps.vadmin.auth.utils.current import FullAdminAuth
from utils.response import SuccessResponse
from apps.vadmin.auth.utils.validation.auth import Auth
from core.database import db_getter
from apps.education.category.crud import CategoryDal
from apps.education.course.crud import LessonDal


app = APIRouter()


###########################################################
#    题目信息
###########################################################
@app.get("/question", summary="获取题目信息列表")
async def get_question_list(p: params.QuestionParams = Depends(), db: AsyncSession = Depends(db_getter)):
    if p.category_id:
        categoryids = await CategoryDal(db).get_category_children_id(category_type="course", id=p.category_id)
        queryParams = p.dict()
        del queryParams["category_id"]
        datas, count = await crud.QuestionDal(db).get_datas(**queryParams, v_return_count=True, category_id=("in", categoryids))
    else:
        datas, count = await crud.QuestionDal(db).get_datas(**p.dict(), v_return_count=True)
        categoryids = [data["category_id"] for data in datas]

    categories = await CategoryDal(db).get_datas(limit=0, v_return_count=False, id=("in",categoryids))
    
    lessonids = [data["lesson_id"] for data in datas]
    lessons = await LessonDal(db).get_datas(limit=0, v_return_count=False, id=("in",lessonids))

    for data in datas:
        for category in categories:
            if data["category_id"] == category["id"]:
                data["category_name"] = category["category_name"]
                break
        for lesson in lessons:
            if data["lesson_id"] == lesson["id"]:
                data["lesson_name"] = lesson["lesson_name"]
                break
    return SuccessResponse(datas, count=count)


@app.post("/question", summary="创建题目信息")
async def create_question(data: schemas.Question, auth: Auth = Depends(FullAdminAuth())):
    return SuccessResponse(await crud.QuestionDal(auth.db).create_data(data=data))


@app.delete("/question", summary="删除题目信息", description="硬删除")
async def delete_question_list(ids: IdList = Depends(), auth: Auth = Depends(FullAdminAuth())):
    await crud.QuestionDal(auth.db).delete_datas(ids=ids.ids, v_soft=False)
    return SuccessResponse("删除成功")


@app.put("/question/{data_id}", summary="更新题目信息")
async def put_question(data_id: int, data: schemas.Question, auth: Auth = Depends(FullAdminAuth())):
    return SuccessResponse(await crud.QuestionDal(auth.db).put_data(data_id, data))


@app.get("/question/{data_id}", summary="获取题目信息信息")
async def get_question(data_id: int, db: AsyncSession = Depends(db_getter)):
    schema = schemas.QuestionSimpleOut
    return SuccessResponse(await crud.QuestionDal(db).get_data(data_id, v_schema=schema))

