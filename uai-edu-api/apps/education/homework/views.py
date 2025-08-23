#!/usr/bin/python
# @Author   : uai-team
# @Version  : 1.0
# @Created  : 2025/07/30
# @File     : views.py
# @desc     : 路由，视图文件
from utils.response import SuccessResponse
from fastapi import APIRouter, Depends
from apps.vadmin.auth.utils.current import FullAdminAuth, AllUserAuth
from . import crud, models, params, schemas
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import db_getter
from core.dependencies import IdList
from sqlalchemy.orm import joinedload
from apps.vadmin.auth.utils.validation.auth import Auth
from apps.education.category.crud import CategoryDal
from apps.education.course.crud import LessonDal, ChapterDal, CourseDal
from apps.education.book.crud import BookDal
from apps.education.exam.crud import ExamPaperDal
from apps.vadmin.auth.crud import DeptDal, UserDal
from apps.vadmin.auth.models import VadminUser
from apps.vadmin.auth.schemas import UserOut



app = APIRouter()


###########################################################
#    作业管理
###########################################################
@app.get("/homework", summary="获取作业管理列表")
async def get_homework_list(p: params.HomeworkParams = Depends(), db: AsyncSession = Depends(db_getter)):
    if p.category_id:
        categoryids = await CategoryDal(db).get_category_children_id(category_type="course", id=p.category_id)
        queryParams = p.dict()
        del queryParams["category_id"]
        datas, count = await crud.HomeworkDal(db).get_datas(**queryParams, v_return_count=True, category_id=("in", categoryids))
    else:
        datas, count = await crud.HomeworkDal(db).get_datas(**p.dict(), v_return_count=True)
        categoryids = [data["category_id"] for data in datas]

    categories = await CategoryDal(db).get_datas(limit=0, v_return_count=False, id=("in",categoryids))
    deptids = [data["dept_id"] for data in datas]
    depts = await DeptDal(db).get_datas(limit=0, v_return_count=False, id=("in",deptids))

    for data in datas:
        for category in categories:
            if data["category_id"] == category["id"]:
                data["category_name"] = category["category_name"]
                break
        for dept in depts:
            if data["dept_id"] == dept["id"]:
                data["dept_name"] = dept["name"]
                break

    return SuccessResponse(datas, count=count)


@app.post("/homework", summary="创建作业管理")
async def create_homework(data: schemas.HomeworkIn, auth: Auth = Depends(FullAdminAuth())):
    homework = await crud.HomeworkDal(auth.db).create_data(data={"category_id":data.category_id, "dept_id":data.dept_id, "homework_name": data.homework_name, "others": data.others})

    for item in data.items:
        item.homework_id = homework["id"]
        await crud.HomeworkItemDal(auth.db).create_data(data=item)

    return SuccessResponse()


@app.delete("/homework", summary="删除作业管理", description="硬删除")
async def delete_homework_list(ids: IdList = Depends(), auth: Auth = Depends(FullAdminAuth())):
    await crud.HomeworkDal(auth.db).delete_datas(ids=ids.ids, v_soft=False)
    return SuccessResponse("删除成功")


@app.put("/homework/{data_id}", summary="更新作业管理")
async def put_homework(data_id: int, data: schemas.Homework, auth: Auth = Depends(FullAdminAuth())):
    return SuccessResponse(await crud.HomeworkDal(auth.db).put_data(data_id, data))


