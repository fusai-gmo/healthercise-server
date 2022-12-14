import sys
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime, Time
from sqlalchemy.schema import ForeignKey
from sqlalchemy.orm import relationship
from setting import Base
from setting import ENGINE

class user(Base):
    """
    ユーザモデル
    """
    __tablename__ = 'user'
    id = Column('id', Integer, primary_key = True, autoincrement=True)
    firebase_id = Column('firebase_id', String(50), unique = True)
    name = Column('name', String(200))
    email = Column('email', String(100))
    age = Column('age', Integer)
    height = Column('height', Integer)
    weight = Column('weight', Integer)
    slack_id = Column('slack_id', String(100))
    notify_start_time = Column( 'notify_start_time', Time)
    notify_finish_time = Column( 'notify_finish_time', Time)

    sex = relationship('sex')
    commute = relationship('commute')
    activity_level = relationship('activity_level')
    # access_token = relationship('access_token')
    activity_log = relationship('activity_log')
    activity_summary = relationship('activity_summary')
    


# def main(args):
#     """
#     メイン関数
#     """
#     Base.metadata.create_all(bind=ENGINE,checkfirst=True)

# if __name__ == "__main__":
#     main(sys.argv)