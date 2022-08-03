import sys
import user
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from setting import Base
from setting import ENGINE

class activity_summary(Base):
    """
    activity_summary
    """
    __tablename__ = 'activity_summary'
    id = Column('id', Integer, primary_key = True)
    user_id = Column('user_id',ForeignKey("user.id"),unique=True)
    day = Column('day',DateTime)
    total_activity_calory = Column('total_activity_calory',Integer)
def main(args):
    """
    メイン関数
    """
    Base.metadata.create_all(bind=ENGINE, checkfirst=True)

if __name__ == "__main__":
    main(sys.argv)