@app.get("/homework/{data_id}", summary="获取作业管理信息")
async def get_homework(data_id: int, db: AsyncSession = Depends(db_getter)):
    schema = schemas.HomeworkSimpleOut
    homework = await crud.HomeworkDal(db).get_data(data_id, v_schema=schema)
    homeworkid = homework["id"]

    homeworkitems = await crud.HomeworkItemDal(db).get_datas(limit=0, v_return_count=False, homework_id=homeworkid)
    for item in homeworkitems:
        if item["item_type"] == "course":
            lesson = await LessonDal(db).get_data(item["resource_id"])
            chapter = await ChapterDal(db).get_data(lesson.chapter_id)
            course = await CourseDal(db).get_data(chapter.course_id)
            item["resource_name"] = lesson.lesson_name
            item["course_id"] = course.id
        elif item["item_type"] == "book":
            book = await BookDal(db).get_data(item["resource_id"])
            item["resource_name"] = book.book_name
        elif item["item_type"] == "exam":
            paper = await ExamPaperDal(db).get_data(item["resource_id"])
            item["resource_name"] = paper.paper_name
    
    homework["items"] = homeworkitems

    return SuccessResponse(homework)


@app.get("/homework/auth/user/center", summary="获取家庭作业列表")
async def get_user_homework_list(auth: Auth = Depends(AllUserAuth()), pageCurrent: int = 1, pageSize: int = 20):
    model = VadminUser
    options = [joinedload(model.roles), joinedload(model.depts)]
    schema = UserOut
    user = await UserDal(auth.db).get_data(auth.user.id, v_options=options, v_schema=schema)
    user_dept_ids = [dept["id"] for dept in user["depts"]]
    deptids = [id for id in user_dept_ids]
    for id in user_dept_ids:
        depts = await DeptDal(auth.db).get_dept_parent_id(id)
        for dept in depts:
            if dept not in deptids:
                deptids.append(dept)

    datas, count = await crud.HomeworkDal(auth.db).get_datas(
        page=pageCurrent,
        limit=pageSize,
        v_return_count=True,
        dept_id=("in", deptids))

    categoryids = [data["category_id"] for data in datas]
    categories = await CategoryDal(auth.db).get_datas(limit=0, v_return_count=False, id=("in",categoryids))
    depts = await DeptDal(auth.db).get_datas(limit=0, v_return_count=False, id=("in",deptids))

    for data in datas:
        for category in categories:
            if data["category_id"] == category["id"]:
                data["category_name"] = category["category_name"]
                break
        for dept in depts:
            if data["dept_id"] == dept["id"]:
                data["dept_name"] = dept["name"]
                break

    return SuccessResponse({"list": datas, "totalCount": count, "pageCurrent": pageCurrent, "pageSize": pageSize})




###########################################################
#    作业管理
###########################################################
@app.get("/homeworkitem", summary="获取作业管理列表")
async def get_homeworkitem_list(p: params.HomeworkItemParams = Depends(), db: AsyncSession = Depends(db_getter)):
    datas, count = await crud.HomeworkItemDal(db).get_datas(**p.dict(), v_return_count=True)
    return SuccessResponse(datas, count=count)


@app.post("/homeworkitem", summary="创建作业管理")
async def create_homeworkitem(data: schemas.HomeworkItem, auth: Auth = Depends(FullAdminAuth())):
    return SuccessResponse(await crud.HomeworkItemDal(auth.db).create_data(data=data))


@app.delete("/homeworkitem", summary="删除作业管理", description="硬删除")
async def delete_homeworkitem_list(ids: IdList = Depends(), auth: Auth = Depends(FullAdminAuth())):
    await crud.HomeworkItemDal(auth.db).delete_datas(ids=ids.ids, v_soft=False)
    return SuccessResponse("删除成功")


@app.put("/homeworkitem/{data_id}", summary="更新作业管理")
async def put_homeworkitem(data_id: int, data: schemas.HomeworkItem, auth: Auth = Depends(FullAdminAuth())):
    return SuccessResponse(await crud.HomeworkItemDal(auth.db).put_data(data_id, data))


@app.get("/homeworkitem/{data_id}", summary="获取作业管理信息")
async def get_homeworkitem(data_id: int, db: AsyncSession = Depends(db_getter)):
    schema = schemas.HomeworkItemSimpleOut
    return SuccessResponse(await crud.HomeworkItemDal(db).get_data(data_id, v_schema=schema))

