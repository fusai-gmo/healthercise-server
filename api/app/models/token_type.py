import sys
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from setting import Base
from setting import ENGINE

class token_type(Base):
    """
    token_typeモデル
    """
    __tablename__ = 'token_type'
    id = Column('id', Integer, primary_key = True, autoincrement=True)
    token_type = Column('token_type', String(100),)

# def main(args):
#     """
#     メイン関数
#     """
#     Base.metadata.create_all(bind=ENGINE, checkfirst=True)

# if __name__ == "__main__":
#     main(sys.argv)