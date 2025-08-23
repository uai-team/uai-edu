#!/usr/bin/python
# @Author   : uai-team
# @Version  : 1.0
# @Created  : 2025/07/26
# @File     : exam.py
# @desc     : pydantic 模型，用于数据库序列化操作

from pydantic import BaseModel, Field, ConfigDict
from core.data_types import DatetimeStr


class ExamUser(BaseModel):
    paper_id: int = Field(..., title="试卷ID")
    user_id: int = Field(..., title="用户ID")
    score: int | None = Field(None, title="分数")


class ExamUserSimpleOut(ExamUser):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., title="编号")
    create_datetime: DatetimeStr = Field(..., title="创建时间")
    update_datetime: DatetimeStr = Field(..., title="更新时间")


class ExamUserAnswer(BaseModel):
    answer_id: int = Field(..., title="考试ID")
    question_id: int = Field(..., title="题目ID")
    correct: int = Field(..., title="是否正确")
    score: int | None = Field(None, title="分数")
    user_answer: str | None = Field(None, title="用户答案")
    id: int | None = Field(None, title="编号")


class ExamUserAnswerSimpleOut(ExamUserAnswer):
    model_config = ConfigDict(from_attributes=True)

    create_datetime: DatetimeStr = Field(..., title="创建时间")
    update_datetime: DatetimeStr = Field(..., title="更新时间")
