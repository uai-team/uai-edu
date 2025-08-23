#!/usr/bin/python
# @Author   : uai-team
# @Version  : 1.0
# @Created  : 2025/07/24
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
from apps.education.question.crud import QuestionDal
from apps.education.course.crud import LessonDal, ChapterDal, CourseDal
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload



app = APIRouter()


###########################################################
#    考试试卷
###########################################################
@app.get("/paper", summary="获取考试试卷列表")
async def get_paper_list(p: params.ExamPaperParams = Depends(), db: AsyncSession = Depends(db_getter)):
    if p.category_id:
        categoryids = await CategoryDal(db).get_category_children_id(category_type="course", id=p.category_id)
        queryParams = p.dict()
        del queryParams["category_id"]
        datas, count = await crud.ExamPaperDal(db).get_datas(**queryParams, v_return_count=True, category_id=("in", categoryids))
    else:
        datas, count = await crud.ExamPaperDal(db).get_datas(**p.dict(), v_return_count=True)
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


@app.post("/paper", summary="创建考试试卷")
async def create_paper(data: schemas.ExamPaper, auth: Auth = Depends(FullAdminAuth())):
    data.paper_score = sum([sum([question.score for question in title.question_items]) for title in data.title_items])
    paper = await crud.ExamPaperDal(auth.db).create_data(data=data.model_dump(exclude={"title_items"}))
    paper_id = paper["id"]
    for title_order, title_item in enumerate(data.title_items):
        title_item.paper_id = paper_id
        title_item.order = title_order + 1
        title = await crud.PaperTitleDal(auth.db).create_data(data=title_item.model_dump(exclude={"question_items"}))
        title_id = title["id"]
        for question_order, question_item in enumerate(title_item.question_items):
            question_item.title_id = title_id
            question_item.order = question_order + 1
            question_item.question_id = question_item.id
            await crud.TitleQuestionDal(auth.db).create_data(data=question_item.model_dump(exclude={"id", "user_answer", "question_info"}))

    return SuccessResponse(paper)


@app.delete("/paper", summary="删除考试试卷", description="硬删除")
async def delete_paper_list(ids: IdList = Depends(), auth: Auth = Depends(FullAdminAuth())):
    await crud.ExamPaperDal(auth.db).delete_datas(ids=ids.ids, v_soft=True)
    return SuccessResponse("删除成功")


@app.put("/paper/{data_id}", summary="更新考试试卷")
async def put_paper(data_id: int, data: schemas.ExamPaper, auth: Auth = Depends(FullAdminAuth())):
    return SuccessResponse(await crud.ExamPaperDal(auth.db).put_data(data_id, data))


@app.get("/paper/{data_id}", summary="获取考试试卷信息")
async def get_paper(data_id: int, db: AsyncSession = Depends(db_getter)):
    schema = schemas.ExamPaperSimpleOut
    paper = await crud.ExamPaperDal(db).get_data(data_id, v_schema=schema)
    titles = await crud.PaperTitleDal(db).get_datas(limit=0, v_return_count=False, v_order_field="order", paper_id=data_id)
    titleids = [title["id"] for title in titles]

    for title in titles:
        questions = await crud.TitleQuestionDal(db).get_datas(limit=0, v_return_count=False, v_order_field="order", title_id=title["id"])
        for question in questions:
            question["question_info"] = await QuestionDal(db).get_data(question["question_id"], v_schema=QuestionSimpleOut)
        title["question_items"] = questions

    paper["title_items"] = titles

    return SuccessResponse(paper)


