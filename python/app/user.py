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
    id = Column('id', Integer, primary_key = True)
    name = Column('name', String(200))
    age = Column('age', Integer)
    email = Column('email', String(100))
    sex = Column('sex', ForeignKey('sex.id',onupdate='CASCADE', ondelete='CASCADE'))


def main(args):
    """
    メイン関数
    """
    Base.metadata.create_all(bind=ENGINE,checkfirst=True)

if __name__ == "__main__":
    main(sys.argv)