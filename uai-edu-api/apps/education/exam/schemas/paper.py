#!/usr/bin/python
# @Author   : uai-team
# @Version  : 1.0
# @Created  : 2025/07/24
# @File     : paper.py
# @desc     : pydantic 模型，用于数据库序列化操作

from pydantic import BaseModel, Field, ConfigDict
from core.data_types import DatetimeStr
from .title import PaperTitle


class ExamPaper(BaseModel):
    id: int | None = Field(None, title="编号")
    category_id: int = Field(..., title="学科科目")
    dept_id: int = Field(..., title="可见范围")
    paper_name: str = Field(..., title="试卷名称")
    paper_time: int = Field(..., title="考试时长")
    paper_score: int = Field(..., title="试卷总分")
    title_items: list[PaperTitle] | None = Field(None, title="试卷标题")


class ExamPaperSimpleOut(ExamPaper):
    model_config = ConfigDict(from_attributes=True)

    create_datetime: DatetimeStr = Field(..., title="创建时间")
    update_datetime: DatetimeStr = Field(..., title="更新时间")
