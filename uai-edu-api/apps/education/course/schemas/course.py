#!/usr/bin/python
# @Author   : uai-team
# @Version  : 1.0
# @Created  : 2025/06/28
# @File     : course.py
# @desc     : pydantic 模型，用于数据库序列化操作

from pydantic import BaseModel, Field, ConfigDict
from core.data_types import DatetimeStr
from apps.education.category.schemas.category import CategorySimpleOut
from apps.education.zone.schemas import ZoneSimpleOut


class Course(BaseModel):
    course_name: str = Field(..., title="课程名称")
    course_cover: str = Field(..., title="课程封面")
    course_desc: str | None = Field(None, title="课程描述")
    lecturer: int | None = Field(None, title="授课教师")
    instructor: int | None = Field(None, title="指导教师")


class CourseIn(Course):
    category_ids: list[int] = []
    zone_ids: list[int] = []


class CourseSimpleOut(Course):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., title="编号")
    create_datetime: DatetimeStr = Field(..., title="创建时间")
    update_datetime: DatetimeStr = Field(..., title="更新时间")


class CourseOut(CourseSimpleOut):
    model_config = ConfigDict(from_attributes=True)

    categories: list[CategorySimpleOut] = []
    zones: list[ZoneSimpleOut] = []
    chapterRespList: list = []
