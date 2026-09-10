from pathlib import Path
import tomllib
import streamlit as st

class DalConfiguracoesSmtp:
    
    def __init__(self, caminho_exemplo: str = ".streamlit/secrets.example.toml"):
        self.caminho_exemplo = Path(caminho_exemplo)

    def obter_credenciais(self) -> dict:
        try:
            return dict(st.secrets["smtp"])
        except Exception:
            if self.caminho_exemplo.exists():
                with open(self.caminho_exemplo, "rb") as f:
                    dados = tomllib.load(f)
                    return dados.get("smtp", {})
            return {}