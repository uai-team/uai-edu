#!/usr/bin/python
# @Author   : uai-team
# @Version  : 1.0
# @Created  : 2025/06/25
# @File     : category.py
# @desc     : pydantic 模型，用于数据库序列化操作

from pydantic import BaseModel, Field, ConfigDict
from core.data_types import DatetimeStr


class Category(BaseModel):
    category_type: str = Field(..., title="类目类型")
    category_name: str = Field(..., title="类目名称")
    order: int | None = Field(None, title="显示排序")
    desc: str | None = Field(None, title="描述")
    parent_id: int | None = Field(None, title="上级类目")


class CategorySimpleOut(Category):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., title="编号")
    create_datetime: DatetimeStr = Field(..., title="创建时间")
    update_datetime: DatetimeStr = Field(..., title="更新时间")


class CategoryTreeListOut(CategorySimpleOut):
    model_config = ConfigDict(from_attributes=True)

    children: list[dict] = []
