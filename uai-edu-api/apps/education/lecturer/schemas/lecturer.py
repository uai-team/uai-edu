#!/usr/bin/python
# @Author   : uai-team
# @Version  : 1.0
# @Created  : 2025/06/28
# @File     : lecturer.py
# @desc     : pydantic 模型，用于数据库序列化操作

from pydantic import BaseModel, Field, ConfigDict
from core.data_types import DatetimeStr


class Lecturer(BaseModel):
    lecturer_name: str = Field(..., title="教师名称")
    lecturer_avatar: str = Field(..., title="教师头像")
    lecturer_title: str = Field(..., title="教师职称")
    lecturer_position: str = Field(..., title="教师职务")
    lecturer_desc: str | None = Field(None, title="教师描述")


class LecturerSimpleOut(Lecturer):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., title="编号")
    create_datetime: DatetimeStr = Field(..., title="创建时间")
    update_datetime: DatetimeStr = Field(..., title="更新时间")
