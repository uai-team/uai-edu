#!/usr/bin/python
# @Author   : uai-team
# @Version  : 1.0
# @Created  : 2025/07/15
# @File     : lesson.py
# @desc     : pydantic 模型，用于数据库序列化操作

from pydantic import BaseModel, Field, ConfigDict
from core.data_types import DatetimeStr


class Lesson(BaseModel):
    chapter_id: int = Field(..., title="章节ID")
    lesson_name: str = Field(..., title="课时名称")
    lesson_type: str = Field(..., title="课时类型")
    order: int | None = Field(None, title="显示排序")
    lecturer: int | None = Field(None, title="授课教师")
    instructor: int | None = Field(None, title="指导教师")
    lesson_resource: str | None = Field(None, title="授课资源")
    lesson_courseware: str | None = Field(None, title="课件资源")
    lesson_tasklist: str | None = Field(None, title="学习任务")
    lesson_exercise: str | None = Field(None, title="课后练习")
    total_duration: float | None = Field(None, title="课时时长")
    lesson_desc: str | None = Field(None, title="课时描述")


class LessonSimpleOut(Lesson):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., title="编号")
    create_datetime: DatetimeStr = Field(..., title="创建时间")
    update_datetime: DatetimeStr = Field(..., title="更新时间")


class StudyLesson(BaseModel):
    course_id: int = Field(..., title="课程ID")
    lesson_id: int = Field(..., title="课时ID")


class StudyLessonProgress(BaseModel):
    course_id: int = Field(..., title="课程ID")
    chapter_id: int = Field(..., title="章节ID")
    lesson_id: int = Field(..., title="课时ID")
    user_id: int = Field(..., title="用户ID")
    current_duration: float = Field(..., title="学习时长")
    study_status: int = Field(..., title="学习状态")


class StudyLessonProgressSimpleOut(StudyLessonProgress):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., title="编号")
    create_datetime: DatetimeStr = Field(..., title="创建时间")
    update_datetime: DatetimeStr = Field(..., title="更新时间")
