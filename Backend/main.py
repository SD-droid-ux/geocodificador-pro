from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import pandas as pd
from supabase import create_client, Client

# Carregar variáveis de ambiente
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

app = FastAPI()

# Permitir acesso de qualquer origem (útil para testes locais)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload")
async def upload_excel(file: UploadFile = File(...)):
    if not file.filename.endswith(".xlsx"):
        raise HTTPException(status_code=400, detail="O arquivo deve ser um Excel (.xlsx)")

    try:
        # Ler os dados do Excel para um DataFrame
        df = pd.read_excel(file.file)

        # Validação básica: precisa ter colunas latitude e longitude
        if "latitude" not in df.columns or "longitude" not in df.columns:
            raise HTTPException(status_code=400, detail="O arquivo deve conter colunas 'latitude' e 'longitude'.")

        # Apagar os dados anteriores
        supabase.table("enderecos").delete().neq("id", 0).execute()

        # Inserir os novos dados
        data = df.to_dict(orient="records")
        for row in data:
            supabase.table("enderecos").insert(row).execute()

        return {"status": "sucesso", "linhas_inseridas": len(data)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

