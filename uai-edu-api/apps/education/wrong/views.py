#!/usr/bin/python
# @Author   : uai-team
# @Version  : 1.0
# @Created  : 2025/07/29
# @File     : views.py
# @desc     : 路由，视图文件
from apps.vadmin.auth.utils.current import FullAdminAuth, AllUserAuth
from core.dependencies import IdList
from core.database import db_getter
from fastapi import APIRouter, Depends
from utils.response import SuccessResponse
from . import models, params, crud, schemas
from apps.education.category.crud import CategoryDal
from apps.education.question.schemas import QuestionSimpleOut
from apps.vadmin.auth.crud import DeptDal, UserDal
from apps.vadmin.auth.models import VadminUser
from apps.vadmin.auth.schemas import UserOut
from apps.vadmin.auth.utils.validation.auth import Auth
from apps.education.exam.crud import ExamPaperDal, ExamUserDal, ExamUserAnswerDal
from apps.education.exam.schemas import ExamPaperSimpleOut, ExamUserAnswerSimpleOut
from apps.education.question.crud import QuestionDal
from apps.education.course.crud import LessonDal, ChapterDal, CourseDal
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
import datetime


app = APIRouter()


###########################################################
#    我的错题本
###########################################################
@app.post("/wrong/auth/user/notebook/add/{data_id}", summary="添加到错题本")
async def create_notebook(data_id: int, db: AsyncSession = Depends(db_getter)):
    answer = await ExamUserAnswerDal(db).get_data(data_id)
    data = {
        "answer_id": answer.answer_id,
        "question_id": answer.question_id,
        "wrong_datetime": answer.create_datetime,
        "user_answer": answer.user_answer
    }

    return SuccessResponse(await crud.NotebookDal(db).create_data(data=data))


@app.get("/wrong/auth/user/notebook/list", summary="获取我的错题本")
async def get_notebook_search_list(auth: Auth = Depends(AllUserAuth()), pageCurrent: int = 1, pageSize: int = 20, categoryId: int = None):
    categories = await CategoryDal(auth.db).get_category_children_id(category_type="course", id=categoryId)

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

    paperes = await ExamPaperDal(auth.db).get_datas(limit=0, v_return_count=False, v_schema=ExamPaperSimpleOut, category_id=("in", categories), dept_id=("in", deptids))

    if len(paperes) == 0:
        return SuccessResponse({"list": [], "totalCount": 0, "pageCurrent": pageCurrent, "pageSize": pageSize})

    paperids = [paper["id"] for paper in paperes]
    answers = await ExamUserDal(auth.db).get_datas(
        limit=0,
        v_return_count=False,
        user_id=auth.user.id,
        paper_id=("in", paperids))

    if len(answers) == 0:
        return SuccessResponse({"list": [], "totalCount": 0, "pageCurrent": pageCurrent, "pageSize": pageSize})

    answerids = [answer["id"] for answer in answers]
    wrongs, count= await crud.NotebookDal(auth.db).get_datas(page=pageCurrent, limit=pageSize, v_return_count=True, answer_id=("in", answerids))

    if len(wrongs) == 0:
        return SuccessResponse({"list": [], "totalCount": 0, "pageCurrent": pageCurrent, "pageSize": pageSize})

    questionids = [wrong["question_id"] for wrong in wrongs]
    questions = await QuestionDal(auth.db).get_datas(limit=0, v_return_count=False, id=("in", questionids), v_schema=QuestionSimpleOut)

    lessonids = [question["lesson_id"] for question in questions]
    lessons = await LessonDal(auth.db).get_datas(limit=0, v_return_count=False, id=("in",lessonids))

    chapterids = [lesson["chapter_id"] for lesson in lessons]
    chapters = await ChapterDal(auth.db).get_datas(limit=0, v_return_count=False, id=("in", chapterids))

    courseids = [chapter["course_id"] for chapter in chapters]
    courses = await CourseDal(auth.db).get_datas(limit=0, v_return_count=False, id=("in", courseids))

    for wrong in wrongs:
        for question in questions:
            if wrong["question_id"] == question["id"]:
                wrong["question_info"] = question
                for lesson in lessons:
                    if question["lesson_id"] == lesson["id"]:
                        wrong["lesson_id"] = lesson["id"]
                        wrong["lesson_name"] = lesson["lesson_name"]
                        for chapter in chapters:
                            if lesson["chapter_id"] == chapter["id"]:
                                wrong["chapter_id"] = chapter["id"]
                                wrong["chapter_name"] = chapter["chapter_name"]
                                for course in courses:
                                    if chapter["course_id"] == course["id"]:
                                        wrong["course_id"] = course["id"]
                                        wrong["course_name"] = course["course_name"]
                                        break
                                break
                        break
                break

    return SuccessResponse({"list": wrongs, "totalCount": count, "pageCurrent": pageCurrent, "pageSize": pageSize})


