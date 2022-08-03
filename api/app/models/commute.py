import sys
import models.user
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey,Boolean, Time
from setting import Base
from setting import ENGINE

class commute(Base):
    """
    commuteモデル
    """
    __tablename__ = 'commute'
    id = Column('id', Integer, primary_key = True, autoincrement=True)
    user_id = Column('user_id', ForeignKey("user.id"))
    commute_start_time = Column( 'commute_start_time', Time)
    commute_finish_time = Column( 'commute_finish_time', Time)
    commute_is_activity = Column( 'commute_is_activity', Boolean)
    isCommute = Column('is_commute', Boolean)

# def main(args):
#     """
#     メイン関数
#     """
#     Base.metadata.create_all(bind=ENGINE, checkfirst=True)

# if __name__ == "__main__":
#     main(sys.argv)