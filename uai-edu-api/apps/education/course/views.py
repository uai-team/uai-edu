#!/usr/bin/python
# @Author   : uai-team
# @Version  : 1.0
# @Created  : 2025/06/28
# @File     : views.py
# @desc     : 路由，视图文件
from core.database import db_getter
from apps.education.category.models import UaiEduCategory
from sqlalchemy.ext.asyncio import AsyncSession
from . import schemas, models, crud, params
from apps.vadmin.auth.utils.validation.auth import Auth
from apps.vadmin.auth.crud import UserDal
from apps.vadmin.auth.models import VadminUser
from apps.vadmin.auth.schemas import UserRoleOut
from fastapi import APIRouter, Depends
from sqlalchemy.orm import joinedload
from core.dependencies import IdList
from sqlalchemy import text
from utils.response import SuccessResponse
from apps.education.category.crud import CategoryDal
from apps.vadmin.auth.utils.current import FullAdminAuth


app = APIRouter()


###########################################################
#    课程信息
###########################################################
@app.get("/course", summary="获取课程信息列表")
async def get_course_list(p: params.CourseParams = Depends(), db: AsyncSession = Depends(db_getter)):
    model = models.UaiEduCourse
    options = [joinedload(model.categories), joinedload(model.zones)]
    schema = schemas.CourseOut
    if p.category_id:
        categoryids = await CategoryDal(db).get_category_children_id(category_type="course", id=p.category_id)
        queryParams = p.dict()
        del queryParams["category_id"]
        datas, count = await crud.CourseDal(db).get_datas(**queryParams, v_options=options, v_schema=schema, v_return_count=True, v_join=[["categories"]], v_where=[text(f"category_id in ({','.join(map(str, categoryids))})")], v_distinct=True)
    else:
        datas, count = await crud.CourseDal(db).get_datas(**p.dict(), v_options=options, v_schema=schema, v_return_count=True)
    return SuccessResponse(datas, count=count)


@app.get("/course/center", summary="获取课程信息列表")
async def get_course_search_list(db: AsyncSession = Depends(db_getter), pageCurrent: int = 1, pageSize: int = 20, categoryId: int = None):
    categories = await CategoryDal(db).get_category_children_id(category_type="course", id=categoryId)
    
    model = models.UaiEduCourse
    schema = schemas.CourseSimpleOut
    datas, count = await crud.CourseDal(db).get_datas(
        page=pageCurrent,
        limit=pageSize,
        v_join=[["categories"]],
        v_where=[text(f"category_id in ({','.join(map(str, categories))})")],
        v_schema=schema,
        v_distinct=True,
        v_return_count=True)
    return SuccessResponse({"list": datas, "totalCount": count, "pageCurrent": pageCurrent, "pageSize": pageSize})


@app.post("/course", summary="创建课程信息")
async def create_course(data: schemas.CourseIn, auth: Auth = Depends(FullAdminAuth())):
    return SuccessResponse(await crud.CourseDal(auth.db).create_data(data=data))


@app.delete("/course", summary="删除课程信息", description="硬删除")
async def delete_course_list(ids: IdList = Depends(), auth: Auth = Depends(FullAdminAuth())):
    await crud.CourseDal(auth.db).delete_datas(ids=ids.ids, v_soft=False)
    return SuccessResponse("删除成功")


@app.put("/course/{data_id}", summary="更新课程信息")
async def put_course(data_id: int, data: schemas.CourseIn, auth: Auth = Depends(FullAdminAuth())):
    return SuccessResponse(await crud.CourseDal(auth.db).put_data(data_id, data))


@app.get("/course/{data_id}", summary="获取课程信息")
async def get_course(data_id: int, db: AsyncSession = Depends(db_getter)):
    model = models.UaiEduCourse
    options = [joinedload(model.categories), joinedload(model.zones)]
    schema = schemas.CourseOut
    return SuccessResponse(await crud.CourseDal(db).get_data(data_id, v_options=options, v_schema=schema))


@app.get("/course/detail/{id}", summary="获取课程信息")
async def get_course_detail(id: int, db: AsyncSession = Depends(db_getter)):
    model = models.UaiEduCourse
    options = [joinedload(model.categories), joinedload(model.zones)]
    schema = schemas.CourseOut
    course = await crud.CourseDal(db).get_data(id, v_options=options, v_schema=schema)

    chapterRespList = await crud.ChapterDal(db).get_datas(limit=0, v_return_count=False, course_id=id)

    for chapter in chapterRespList:
        chapter["lessonRespList"] = await crud.LessonDal(db).get_datas(limit=0, v_return_count=False, chapter_id=chapter["id"])

    course["chapterRespList"] = chapterRespList
    return SuccessResponse(course)


