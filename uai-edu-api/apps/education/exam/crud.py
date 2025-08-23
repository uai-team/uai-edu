#!/usr/bin/python
# @Author   : uai-team
# @Version  : 1.0
# @Created  : 2025/07/24
# @File     : crud.py
# @desc     : 数据访问层
from core.crud import DalBase
from . import models, schemas
from sqlalchemy.ext.asyncio import AsyncSession



class ExamPaperDal(DalBase):

    def __init__(self, db: AsyncSession):
        super(ExamPaperDal, self).__init__()
        self.db = db
        self.model = models.UaiEduExamPaper
        self.schema = schemas.ExamPaperSimpleOut


class PaperTitleDal(DalBase):

    def __init__(self, db: AsyncSession):
        super(PaperTitleDal, self).__init__()
        self.db = db
        self.model = models.UaiEduExamPaperTitle
        self.schema = schemas.PaperTitleSimpleOut


class TitleQuestionDal(DalBase):

    def __init__(self, db: AsyncSession):
        super(TitleQuestionDal, self).__init__()
        self.db = db
        self.model = models.UaiEduExamPaperTitleQuestions
        self.schema = schemas.TitleQuestionSimpleOut


class ExamUserDal(DalBase):

    def __init__(self, db: AsyncSession):
        super(ExamUserDal, self).__init__()
        self.db = db
        self.model = models.UaiEduExamUser
        self.schema = schemas.ExamUserSimpleOut


class ExamUserAnswerDal(DalBase):

    def __init__(self, db: AsyncSession):
        super(ExamUserAnswerDal, self).__init__()
        self.db = db
        self.model = models.UaiEduExamUserAnswer
        self.schema = schemas.ExamUserAnswerSimpleOut
