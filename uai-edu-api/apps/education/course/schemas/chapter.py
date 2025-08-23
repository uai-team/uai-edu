#!/usr/bin/python
# @Author   : uai-team
# @Version  : 1.0
# @Created  : 2025/07/14
# @File     : chapter.py
# @desc     : pydantic 模型，用于数据库序列化操作

from pydantic import BaseModel, Field, ConfigDict
from core.data_types import DatetimeStr


class Chapter(BaseModel):
    course_id: int = Field(..., title="课程ID")
    chapter_name: str = Field(..., title="章节名称")
    chapter_desc: str | None = Field(None, title="章节描述")
    order: int | None = Field(None, title="显示排序")


class ChapterSimpleOut(Chapter):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., title="编号")
    create_datetime: DatetimeStr = Field(..., title="创建时间")
    update_datetime: DatetimeStr = Field(..., title="更新时间")