@app.get("/course/name/detail", summary="获取课程信息列表")
async def get_course_list(p: params.CourseParams = Depends(), db: AsyncSession = Depends(db_getter)):
    datas, count = await crud.CourseDal(db).get_datas(**p.dict(), v_return_count=True)
    if count > 0:
        id = datas[0]["id"]
        model = models.UaiEduCourse
        options = [joinedload(model.categories), joinedload(model.zones)]
        schema = schemas.CourseOut
        course = await crud.CourseDal(db).get_data(id, v_options=options, v_schema=schema)

        chapterRespList = await crud.ChapterDal(db).get_datas(limit=0, v_return_count=False, course_id=id)

        for chapter in chapterRespList:
            chapter["lessonRespList"] = await crud.LessonDal(db).get_datas(limit=0, v_return_count=False, chapter_id=chapter["id"])

        course["chapterRespList"] = chapterRespList
        return SuccessResponse(course)
    
    return SuccessResponse(datas, count=count)


###########################################################
#    章节信息
###########################################################
@app.get("/chapter", summary="获取章节信息列表")
async def get_chapter_list(p: params.ChapterParams = Depends(), db: AsyncSession = Depends(db_getter)):
    datas, count = await crud.ChapterDal(db).get_datas(**p.dict(), v_return_count=True)
    return SuccessResponse(datas, count=count)


@app.post("/chapter", summary="创建章节信息")
async def create_chapter(data: schemas.Chapter, auth: Auth = Depends(FullAdminAuth())):
    return SuccessResponse(await crud.ChapterDal(auth.db).create_data(data=data))


@app.delete("/chapter", summary="删除章节信息", description="硬删除")
async def delete_chapter_list(ids: IdList = Depends(), auth: Auth = Depends(FullAdminAuth())):
    await crud.ChapterDal(auth.db).delete_datas(ids=ids.ids, v_soft=False)
    return SuccessResponse("删除成功")


@app.put("/chapter/{data_id}", summary="更新章节信息")
async def put_chapter(data_id: int, data: schemas.Chapter, auth: Auth = Depends(FullAdminAuth())):
    return SuccessResponse(await crud.ChapterDal(auth.db).put_data(data_id, data))


@app.get("/chapter/{data_id}", summary="获取章节信息信息")
async def get_chapter(data_id: int, db: AsyncSession = Depends(db_getter)):
    schema = schemas.ChapterSimpleOut
    return SuccessResponse(await crud.ChapterDal(db).get_data(data_id, v_schema=schema))


###########################################################
#    课时信息
###########################################################
@app.get("/lesson", summary="获取课时信息列表")
async def get_lesson_list(p: params.LessonParams = Depends(), db: AsyncSession = Depends(db_getter)):
    datas, count = await crud.LessonDal(db).get_datas(**p.dict(), v_return_count=True)
    return SuccessResponse(datas, count=count)


@app.post("/lesson", summary="创建课时信息")
async def create_lesson(data: schemas.Lesson, auth: Auth = Depends(FullAdminAuth())):
    return SuccessResponse(await crud.LessonDal(auth.db).create_data(data=data))


@app.delete("/lesson", summary="删除课时信息", description="硬删除")
async def delete_lesson_list(ids: IdList = Depends(), auth: Auth = Depends(FullAdminAuth())):
    await crud.LessonDal(auth.db).delete_datas(ids=ids.ids, v_soft=False)
    return SuccessResponse("删除成功")


@app.put("/lesson/{data_id}", summary="更新课时信息")
async def put_lesson(data_id: int, data: schemas.Lesson, auth: Auth = Depends(FullAdminAuth())):
    return SuccessResponse(await crud.LessonDal(auth.db).put_data(data_id, data))


@app.get("/lesson/{data_id}", summary="获取课时信息信息")
async def get_lesson(data_id: int, db: AsyncSession = Depends(db_getter)):
    schema = schemas.LessonSimpleOut
    return SuccessResponse(await crud.LessonDal(db).get_data(data_id, v_schema=schema))


@app.post("/lesson/auth/study", summary="学习课程")
async def study_lesson(data: schemas.StudyLesson, auth: Auth = Depends(FullAdminAuth())):
    schema = schemas.LessonSimpleOut
    return SuccessResponse(await crud.LessonDal(auth.db).get_data(data.lesson_id, v_schema=schema))


