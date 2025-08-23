from apps.common.common import app as common_app

from apps.vadmin.auth.utils.login import app as auth_app
from apps.vadmin.auth.views import app as vadmin_auth_app
from apps.vadmin.system.views import app as vadmin_system_app
from apps.vadmin.record.views import app as vadmin_record_app
from apps.vadmin.workplace.views import app as vadmin_workplace_app
from apps.vadmin.analysis.views import app as vadmin_analysis_app
from apps.vadmin.help.views import app as vadmin_help_app
from apps.vadmin.resource.views import app as vadmin_resource_app

from apps.vadmin.auth.utils.user_login import app as user_auth_app

from apps.education.banner.views import app as education_banner_app
from apps.education.category.views import app as education_category_app
from apps.education.zone.views import app as education_zone_app
from apps.education.course.views import app as education_course_app
from apps.education.lecturer.views import app as education_lecturer_app
from apps.education.simulation.views import app as education_simulation_app
from apps.education.book.views import app as education_book_app

from apps.education.question.views import app as education_question_app
from apps.education.exam.views import app as education_exam_app
from apps.education.wrong.views import app as education_wrong_app
from apps.education.homework.views import app as education_homework_app


# 引入应用中的路由
urlpatterns = [
    {"ApiRouter": common_app, "prefix": "/common", "tags": ["公共模块"]},

    {"ApiRouter": auth_app, "prefix": "/auth", "tags": ["系统认证"]},
    {"ApiRouter": vadmin_auth_app, "prefix": "/vadmin/auth", "tags": ["权限管理"]},
    {"ApiRouter": vadmin_system_app, "prefix": "/vadmin/system", "tags": ["系统管理"]},
    {"ApiRouter": vadmin_record_app, "prefix": "/vadmin/record", "tags": ["记录管理"]},
    {"ApiRouter": vadmin_workplace_app, "prefix": "/vadmin/workplace", "tags": ["工作区管理"]},
    {"ApiRouter": vadmin_analysis_app, "prefix": "/vadmin/analysis", "tags": ["数据分析管理"]},
    {"ApiRouter": vadmin_help_app, "prefix": "/vadmin/help", "tags": ["帮助中心管理"]},
    {"ApiRouter": vadmin_resource_app, "prefix": "/vadmin/resource", "tags": ["资源管理"]},

    {"ApiRouter": user_auth_app, "prefix": "/user", "tags": ["用户认证"]},

    {"ApiRouter": education_banner_app, "prefix": "/education", "tags": ["轮播图管理"]},
    {"ApiRouter": education_category_app, "prefix": "/education", "tags": ["类目管理"]},
    {"ApiRouter": education_zone_app, "prefix": "/education", "tags": ["专区管理"]},
    {"ApiRouter": education_course_app, "prefix": "/education", "tags": ["课程管理"]},
    {"ApiRouter": education_lecturer_app, "prefix": "/education", "tags": ["教师管理"]},
    {"ApiRouter": education_simulation_app, "prefix": "/education", "tags": ["仿真管理"]},
    {"ApiRouter": education_book_app, "prefix": "/education", "tags": ["教材管理"]},

    {"ApiRouter": education_question_app, "prefix": "/education", "tags": ["题目管理"]},
    {"ApiRouter": education_exam_app, "prefix": "/education", "tags": ["试卷管理"]},
    {"ApiRouter": education_wrong_app, "prefix": "/education", "tags": ["错题管理"]},
    {"ApiRouter": education_homework_app, "prefix": "/education", "tags": ["作业管理"]},
]
