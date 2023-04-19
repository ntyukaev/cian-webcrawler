from sqlalchemy import create_engine, Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, String, Boolean, Text
from scrapy.utils.project import get_project_settings

Base = declarative_base()


def db_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    return create_engine(get_project_settings().get("CONNECTION_STRING"))


def create_table(engine):
    Base.metadata.create_all(engine)


class Cian(Base):
    __tablename__ = "cian"

    id = Column(Integer, primary_key=True)
    url = Column(String)
    lat = Column(String, nullable=True)
    lng = Column(String, nullable=True)
    price = Column(Integer, nullable=True)
    photos = Column(String, nullable=True)
    phones = Column(String, nullable=True)
    status = Column(String, nullable=True)
    address = Column(String, nullable=True)
    docx_url = Column(String, nullable=True)
    pdf_url = Column(String, nullable=True)
    category = Column(String, nullable=True)
    deal_type = Column(String, nullable=True)
    edit_date = Column(Integer, nullable=True)
    flat_type = Column(String, nullable=True)
    sale_type = Column(String, nullable=True)
    offer_type = Column(String, nullable=True)
    room_count = Column(Integer, nullable=True)
    total_area = Column(String, nullable=True)
    year_built = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    floor_count = Column(Integer, nullable=True)
    living_area = Column(String, nullable=True)
    repair_type = Column(String, nullable=True)
    floor_number = Column(Integer, nullable=True)
    kitchen_area = Column(String, nullable=True)
    balcony_count = Column(Integer, nullable=True)
    entrance_count = Column(Integer, nullable=True)
    total_visitors = Column(Integer, nullable=True)
    mortgage_allowed = Column(Boolean, nullable=True)
    price_per_square = Column(Integer, nullable=True)
    publication_date = Column(Integer, nullable=True)
    combined_wc_count = Column(Integer, nullable=True)
    separate_wc_count = Column(Integer, nullable=True)
    house_material_type = Column(String, nullable=True)
