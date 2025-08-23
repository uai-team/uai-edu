#!/usr/bin/python
# @Author   : uai-team
# @Version  : 1.0
# @Created  : 2025/07/30
# @File     : crud.py
# @desc     : 数据访问层
from . import models, schemas
from sqlalchemy.ext.asyncio import AsyncSession
from core.crud import DalBase



class HomeworkDal(DalBase):

    def __init__(self, db: AsyncSession):
        super(HomeworkDal, self).__init__()
        self.db = db
        self.model = models.UaiEduHomework
        self.schema = schemas.HomeworkSimpleOut


class HomeworkItemDal(DalBase):

    def __init__(self, db: AsyncSession):
        super(HomeworkItemDal, self).__init__()
        self.db = db
        self.model = models.UaiEduHomeworkItem
        self.schema = schemas.HomeworkItemSimpleOut
