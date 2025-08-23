#!/usr/bin/python
# @Author   : uai-team
# @Version  : 1.0
# @Created  : 2025/07/30
# @File     : homeworkitem.py
# @desc     : pydantic 模型，用于数据库序列化操作

from pydantic import BaseModel, Field, ConfigDict
from core.data_types import DatetimeStr


class HomeworkItem(BaseModel):
    homework_id: int | None = Field(None, title="作业ID")
    item_type: str = Field(..., title="作业项类型")
    resource_id: int = Field(..., title="资源ID")
    order: int | None = Field(None, title="显示排序")


class HomeworkItemSimpleOut(HomeworkItem):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., title="编号")
    create_datetime: DatetimeStr = Field(..., title="创建时间")
    update_datetime: DatetimeStr = Field(..., title="更新时间")
