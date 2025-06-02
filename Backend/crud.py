from sqlalchemy.orm import Session
from models import DataRow

def clear_data(db: Session):
    db.query(DataRow).delete()
    db.commit()

def insert_data(db: Session, df):
    for _, row in df.iterrows():
        data = DataRow(
            latitude=str(row.get("latitude", "")),
            longitude=str(row.get("longitude", "")),
            # Adapte para outras colunas do seu Excel aqui
        )
        db.add(data)
    db.commit()
