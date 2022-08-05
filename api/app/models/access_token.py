import sys
import models.user
import models.token_type
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from setting import Base
from setting import ENGINE

class access_token(Base):
    """
    access_tokenモデル
    """
    __tablename__ = 'access_token'
    id = Column('id', Integer, primary_key = True, autoincrement=True)
    user_id = Column('user_id', Integer)
    token_type_id = Column('token_type_id', ForeignKey('token_type.id'))
    token = Column('token', String(300))

# def main(args):
#     """
#     メイン関数
#     """
#     Base.metadata.create_all(bind=ENGINE, checkfirst=True)

# if __name__ == "__main__":
#     main(sys.argv)