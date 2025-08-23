#!/usr/bin/python
# @Author   : uai-team
# @Version  : 1.0
# @Created  : 2025/06/25
# @File     : zone.py
# @desc     : pydantic 模型，用于数据库序列化操作

from pydantic import BaseModel, Field, ConfigDict
from core.data_types import DatetimeStr


class Course(BaseModel):
    course_name: str = Field(..., title="课程名称")
    course_cover: str = Field(..., title="课程封面")
    course_desc: str | None = Field(None, title="课程描述")
    lecturer: int | None = Field(None, title="授课教师")
    instructor: int | None = Field(None, title="指导教师")


class CourseSimpleOut(Course):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., title="编号")
    create_datetime: DatetimeStr = Field(..., title="创建时间")
    update_datetime: DatetimeStr = Field(..., title="更新时间")


class Zone(BaseModel):
    zone_type: str = Field(..., title="专区类型")
    zone_name: str = Field(..., title="专区名称")
    zone_desc: str | None = Field(None, title="专区描述")
    order: int | None = Field(None, title="显示排序")


class ZoneSimpleOut(Zone):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., title="编号")
    create_datetime: DatetimeStr = Field(..., title="创建时间")
    update_datetime: DatetimeStr = Field(..., title="更新时间")


class ZoneOut(ZoneSimpleOut):
    model_config = ConfigDict(from_attributes=True)

    courses: list[Course] = []
