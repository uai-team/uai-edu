#!/usr/bin/python
# @Author   : uai-team
# @Version  : 1.0
# @Created  : 2025/07/30
# @File     : homework.py
# @desc     : pydantic 模型，用于数据库序列化操作

from pydantic import BaseModel, Field, ConfigDict
from core.data_types import DatetimeStr
from .homeworkitem import HomeworkItem


class Homework(BaseModel):
    category_id: int = Field(..., title="学科科目")
    dept_id: int = Field(..., title="可见范围")
    homework_name: str = Field(..., title="作业名称")
    others: str | None = Field(None, title="其他作业")


class HomeworkSimpleOut(Homework):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., title="编号")
    create_datetime: DatetimeStr = Field(..., title="创建时间")
    update_datetime: DatetimeStr = Field(..., title="更新时间")

class HomeworkIn(Homework):
    model_config = ConfigDict(from_attributes=True)
    items: list[HomeworkItem] = Field(..., title="作业项")