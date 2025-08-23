#!/usr/bin/python
# @Author   : uai-team
# @Version  : 1.0
# @Created  : 2025/07/22
# @File     : crud.py
# @desc     : 数据访问层

from sqlalchemy.ext.asyncio import AsyncSession
from core.crud import DalBase
from . import models, schemas


class QuestionDal(DalBase):

    def __init__(self, db: AsyncSession):
        super(QuestionDal, self).__init__()
        self.db = db
        self.model = models.UaiEduQuestion
        self.schema = schemas.QuestionSimpleOut