@app.post("/lesson/auth/study/progress", summary="课程学习进度")
async def study_lesson_progress(data: schemas.StudyLessonProgress, auth: Auth = Depends(FullAdminAuth())):
    datas = await crud.LessonProgressDal(auth.db).get_datas(limit=1, v_return_count=False, course_id=data.course_id, chapter_id=data.chapter_id, lesson_id=data.lesson_id, user_id=data.user_id)
    if datas:
        return SuccessResponse(await crud.LessonProgressDal(auth.db).put_data(datas[0]["id"], data))
    else:
        return SuccessResponse(await crud.LessonProgressDal(auth.db).create_data(data=data))


@app.get("/lesson/by/category/{categoryId}", summary="根据类目获取所有课程")
async def get_lesson_by_category(categoryId: int, db: AsyncSession = Depends(db_getter)):
    categories = await CategoryDal(db).get_category_children_id(category_type="course", id=categoryId)

    model = models.UaiEduCourse
    schema = schemas.CourseSimpleOut
    courses = await crud.CourseDal(db).get_datas(
        limit=0,
        v_join=[["categories"]],
        v_where=[text(f"category_id in ({','.join(map(str, categories))})")],
        v_schema=schema,
        v_distinct=True,
        v_return_count=False)
    courseids = [course["id"] for course in courses]

    if courseids:
        chapters = await crud.ChapterDal(db).get_datas(limit=0, v_return_count=False, course_id=("in",courseids))
        chapterids = [chapter["id"] for chapter in chapters]

        if chapterids:
            lessons = await crud.LessonDal(db).get_datas(limit=0, v_return_count=False, chapter_id=("in", chapterids))

            return SuccessResponse(lessons)

    return SuccessResponse([])



###########################################################
#    课时进度信息
###########################################################
@app.get("/progress/lesson", summary="获取课时进度列表")
async def get_lesson_progress_list(p: params.LessonProgressParams = Depends(), auth: Auth = Depends(FullAdminAuth())):
    model = VadminUser
    options = [joinedload(model.roles)]
    schema = UserRoleOut
    users, count = await UserDal(auth.db).get_datas(
        page=p.page,
        limit=p.limit,
        v_join=[["roles"]],
        v_where=[text("role_key = 'student'")],
        v_options=options,
        v_schema=schema,
        v_return_count=True,
        # role_key="student"
    )
    ids = [user["id"] for user in users]
    total_duration = 0
    if p.course_id:
        chapters = await crud.ChapterDal(auth.db).get_datas(limit=0, v_return_count=False, course_id=p.course_id)
        chapterids = [chapter["id"] for chapter in chapters]
        lessons = await crud.LessonDal(auth.db).get_datas(limit=0, v_return_count=False, chapter_id=("in", chapterids))
        for lesson in lessons:
            if lesson["total_duration"]:
                total_duration += lesson["total_duration"]

        datas = await crud.LessonProgressDal(auth.db).get_datas(limit=0, v_return_count=False, course_id=p.course_id, user_id=("in", ids))
    elif p.chapter_id:
        lessons = await crud.LessonDal(auth.db).get_datas(limit=0, v_return_count=False, chapter_id=p.chapter_id)
        for lesson in lessons:
            if lesson["total_duration"]:
                total_duration += lesson["total_duration"]

        datas = await crud.LessonProgressDal(auth.db).get_datas(limit=0, v_return_count=False, chapter_id=p.chapter_id, user_id=("in", ids))
    elif p.lesson_id:
        lessons = await crud.LessonDal(auth.db).get_datas(limit=0, v_return_count=False, id=p.lesson_id)
        for lesson in lessons:
            if lesson["total_duration"]:
                total_duration += lesson["total_duration"]

        datas = await crud.LessonProgressDal(auth.db).get_datas(limit=0, v_return_count=False, lesson_id=p.lesson_id, user_id=("in",ids))

    results = []
    if p.course_id or p.chapter_id or p.lesson_id:
        for user in users:
            result = {"user_id": user["id"], "user_name": user["name"], "current_duration": 0, "total_duration": total_duration}
            for data in datas:
                if data["user_id"] == user["id"]:
                    result["current_duration"] += data["current_duration"]
            results.append(result)
    return SuccessResponse(results, count=count)

    # datas, count = await crud.LessonProgressDal(auth.db).get_datas(**p.dict(), v_return_count=True, id=p.lesson_id)
    # return SuccessResponse(datas, count=count)
