import sys
import models.user
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from setting import Base
from setting import ENGINE

class activity_level(Base):
    """
    activity_levelモデル
    """
    __tablename__ = 'activity_level'
    id = Column('id', Integer, primary_key = True, autoincrement=True)
    user_id = Column('user_id', ForeignKey("user.id"))
    level = Column('level', String(300))


# def main(args):
#     """
#     メイン関数
#     """
#     Base.metadata.create_all(bind=ENGINE, checkfirst=True)

# if __name__ == "__main__":
#     main(sys.argv)