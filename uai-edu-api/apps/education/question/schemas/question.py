#!/usr/bin/python
# @Author   : uai-team
# @Version  : 1.0
# @Created  : 2025/07/22
# @File     : question.py
# @desc     : pydantic 模型，用于数据库序列化操作

from pydantic import BaseModel, Field, ConfigDict
from core.data_types import DatetimeStr


class Question(BaseModel):
    question_type: str = Field(..., title="题目类型")
    category_id: int = Field(..., title="学科科目")
    lesson_id: int | None = Field(None, title="知识点")
    question_title: str = Field(..., title="题目内容")
    difficult: int | None = Field(None, title="题目难度")
    question_items: str | None = Field(None, title="答案选项")
    correct: str | None = Field(None, title="正确答案")
    analyze: str | None = Field(None, title="答案解析")


class QuestionSimpleOut(Question):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., title="编号")
    create_datetime: DatetimeStr = Field(..., title="创建时间")
    update_datetime: DatetimeStr = Field(..., title="更新时间")
