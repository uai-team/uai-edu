#!/usr/bin/python
# @Author   : uai-team
# @Version  : 1.0
# @Created  : 2025/07/24
# @File     : m2m.py
# @desc     : pydantic 模型，用于数据库序列化操作

from pydantic import BaseModel, Field, ConfigDict
from core.data_types import DatetimeStr
from apps.education.question.schemas import QuestionSimpleOut


class TitleQuestion(BaseModel):
    title_id: int | None = Field(None, title="标题ID")
    question_id: int | None = Field(None, title="题目ID")
    score: int | None = Field(None, title="分数")
    order: int | None = Field(None, title="显示排序")
    id: int | None = Field(None, title="编号")
    user_answer: str | None = Field(None, title="用户答案")
    question_info: QuestionSimpleOut | None = Field(None, title="题目信息")


class TitleQuestionSimpleOut(TitleQuestion):
    model_config = ConfigDict(from_attributes=True)

    create_datetime: DatetimeStr = Field(..., title="创建时间")
    update_datetime: DatetimeStr = Field(..., title="更新时间")
