from fastapi import FastAPI, Depends, HTTPException, status, UploadFile, File
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.middleware.cors import CORSMiddleware
import secrets
import pandas as pd
from io import BytesIO
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from models import DataRow
from crud import clear_data, insert_data

app = FastAPI()

# CORS para permitir frontend local e remoto
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ajuste depois para domínio específico
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

security = HTTPBasic()

# Login e senha fixos (troque aqui)
USER = "usuario"
PASSWORD = "senha123"

# Dependency para DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def verify_credentials(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, USER)
    correct_password = secrets.compare_digest(credentials.password, PASSWORD)
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário ou senha incorretos",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

@app.get("/")
def read_root():
    return {"message": "API Geocodificador funcionando!"}

@app.post("/upload-excel")
def upload_excel(
    file: UploadFile = File(...),
    username: str = Depends(verify_credentials),
    db: Session = Depends(get_db)
):
    if not file.filename.endswith((".xls", ".xlsx")):
        raise HTTPException(status_code=400, detail="Arquivo deve ser Excel (.xls ou .xlsx)")
    content = file.file.read()
    df = pd.read_excel(BytesIO(content))

    # Apaga dados antigos e insere novos
    clear_data(db)
    insert_data(db, df)

    return {"message": f"Arquivo {file.filename} importado com sucesso!", "rows": len(df)}

