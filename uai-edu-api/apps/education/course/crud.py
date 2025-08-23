#!/usr/bin/python
# @Author   : uai-team
# @Version  : 1.0
# @Created  : 2025/07/14
# @File     : crud.py
# @desc     : 数据访问层
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import joinedload
from core.exception import CustomException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm.strategy_options import _AbstractLoad
from core.crud import DalBase
from typing import Any

from . import schemas, models, params
from ..category.crud import CategoryDal
from ..zone.crud import ZoneDal


class CourseDal(DalBase):

    def __init__(self, db: AsyncSession):
        super(CourseDal, self).__init__()
        self.db = db
        self.model = models.UaiEduCourse
        self.schema = schemas.CourseSimpleOut

    async def create_data(
            self,
            data: schemas.CourseIn,
            v_options: list[_AbstractLoad] = None,
            v_return_obj: bool = False,
            v_schema: Any = None
    ) -> Any:
        obj = self.model(**data.model_dump(exclude={'category_ids', "zone_ids"}))
        if data.category_ids:
            categories = await CategoryDal(self.db).get_datas(limit=0, id=("in", data.category_ids), v_return_objs=True)
            for category in categories:
                obj.categories.add(category)
        if data.zone_ids:
            zones = await ZoneDal(self.db).get_datas(limit=0, id=("in", data.zone_ids), v_return_objs=True)
            for zone in zones:
                obj.zones.add(zone)
        await self.flush(obj)
        return await self.out_dict(obj, v_options, v_return_obj, v_schema)

    async def put_data(
            self,
            data_id: int,
            data: schemas.CourseIn,
            v_options: list[_AbstractLoad] = None,
            v_return_obj: bool = False,
            v_schema: Any = None
    ) -> Any:
        obj = await self.get_data(data_id, v_options=[joinedload(self.model.categories), joinedload(self.model.zones)])
        data_dict = jsonable_encoder(data)
        for key, value in data_dict.items():
            if key == "category_ids":
                if value:
                    categories = await CategoryDal(self.db).get_datas(limit=0, id=("in", value), v_return_objs=True)
                    if obj.categories:
                        obj.categories.clear()
                    for category in categories:
                        obj.categories.add(category)
                continue
            elif key == "zone_ids":
                if value:
                    zones = await ZoneDal(self.db).get_datas(limit=0, id=("in", value), v_return_objs=True)
                    if obj.zones:
                        obj.zones.clear()
                    for zone in zones:
                        obj.zones.add(zone)
                continue
            setattr(obj, key, value)
        await self.flush(obj)
        return await self.out_dict(obj, None, v_return_obj, v_schema)


class ChapterDal(DalBase):

    def __init__(self, db: AsyncSession):
        super(ChapterDal, self).__init__()
        self.db = db
        self.model = models.UaiEduCourseChapter
        self.schema = schemas.ChapterSimpleOut


class LessonDal(DalBase):

    def __init__(self, db: AsyncSession):
        super(LessonDal, self).__init__()
        self.db = db
        self.model = models.UaiEduCourseChapterLesson
        self.schema = schemas.LessonSimpleOut


class LessonProgressDal(DalBase):

    def __init__(self, db: AsyncSession):
        super(LessonProgressDal, self).__init__()
        self.db = db
        self.model = models.UaiEduCourseLessonProgress
        self.schema = schemas.StudyLessonProgressSimpleOut
