#!/usr/bin/python
# @Author   : uai-team
# @Version  : 1.0
# @Created  : 2025/07/07
# @File     : book.py
# @desc     : pydantic 模型，用于数据库序列化操作

from pydantic import BaseModel, Field, ConfigDict
from core.data_types import DatetimeStr
from apps.education.category.schemas.category import CategorySimpleOut


class Book(BaseModel):
    book_name: str = Field(..., title="教材名称")
    book_cover: str = Field(..., title="教材封面")
    book_path: str | None = Field(None, title="教材资源")
    book_desc: str | None = Field(None, title="教材描述")


class BookIn(Book):
    category_ids: list[int] = []


class BookSimpleOut(Book):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., title="编号")
    create_datetime: DatetimeStr = Field(..., title="创建时间")
    update_datetime: DatetimeStr = Field(..., title="更新时间")


class BookOut(BookSimpleOut):
    model_config = ConfigDict(from_attributes=True)

    categories: list[CategorySimpleOut] = []
