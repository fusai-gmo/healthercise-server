import sys
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from setting import Base
from setting import ENGINE

class activityLevel(Base):
    """
    activityLevelモデル
    """
    __tablename__ = 'activityLevel'
    id = Column('id', Integer, primary_key = True)
    list_id = Column('list_id', Integer)
    level = Column('level', String(300))
    list_id = relationship("activityList")


def main(args):
    """
    メイン関数
    """
    Base.metadata.create_all(bind=ENGINE, checkfirst=True)

if __name__ == "__main__":
    main(sys.argv)