#!/usr/bin/python
# @Author   : uai-team
# @Version  : 1.0
# @Created  : 2025/06/24
# @File     : crud.py
# @desc     : 数据访问层

from sqlalchemy.ext.asyncio import AsyncSession
from core.crud import DalBase
from . import models, schemas


class CarouselDal(DalBase):

    def __init__(self, db: AsyncSession):
        super(CarouselDal, self).__init__()
        self.db = db
        self.model = models.UaiEduCarousel
        self.schema = schemas.CarouselSimpleOut
