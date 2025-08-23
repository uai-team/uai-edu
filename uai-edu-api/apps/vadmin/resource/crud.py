#!/usr/bin/python
# @Author   : uai-team
# @Version  : 1.0
# @Created  : 2025/06/24
# @File     : crud.py
# @desc     : 数据访问层

from sqlalchemy.ext.asyncio import AsyncSession
from . import schemas, models
from core.crud import DalBase


class ImagesDal(DalBase):

    def __init__(self, db: AsyncSession):
        super(ImagesDal, self).__init__()
        self.db = db
        self.model = models.VadminImages
        self.schema = schemas.ImagesSimpleOut


class LinksDal(DalBase):

    def __init__(self, db: AsyncSession):
        super(LinksDal, self).__init__()
        self.db = db
        self.model = models.VadminLinks
        self.schema = schemas.LinksSimpleOut
