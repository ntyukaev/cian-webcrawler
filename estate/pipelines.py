# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from sqlalchemy.orm import sessionmaker
from scrapy.exceptions import DropItem
from .models import create_table, db_connect, Cian


class CianPipeline:
    def __init__(self):
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        if not item and item.get("data"):
            return DropItem
        data = item.get("data")
        session = self.Session()
        existing_record = session.query(Cian).filter_by(id=data.id).first()
        status = "New"
        if existing_record:
            if existing_record.edit_date >= data.edit_date:
                return data
            status = "Updated"
        spider.updates.append(" ".join([status, data.url]))
        try:
            session.merge(data)
            session.commit()
        except:
            session.rollback()
        finally:
            session.close()
        return data
