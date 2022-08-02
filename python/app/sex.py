import sys
import user
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from setting import Base
from setting import ENGINE

class sex(Base):
    """
    sexモデル
    """
    __tablename__ = 'sex'
    id = Column('id', Integer, primary_key = True)
    user_id = Column('user_id', ForeignKey("user.id"))
    sex = Column('sex', String(10))


def main(args):
    """
    メイン関数
    """
    Base.metadata.create_all(bind=ENGINE, checkfirst=True)

if __name__ == "__main__":
    main(sys.argv)