import sys
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from setting import Base
from setting import ENGINE

class tokenType(Base):
    """
    tokenTypeモデル
    """
    __tablename__ = 'tokenType'
    id = Column('id', Integer, primary_key = True)
    tokenType = Column('tokenType', String(100),)
    tokenType = relationship("user")
    tokenType = relationship("token")

def main(args):
    """
    メイン関数
    """
    Base.metadata.create_all(bind=ENGINE, checkfirst=True)

if __name__ == "__main__":
    main(sys.argv)