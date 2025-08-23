Generic single-database configuration.


## 新的数据迁移

- 新建模型：
  - 在你的app目录下新建一个models目录，`__init__.py`导入你需要迁移的models
  ```python
  # app/.../your_app/models/__init__.py
  from .your_model import YourModel,YourModel2
  
  ```
  ```python
  # app/.../your_app/models/your_model.py
  from db.db_base import BaseModel
  
  class YourModel(BaseModel):
    # 定义你的model
    ...
  
  class YourModel2(BaseModel):
    # 定义你的model
    ...
  ```
- 根据模型配置你的alembic：
  ```
  # alembic.ini
  [dev]
  ...
  sqlalchemy.url = mysql+pymysql://your_username:password@ip:port/your_db_name
  ...
  ```
  ```python
  # alembic/env.py
  # 导入项目中的基本映射类，与 需要迁移的 ORM 模型
  from apps.vadmin.auth.models import *
  ...
  from apps.xxx.your_app.models import *
  ```
- 执行数据库迁移命令（终端执行执行脚本）：
  ```shell
  # 执行命令（生产环境）：
  python main.py migrate
  
  # 执行命令（开发环境）：
  python main.py migrate --env dev
  
  # 开发环境的原命令
  alembic --name dev revision --autogenerate -m 2.0
  alembic --name dev upgrade head
  ```

生成迁移文件后，会在alembic迁移目录中的version目录中多个迁移文件

## 新的CRUD

- 新的模型文件已经建好（上一步迁移时必须）
- 在 scripts/crud_generate/main.py 添加执行命令

```python
# scripts/crud_generate/main.py
if __name__ == '__main__':
    from apps.xxx.your_app.models import YourModel

    crud = CrudGenerate(YourModel, "中文名", "en_name")
    # 只打印代码，不执行创建写入
    crud.generate_codes()
    # 创建并写入代码
    crud.main()
```

- 生成后会自动创建crud, params,schema, views

## 新的路由配置

```python
# application/urls.py

from apps.xxx.your_app.views import app as your_app

urlpatterns = [
    ...,
    {"ApiRouter": your_app, "prefix": "/your_router", "tags": ["your_tag"]},
]
```

完成后在 http://127.0.0.1:9000/docs 验证生成的接口
