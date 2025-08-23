#!/usr/bin/python
# @Author   : uai-team
# @Version  : 1.0
# @Created  : 2025/07/29
# @File     : notebook.py
# @desc     : pydantic 模型，用于数据库序列化操作

from pydantic import BaseModel, Field, ConfigDict
from core.data_types import DatetimeStr


class Notebook(BaseModel):
    answer_id: int = Field(..., title="考试ID")
    question_id: int = Field(..., title="题目ID")
    user_answer: str | None = Field(None, title="用户答案")
    wrong_datetime: DatetimeStr = Field(..., title="创建时间")
    review_count: int = Field(0, title="复习次数")
    last_review_time: DatetimeStr | None = Field(None, title="上次复习时间")


class NotebookSimpleOut(Notebook):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., title="编号")
    create_datetime: DatetimeStr = Field(..., title="创建时间")
    update_datetime: DatetimeStr = Field(..., title="更新时间")
