from peewee import *

database = PostgresqlDatabase('crawler', **{'host': 'localhost', 'port': 5432, 'user': 'postgres', 'password': '9527'})

class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
    class Meta:
        database = database

class SpiderDesign006Designer(BaseModel):
    avatar_pic_url = CharField(null=True)
    crawl_status = SmallIntegerField(constraints=[SQL("DEFAULT 1")], null=True)
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    designer_level = CharField(null=True)
    designer_name = CharField(null=True)
    homepage_url = CharField()
    priority = SmallIntegerField(constraints=[SQL("DEFAULT 1")], null=True)
    remark = CharField(null=True)
    status = SmallIntegerField(constraints=[SQL("DEFAULT 1")])
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    works_num = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)

    class Meta:
        table_name = 'spider_design006_designer'

class SpiderDesign006Pic(BaseModel):
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    designer_id = IntegerField(constraints=[SQL("DEFAULT 1")], null=True)
    remark = CharField(null=True)
    status = SmallIntegerField(constraints=[SQL("DEFAULT 1")])
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    works_name = CharField(null=True)
    works_page_url = CharField(null=True)
    works_pic_url = CharField(null=True)
    works_upload_time = DateTimeField(null=True)

    class Meta:
        table_name = 'spider_design006_pic'

