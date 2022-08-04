import sys
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime
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
    name = Column('name', String(200))
    email = Column('email', String(100))
    age = Column('age', Integer)
    height = Column('height', Integer)
    weight = Column('weight', Integer)
    id = relationship('sex')
    

    notify_start_time = Column( 'notify_start_time', Time)
    notify_finish_time = Column( 'notify_finish_time', Time)

# def main(args):
#     """
#     メイン関数
#     """
#     Base.metadata.create_all(bind=ENGINE,checkfirst=True)

# if __name__ == "__main__":
#     main(sys.argv)