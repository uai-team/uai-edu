#!/usr/bin/python
# @Author   : uai-team
# @Version  : 1.0
# @Created  : 2025/06/28
# @File     : crud.py
# @desc     : 数据访问层

from sqlalchemy.ext.asyncio import AsyncSession
from core.crud import DalBase
from . import models, schemas


class LecturerDal(DalBase):

    def __init__(self, db: AsyncSession):
        super(LecturerDal, self).__init__()
        self.db = db
        self.model = models.UaiEduLecturer
        self.schema = schemas.LecturerSimpleOut
