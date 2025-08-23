#!/usr/bin/python
# @Author   : uai-team
# @Version  : 1.0
# @Created  : 2025/07/03
# @File     : simulation.py
# @desc     : pydantic 模型，用于数据库序列化操作

from pydantic import BaseModel, Field, ConfigDict
from core.data_types import DatetimeStr
from apps.education.category.schemas.category import CategorySimpleOut


class Simulation(BaseModel):
    simulation_name: str = Field(..., title="仿真名称")
    simulation_cover: str = Field(..., title="仿真封面")
    simulation_path: str | None = Field(None, title="仿真资源")
    simulation_desc: str | None = Field(None, title="仿真描述")
    simulation_prompt: str | None = Field(None, title="系统提示词")


class SimulationIn(Simulation):
    category_ids: list[int] = []


class SimulationSimpleOut(Simulation):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., title="编号")
    create_datetime: DatetimeStr = Field(..., title="创建时间")
    update_datetime: DatetimeStr = Field(..., title="更新时间")


class SimulationOut(SimulationSimpleOut):
    model_config = ConfigDict(from_attributes=True)

    categories: list[CategorySimpleOut] = []