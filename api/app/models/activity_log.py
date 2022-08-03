import sys
import models.user
import models.activity
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from setting import Base
from setting import ENGINE

class activity_log(Base):
    """
    activity_log
    """
    __tablename__ = 'activity_log'
    id = Column('id', Integer, primary_key = True, autoincrement=True)
    user_id = Column('user_id',ForeignKey("user.id"),unique=True)
    activity_id = Column('activity_id',ForeignKey("activity.id"))
    suggest_start_time = Column( 'suggest_start_time', DateTime)
    suggest_finish_time = Column( 'suggest_finish_time', DateTime)

# def main(args):
#     """
#     メイン関数
#     """
#     Base.metadata.create_all(bind=ENGINE, checkfirst=True)

# if __name__ == "__main__":
#     main(sys.argv)