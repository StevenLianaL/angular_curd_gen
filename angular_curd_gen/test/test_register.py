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
    user_views: int
    created: datetime


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


class Client(BaseModel):
    id: int
    name: str


class ClientAdmin:
    """游戏信息管理注释文档信息"""
    model_readable_name = '客户端'
    model_fields = ('id', 'name')
    list_display_restraint = ('id', 'name')
    list_editable_restraint = ('id', 'name')
    list_filter_fields = ('name',)
    list_sort_fields = ('name',)
    model_edit_fields = ('name',)
    model_create_fields = ('name',)
    model_translate_fields = ('ID', '名称')


# create table papers
# (
#     name        varchar(100)                          not null,
#     grade       varchar(2)                            not null,
#     id          int auto_increment
#         primary key,
#     test_type   varchar(20) default ''                null,
#     sections    varchar(30)                           null,
#     instruction varchar(1000)                         null,
#     created     datetime    default CURRENT_TIMESTAMP not null
# )
class Paper(BaseModel):
    id: int
    name: str
    grade: str
    parent_id: int
    version: int
    test_type: str = ""
    created: datetime


class PapersAdmin:
    """试卷管理注释文档信息"""
    model_readable_name = '试卷'
    model_fields = ('id', 'name', 'grade', 'test_type', 'created', 'parent_id', 'version')
    list_display_restraint = ('id', 'name', 'grade', 'test_type', 'version', 'created')
    list_editable_restraint = ('name', 'grade', 'test_type')
    list_filter_fields = ('name', 'grade', 'test_type')
    list_sort_fields = ('created',)
    model_edit_fields = ('name', 'grade')
    model_create_fields = ('name', 'grade',)
    model_translate_fields = ('ID', '名称', '年级', '试卷类型', '创建时间', '父卷ID', '版本')


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


class Product(BaseModel):
    id: int
    name: str
    price: float
    detail: str
    version: str
    created: datetime


class ProductsAdmin:
    model_readable_name = '产品'
    model_fields = ('id', 'name', 'price', 'detail', 'version', 'created')
    list_display_restraint = ('id', 'name', 'price', 'detail', 'version', 'created')
    list_editable_restraint = ()
    list_filter_fields = ('name', 'price', 'version')
    list_sort_fields = ('price', 'created')
    model_edit_fields = ('name', 'price', 'detail', 'version')
    model_create_fields = ('name', 'price', 'detail', 'version')
    model_translate_fields = ('ID', '名称', '价格', '详情', '版本', '创建时间')


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


class Item(BaseModel):
    id: int
    item_text: str
    choices: str
    item_key: str = ""
    item_type: str
    grade: str
    test_type: int
    source: str
    status: int
    author_id: int
    created: datetime
    parent_id: int
    version: int


class ItemsAdmin:
    model_readable_name = '试题'
    model_fields = (
        'id', 'item_text', 'choices', 'item_key', 'item_type',
        'grade', 'test_type', 'source', 'status', 'author_id',
        'created', 'parent_id', 'version'
    )
    list_display_restraint = (
        'id', 'item_text', 'choices', 'item_key', 'item_type',
        'grade', 'test_type', 'source', 'created'
    )
    list_editable_restraint = ()
    list_filter_fields = ('item_text', 'grade', 'test_type')
    list_sort_fields = ('created', 'grade', 'test_type')
    model_edit_fields = ('item_text', 'choices', 'item_key', 'item_type', 'grade', 'status')
    model_create_fields = ('item_text', 'choices', 'item_key', 'item_type', 'grade', 'test_type')
    model_translate_fields = (
        'ID', '题目文本', '选项', '题目标识', '题目类型', '年级',
        '测试类型', '来源', '状态', '作者ID', '创建时间', '父题ID', '版本'
    )


class Marking(BaseModel):
    id: int
    examinee_id: int
    item_code: str
    paper_id: int
    exam_id: int
    first_score: str = ""
    second_score: str = ""
    final_score: str = ""
    markers: str = ''


class MarkingsAdmin:
    model_readable_name = '打分'
    model_fields = (
        'id', 'examinee_id', 'item_code', 'paper_id', 'exam_id',
        'first_score', 'second_score', 'final_score', 'markers'
    )
    list_display_restraint = (
        'examinee_id', 'item_code', 'first_score'
    )
    list_editable_restraint = ()
    list_filter_fields = ('examinee_id', 'item_code', 'exam_id')
    list_sort_fields = ('examinee_id', 'exam_id')
    model_edit_fields = ('first_score', 'second_score', 'final_score')
    model_create_fields = ('examinee_id', 'item_code', 'paper_id', 'exam_id')
    model_translate_fields = (
        'ID', '考生ID', '题目编号', '试卷ID', '考试ID',
        '初评分数', '复评分数', '终审分数',  '标记'
    )


def test_register_game():
    generate_whole_app(model_admin=GameInfoAdmin, model=GameInfo, app_name='game', app_readable_name='HGame',
                       db_name='game_search', db_user='test', db_pswd='test')


def test_register():
    # generate_whole_app(model_admin=UsersAdmin, model_pos=Users, app_name='first', app_readable_name='第一个应用',
    #                    db_name='yd_user', db_user='test', db_pswd='test')

    # generate_whole_app(model_admin=VideosAdmin, model=Video, app_name='health_videos', app_readable_name='视频平台',
    #                    db_name='health_videos', db_user='test', db_pswd='test')
    # generate_whole_app(model_admin=TradesAdmin, model=Trades, app_name='transactions', app_readable_name='交易',
    #                    db_name='transactions', db_user='test', db_pswd='test')
    # generate_whole_app(model_admin=TradesAdmin, model=Trades, app_name='pay', app_readable_name='交易',
    #                    db_name='transactions', db_user='test', db_pswd='test')
    # generate_whole_app(model_admin=ProductsAdmin, model=Product, app_name='transactions', app_readable_name='产品',
    #                    db_name='transactions', db_user='test', db_pswd='test')
    # generate_whole_app(model_admin=PapersAdmin, model=Paper, app_name='paper', app_readable_name='试卷',
    #                    db_name='yass', db_user='test', db_pswd='test')
    generate_whole_app(model_admin=MarkingsAdmin, model=Marking, app_name='marking', app_readable_name='打分',
                       db_name='peyel_admin', db_user='test', db_pswd='test')
    # generate_whole_app(model_admin=ItemsAdmin, model=Item, app_name='Item', app_readable_name='试卷',
    #                    db_name='yass', db_user='test', db_pswd='test')
