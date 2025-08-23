#!/usr/bin/python
# @Author   : uai-team
# @Version  : 1.0
# @Created  : 2025/06/25
# @File     : crud.py
# @desc     : 数据访问层

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from core.crud import DalBase
from core.exception import CustomException
from . import models, params, schemas


class CategoryDal(DalBase):

    def __init__(self, db: AsyncSession):
        super(CategoryDal, self).__init__()
        self.db = db
        self.model = models.UaiEduCategory
        self.schema = schemas.CategorySimpleOut

    async def get_tree_list(
        self, 
        mode: int, 
        page: int = 1,
        limit: int = 10,
        v_order: str = None,
        v_order_field: str = None,
        **kwargs) -> list:
        """
        1：获取类目树列表
        2：获取类目树选择项，添加/修改类目时使用
        :param mode:
        :return:
        """
        sql = select(self.model)
        sql = self.add_filter_condition(sql, **kwargs)
        queryset = await self.db.scalars(sql)
        datas = list(queryset.all())
        roots = filter(lambda i: not i.parent_id, datas)
        if mode == 1:
            categories = self.generate_tree_list(datas, roots)
        elif mode == 2 or mode == 3:
            categories = self.generate_tree_options(datas, roots)
        else:
            raise CustomException("获取类目失败，无可用选项", code=400)
        return self.category_order(categories)


    async def get_category_children_id(
        self,
        category_type: str,
        id: int, 
    ) -> list:
        sql = select(self.model).where(self.model.category_type == category_type)
        queryset = await self.db.scalars(sql)
        datas = list(queryset.all())
        roots = filter(lambda i: i.parent_id == id if id else not i.parent_id, datas)
        categories = self.generate_children_id(datas, roots)
        if id:
            categories.append(id)
        return categories


    def generate_children_id(self, categories: list[models.UaiEduCategory], nodes: filter) -> list:
        data = []
        for root in nodes:
            router = schemas.CategoryTreeListOut.model_validate(root)
            sons = filter(lambda i: i.parent_id == root.id, categories)
            children = self.generate_children_id(categories, sons)
            data.append(router.id)
            for child in children:
                data.append(child)
        return data


    def generate_tree_list(self, categories: list[models.UaiEduCategory], nodes: filter) -> list:
        """
        生成类目树列表
        :param categories: 总类目列表
        :param nodes: 每层节点类目列表
        :return:
        """
        data = []
        for root in nodes:
            router = schemas.CategoryTreeListOut.model_validate(root)
            sons = filter(lambda i: i.parent_id == root.id, categories)
            router.children = self.generate_tree_list(categories, sons)
            data.append(router.model_dump())
        return data

    def generate_tree_options(self, categories: list[models.UaiEduCategory], nodes: filter) -> list:
        """
        生成类目树选择项
        :param categories: 总类目列表
        :param nodes: 每层节点类目列表
        :return:
        """
        data = []
        for root in nodes:
            router = {"value": root.id, "label": root.category_name, "order": root.order}
            sons = filter(lambda i: i.parent_id == root.id, categories)
            router["children"] = self.generate_tree_options(categories, sons)
            data.append(router)
        return data

    @classmethod
    def category_order(cls, datas: list, order: str = "order", children: str = "children") -> list:
        """
        部门排序
        :param datas:
        :param order:
        :param children:
        :return:
        """
        result = sorted(datas, key=lambda category: category[order])
        for item in result:
            if item[children]:
                item[children] = sorted(item[children], key=lambda category: category[order])
        return result
