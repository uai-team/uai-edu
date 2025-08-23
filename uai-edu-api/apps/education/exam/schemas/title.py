#!/usr/bin/python
# @Author   : uai-team
# @Version  : 1.0
# @Created  : 2025/07/24
# @File     : title.py
# @desc     : pydantic 模型，用于数据库序列化操作

from pydantic import BaseModel, Field, ConfigDict
from core.data_types import DatetimeStr
from .m2m import TitleQuestion


class PaperTitle(BaseModel):
    paper_id: int | None = Field(None, title="试卷ID")
    id: int | None = Field(None, title="编号")
    title_name: str | None = Field(None, title="标题名称")
    order: int | None = Field(None, title="显示排序")
    question_items: list[TitleQuestion] | None = Field(None, title="题目列表")


class PaperTitleSimpleOut(PaperTitle):
    model_config = ConfigDict(from_attributes=True)

    create_datetime: DatetimeStr = Field(..., title="创建时间")
    update_datetime: DatetimeStr = Field(..., title="更新时间")
