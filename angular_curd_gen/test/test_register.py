from datetime import datetime, date
from typing import Optional

from pydantic import BaseModel

from angular_curd_gen.field import Image, Url
from angular_curd_gen.register import ModelAdmin, generate_whole_app


class Users(BaseModel):
    id: int
    username: str
    password: Optional[str] = None
    firstname: str
    lastname: str
    nickname: str = ''
    gender: str
    birthday: date
    role: str
    email: str
    mobile: str
    address: str
    active: bool
    created: datetime


class Apps(BaseModel):
    id: int
    name: str
    appkey: str
    secret: str
    producer: str


class UsersAdmin(ModelAdmin):
    """用户管理注释文档信息"""
    model_readable_name = '用户'
    model_fields = ('id', 'username', 'lastname', 'firstname', 'gender', 'birthday', 'role', 'active', 'created')
    list_display_restraint = model_fields
    list_editable_restraint = ('username', 'gender')
    list_filter_fields = ('id', 'username', 'role', 'gender', 'active', 'birthday')
    model_edit_fields = ('username', 'lastname', 'firstname', 'gender', 'birthday', 'active')
    model_create_fields = ('username', 'lastname', 'firstname', 'gender', 'birthday', 'role', 'active')
    model_translate_fields = ('ID', '用户名', '姓氏', '名字', '性别', '生日', '角色', '是否激活', '创建时间')


class AppsAdmin(ModelAdmin):
    """应用管理注释文档信息"""
    model_readable_name = '应用'
    model_fields = ('id', 'name', 'appkey', 'secret', 'producer')
    list_display_restraint = model_fields
    list_editable_restraint = ('name', 'producer')
    model_edit_fields = ('name', 'appkey', 'secret', 'producer')
    model_create_fields = model_edit_fields
    model_translate_fields = ('ID', '名称', 'AppKey', 'Secret', '生产者')


class GameInfo(BaseModel):
    id: int
    link: Url
    title: str
    cover: Image
    views: int = None
    created: datetime = None


class GameInfoAdmin:
    """游戏信息管理注释文档信息"""
    model_readable_name = '游戏信息'
    model_fields = ('id', 'link', 'title', 'cover', 'views', 'created')
    list_display_restraint = ('id', 'link', 'title', 'cover', 'views')
    list_editable_restraint = ('link', 'title', 'cover', 'views')
    list_filter_fields = ('title',)
    list_sort_fields = ('views',)
    model_edit_fields = ('link', 'title', 'views')
    model_create_fields = model_edit_fields
    model_translate_fields = ('ID', '游戏链接', '游戏名称', '游戏封面', '浏览次数')


def test_register():
    # generate_whole_app(model_admin=UsersAdmin, model=Users, app_name='first', app_readable_name='第一个应用',
    #                    db_name='yd_user', db_user='test', db_pswd='test')
    generate_whole_app(model_admin=GameInfoAdmin, model=GameInfo, app_name='game', app_readable_name='HGame',
                       db_name='game_search', db_user='test', db_pswd='test')
    # generate_whole_app(model_admin=AppsAdmin, model=Apps, app_name='first', app_readable_name='纯应用')
