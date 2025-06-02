from sqlalchemy import Column, Integer, String
from database import Base

class DataRow(Base):
    __tablename__ = "data_rows"

    id = Column(Integer, primary_key=True, index=True)
    latitude = Column(String, index=True)
    longitude = Column(String, index=True)
    # Você pode ajustar as colunas de acordo com o Excel
    # Exemplo:
    # other_field = Column(String, index=True)
