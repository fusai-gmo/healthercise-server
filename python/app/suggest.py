import sys
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from setting import Base
from setting import ENGINE
import DateTime

class suggest(Base):
    """
    suggestモデル
    """
    __tablename__ = 'activityLevel'
    id = Column('id', Integer, primary_key = True)
    suggestStartTime = Column( 'suggestStartTime', DateTime)
    suggestFinishTime = Column( 'suggestFinishTime', DateTime)

def main(args):
    """
    メイン関数
    """
    Base.metadata.create_all(bind=ENGINE, checkfirst=True)

if __name__ == "__main__":
    main(sys.argv)