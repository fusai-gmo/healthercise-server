import sys
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from setting import Base
from setting import ENGINE

class activityList(Base):
    """
    activityListモデル
    """
    __tablename__ = 'activityList'
    id = Column('id', Integer, primary_key = True)
    token = Column('level', String(300))
    activityStrength = Column('activityStrength', ForeignKey('activityLevel.id',onupdate='CASCADE', ondelete='CASCADE'))
    activityName = Column('activityName', String(100) )
    activityCalory = Column('activityCalory', Integer )

def main(args):
    """
    メイン関数
    """
    Base.metadata.create_all(bind=ENGINE, checkfirst=True)

if __name__ == "__main__":
    main(sys.argv)