@app.get("/paper/auth/user/center", summary="获取考试试卷列表")
async def get_user_paper_list(auth: Auth = Depends(AllUserAuth()), pageCurrent: int = 1, pageSize: int = 20):
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

    datas, count = await crud.ExamPaperDal(auth.db).get_datas(
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



@app.post("/paper/auth/user/do/submit", summary="提交考试试卷")
async def user_submit_do_paper(data: schemas.ExamPaper, auth: Auth = Depends(FullAdminAuth())):
    paper_id = data.id
    user_id = auth.user.id
    score = 0

    for title_order, title_item in enumerate(data.title_items):
        for question_order, question_item in enumerate(title_item.question_items):
            if question_item.user_answer == question_item.question_info.correct:
                score += question_item.score

    answer = await crud.ExamUserDal(auth.db).create_data(data={
        "paper_id":paper_id,
        "user_id":user_id,
        "score":score
    })
    
    for title_order, title_item in enumerate(data.title_items):
        for question_order, question_item in enumerate(title_item.question_items):
            await crud.ExamUserAnswerDal(auth.db).create_data(data={
                "answer_id": answer["id"],
                "question_id": question_item.question_id,
                "correct": 1 if question_item.user_answer == question_item.question_info.correct else 0,
                "score": question_item.score if question_item.user_answer == question_item.question_info.correct else 0,
                "user_answer": question_item.user_answer
            })

    return SuccessResponse(answer)


@app.get("/paper/auth/user/records", summary="获取考试记录列表")
async def get_user_exam_records_list(auth: Auth = Depends(AllUserAuth()), pageCurrent: int = 1, pageSize: int = 20):
    exams, count = await crud.ExamUserDal(auth.db).get_datas(
        page=pageCurrent,
        limit=pageSize,
        v_return_count=True,
        user_id=auth.user.id,
        v_order_field="create_datetime",
        v_order="desc")
    paperids = [exam["paper_id"] for exam in exams]

    papers = await crud.ExamPaperDal(auth.db).get_datas(
        limit=0,
        v_return_count=False,
        id=("in", paperids))

    categoryids = [paper["category_id"] for paper in papers]
    categories = await CategoryDal(auth.db).get_datas(limit=0, v_return_count=False, id=("in",categoryids))

    for paper in papers:
        for category in categories:
            if paper["category_id"] == category["id"]:
                paper["category_name"] = category["category_name"]
                break

    for exam in exams:
        for paper in papers:
            if exam["paper_id"] == paper["id"]:
                exam["paper_name"] = paper["paper_name"]
                exam["paper_score"] = paper["paper_score"]
                exam["paper_time"] = paper["paper_time"]
                exam["category_name"] = paper["category_name"]
                break

    return SuccessResponse({"list": exams, "totalCount": count, "pageCurrent": pageCurrent, "pageSize": pageSize})


@app.get("/paper/auth/user/record/{data_id}", summary="获取考试记录信息")
async def get_paper(data_id: int, db: AsyncSession = Depends(db_getter)):
    schema = schemas.ExamUserSimpleOut
    exam = await crud.ExamUserDal(db).get_data(data_id, v_schema=schema)
    answers = await crud.ExamUserAnswerDal(db).get_datas(limit=0, v_return_count=False, answer_id=exam["id"])

    paper = await crud.ExamPaperDal(db).get_data(exam["paper_id"], v_schema=schemas.ExamPaperSimpleOut)
    titles = await crud.PaperTitleDal(db).get_datas(limit=0, v_return_count=False, v_order_field="order", paper_id=exam["paper_id"])
    titleids = [title["id"] for title in titles]
    for title in titles:
        questions = await crud.TitleQuestionDal(db).get_datas(limit=0, v_return_count=False, v_order_field="order", title_id=title["id"])
        for question in questions:
            question["question_info"] = await QuestionDal(db).get_data(question["question_id"], v_schema=QuestionSimpleOut)
            for answer in answers:
                if answer["question_id"] == question["question_id"]:
                    question["user_answer_id"] = answer["id"]
                    question["user_answer"] = answer["user_answer"]
                    question["user_correct"] = answer["correct"]
                    break
        title["question_items"] = questions
    paper["title_items"] = titles

    return SuccessResponse(paper)
