# b_auth
User rights control management module

# 配置
在settings.py 文件中加入
``` python
AUTHENTICATION_BACKENDS = ('b_auth.backend.Backend',)
AUTH_USER_MODEL = 'b_auth.User'
```
