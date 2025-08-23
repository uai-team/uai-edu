#!/usr/bin/python
# @Author   : uai-team
# @Version  : 1.0
# @Created  : 2025/06/25
# @File     : crud.py
# @desc     : 数据访问层

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from core.crud import DalBase
from . import models, schemas


class ZoneDal(DalBase):

    def __init__(self, db: AsyncSession):
        super(ZoneDal, self).__init__()
        self.db = db
        self.model = models.UaiEduZone
        self.schema = schemas.ZoneSimpleOut

    async def get_zone_options(
        self,
        page: int = 1,
        limit: int = 10,
        v_order: str = None,
        v_order_field: str = None,
        **kwargs) -> list:
        sql = select(self.model)
        sql = self.add_filter_condition(sql, **kwargs)
        queryset = await self.db.scalars(sql)
        datas = list(queryset.all())

        options = list(map(lambda zone: {"value": zone.id, "label": zone.zone_name, "order": zone.order}, datas))
        return options
