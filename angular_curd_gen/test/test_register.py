from datetime import datetime, date
from typing import Optional

from pydantic import BaseModel

from angular_curd_gen.field import Image, Url
from angular_curd_gen.register import ModelAdmin, generate_whole_app


class GameInfo(BaseModel):
    id: int
    link: Url
    game_title: str
    cover: Image
    user_views: int = None
    created: datetime = None


class GameInfoAdmin:
    """游戏信息管理注释文档信息"""
    model_readable_name = '游戏信息'
    model_fields = ('id', 'link', 'game_title', 'cover', 'user_views', 'created')
    list_display_restraint = ('id', 'link', 'game_title', 'cover', 'user_views')
    list_editable_restraint = ('link', 'game_title', 'cover', 'user_views')
    list_filter_fields = ('game_title',)
    list_sort_fields = ('user_views',)
    model_edit_fields = ('link', 'game_title', 'user_views')
    model_create_fields = model_edit_fields
    model_translate_fields = ('ID', '游戏链接', '游戏名称', '游戏封面', '浏览次数')


class Video(BaseModel):
    id: int
    name: str
    abstract: str = ""
    word: str = ""
    cloud_id: str = ""
    tags: str = ""
    category: str = ""
    chapter: str = ""
    grades: str = "[]"
    integration: str = "[]"
    field: str = "[]"
    source: str = "public"


class VideosAdmin:
    """游戏信息管理注释文档信息"""
    model_readable_name = '视频'
    model_fields = ('id', 'name', 'abstract', 'word', 'cloud_id', 'tags', 'category',
                    'chapter', 'grades', 'integration', 'field', 'source')
    list_display_restraint = ('id', 'name', 'grades', 'chapter', 'abstract', 'field', 'integration')
    list_editable_restraint = ()
    list_filter_fields = ('name', 'grades', 'field', 'integration', 'integration')
    list_sort_fields = ()
    model_edit_fields = ('name', 'chapter', 'abstract', 'field')
    model_create_fields = ('name', 'chapter', 'abstract', 'field', 'cloud_id')
    model_translate_fields = ('ID', '名称', '摘要', '脚本', '云链接', '标签',
                              '分类', '节', '年级', '学科覆盖', '领域', '来源')


class Trades(BaseModel):
    id: int
    self_trade_no: str
    out_trade_no: str
    name: str
    product_id: int
    user_id: int
    price: float
    is_paid: bool
    pay_method: str
    created: datetime


class TradesAdmin:
    model_readable_name = '交易'
    model_fields = ('id', 'self_trade_no', 'out_trade_no', 'name', 'product_id', 'user_id', 'price',
                    'is_paid', 'pay_method', 'created')
    list_display_restraint = ('id', 'name', 'product_id', 'user_id', 'price', 'is_paid', 'pay_method', 'created')
    list_editable_restraint = ()
    list_filter_fields = ('name', 'is_paid', 'product_id', 'pay_method')
    list_sort_fields = ('price', 'created')
    model_edit_fields = ('name', 'price')
    model_create_fields = ('self_trade_no', 'out_trade_no', 'name', 'product_id', 'user_id', 'price', 'pay_method')
    model_translate_fields = (
        'ID', '交易号', '外部交易号', '商品名称', '商品ID', '用户ID', '价格', '是否支付', '支付方式', '创建时间')


def test_register():
    # generate_whole_app(model_admin=UsersAdmin, model_pos=Users, app_name='first', app_readable_name='第一个应用',
    #                    db_name='yd_user', db_user='test', db_pswd='test')
    generate_whole_app(model_admin=GameInfoAdmin, model=GameInfo, app_name='game', app_readable_name='HGame',
                       db_name='game_search', db_user='test', db_pswd='test')
    # generate_whole_app(model_admin=TradesAdmin, model_pos=Trades, app_name='auto_tasks', app_readable_name='自动任务',
    #                    db_name='transactions', db_user='test', db_pswd='test')
