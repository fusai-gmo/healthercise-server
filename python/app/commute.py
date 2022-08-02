import sys
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey,Boolean, Time
from setting import Base
from setting import ENGINE

class commute(Base):
    """
    commuteモデル
    """
    __tablename__ = 'commute'
    id = Column('id', Integer, primary_key = True)
    commuteStartTime = Column( 'commuteStartTime', Time)
    commuteFinishTime = Column( 'commuteFinishTime', Time)
    isCommute = Column('isCommute', Boolean)

def main(args):
    """
    メイン関数
    """
    Base.metadata.create_all(bind=ENGINE, checkfirst=True)

if __name__ == "__main__":
    main(sys.argv)