@app.post("/wrong/auth/user/notebook/remove/{data_id}", summary="从错题本移除")
async def remove_notebook(data_id: int, db: AsyncSession = Depends(db_getter)):
    await crud.NotebookDal(db).delete_datas(ids=[data_id], v_soft=True)
    return SuccessResponse("删除成功")


async def user_all_wrong_notebook(auth: Auth = Depends(AllUserAuth())):
    answers = await ExamUserDal(auth.db).get_datas(
        limit=0,
        v_return_count=False,
        user_id=auth.user.id
    )

    answerids = [answer["id"] for answer in answers]
    wrongs = await crud.NotebookDal(auth.db).get_datas(limit=0, v_return_count=False, answer_id=("in", answerids))

    return wrongs


async def get_problems_to_review(wrongs, review_intervals):
    problems_to_review = []
    today = datetime.datetime.now()

    for wrong in wrongs:
        base_time = datetime.datetime.strptime(wrong["last_review_time"] if wrong["last_review_time"] else wrong["wrong_datetime"], "%Y-%m-%d %H:%M:%S")
        days_since_base = (today - base_time).days

        if wrong["review_count"] >= len(review_intervals):
            interval_days = review_intervals[-1]
        else:
            interval_days = review_intervals[wrong["review_count"]]

        next_review_date = base_time + datetime.timedelta(days=interval_days)

        if next_review_date.date() <= today.date():
            problems_to_review.append((wrong, next_review_date))

    problems_to_review.sort(key=lambda x: x[1])
    return problems_to_review


@app.get("/wrong/auth/user/notebook/ebbinghaus/schedule", summary="艾宾浩斯遗忘曲线复习计划")
async def get_ebbinghaus_search_list(auth: Auth = Depends(AllUserAuth()), pageCurrent: int = 1, pageSize: int = 20):
    review_intervals = [1, 2, 4, 7, 15, 30, 60]
    today = datetime.datetime.now()

    all_wrongs = await user_all_wrong_notebook(auth)
    total_problems = len(all_wrongs)
    problems_to_review = await get_problems_to_review(all_wrongs, review_intervals)
    total_problems_to_review = len(problems_to_review)

    review_stages = {}
    for wrong in all_wrongs:
        stage = min(wrong["review_count"], len(review_intervals) - 1)
        stage_date = (today + datetime.timedelta(days=stage+1)).strftime("%Y-%m-%d")
        review_stages[stage_date] = review_stages.get(stage_date, 0) + 1

    wrongids = [wrong[0]["id"] for wrong in problems_to_review]
    problems, count = await crud.NotebookDal(auth.db).get_datas(page=pageCurrent, limit=pageSize, v_return_count=True, id=("in", wrongids), v_schema=schemas.NotebookSimpleOut)

    questionids = [wrong["question_id"] for wrong in problems]
    questions = await QuestionDal(auth.db).get_datas(limit=0, v_return_count=False, id=("in", questionids), v_schema=QuestionSimpleOut)

    today_to_review = []
    for problem in problems:
        for question in questions:
            if problem["question_id"] == question["id"]:
                problem["question_info"] = question
                today_to_review.append(problem)
                break

    data = {
        "total_problems": total_problems,
        "problems_to_review": total_problems_to_review,
        "review_rate": f"{((total_problems - total_problems_to_review) / total_problems * 100):.1f}%",
        "review_stages": review_stages,
        "today_to_review": today_to_review
    }
    return SuccessResponse({"list": [data], "totalCount": count, "pageCurrent": pageCurrent, "pageSize": pageSize})


@app.post("/wrong/auth/user/notebook/ebbinghaus/submit/{data_id}", summary="提交复习计划")
async def submit_ebbinghaus(data_id: int, db: AsyncSession = Depends(db_getter)):
    data = await crud.NotebookDal(db).get_data(data_id, v_schema=schemas.NotebookSimpleOut)
    data["review_count"] += 1
    data["last_review_time"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return SuccessResponse(await crud.NotebookDal(db).put_data(data_id, data))