import sys
import models.activity_level
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from setting import Base
from setting import ENGINE

class activity(Base):
    """
    activityモデル
    """
    __tablename__ = 'activity'
    id = Column('id', Integer, primary_key = True, autoincrement=True)
    strength = Column('strength', ForeignKey('activity_level.id',onupdate='CASCADE', ondelete='CASCADE'))
    name = Column('name', String(100) )
    calory = Column('calory', Integer )

# def main(args):
#     """
#     メイン関数
#     """
#     Base.metadata.create_all(bind=ENGINE, checkfirst=True)

# if __name__ == "__main__":
#     main(sys.argv)