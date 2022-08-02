import sys
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from setting import Base
from setting import ENGINE

class accessToken(Base):
    """
    accessTokenモデル
    """
    __tablename__ = 'accessToken'
    id = Column('id', Integer, primary_key = True)
    tokenType = Column('tokenType', String(100))
    token = Column('token', String(300))

def main(args):
    """
    メイン関数
    """
    Base.metadata.create_all(bind=ENGINE, checkfirst=True)

if __name__ == "__main__":
    main(sys.argv)