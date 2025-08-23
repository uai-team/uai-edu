from typing import Any
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from sqlalchemy.orm.strategy_options import _AbstractLoad

from core.crud import DalBase
from core.exception import CustomException

from . import models, params, schemas
from ..category.crud import CategoryDal


class SimulationDal(DalBase):

    def __init__(self, db: AsyncSession):
        super(SimulationDal, self).__init__()
        self.db = db
        self.model = models.UaiEduSimulation
        self.schema = schemas.SimulationSimpleOut

    async def create_data(
            self,
            data: schemas.SimulationIn,
            v_options: list[_AbstractLoad] = None,
            v_return_obj: bool = False,
            v_schema: Any = None
    ) -> Any:
        obj = self.model(**data.model_dump(exclude={'category_ids'}))
        if data.category_ids:
            categories = await CategoryDal(self.db).get_datas(limit=0, id=("in", data.category_ids), v_return_objs=True)
            for category in categories:
                obj.categories.add(category)
        await self.flush(obj)
        return await self.out_dict(obj, v_options, v_return_obj, v_schema)

    async def put_data(
            self,
            data_id: int,
            data: schemas.SimulationIn,
            v_options: list[_AbstractLoad] = None,
            v_return_obj: bool = False,
            v_schema: Any = None
    ) -> Any:
        obj = await self.get_data(data_id, v_options=[joinedload(self.model.categories)])
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
            setattr(obj, key, value)
        await self.flush(obj)
        return await self.out_dict(obj, None, v_return_obj, v_schema)
