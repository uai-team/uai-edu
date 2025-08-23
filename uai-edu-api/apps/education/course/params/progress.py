from fastapi import Depends, Query
from core.dependencies import Paging, QueryParams


class LessonProgressParams(QueryParams):
    def __init__(
            self,
            course_id: int | None = Query(None, title="课程ID"),
            chapter_id: int | None = Query(None, title="章节ID"),
            lesson_id: int | None = Query(None, title="课时ID"),
            params: Paging = Depends()
    ):
        super().__init__(params)
        self.course_id = course_id
        self.chapter_id = chapter_id
        self.lesson_id = lesson_id
