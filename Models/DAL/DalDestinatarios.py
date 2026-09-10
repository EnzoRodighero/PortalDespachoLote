import json

class DalDestinatarios:
    def __init__(self, caminho_arquivo="contatos.json"):
        self.caminho_arquivo = caminho_arquivo

    def listar_entidades(self):
        try:
            with open(self.caminho_arquivo, 'r', encoding='utf-8') as file:
                return list(json.load(file).keys())
        except Exception:
            return []

    def buscar_emails(self, entidade):
        try:
            with open(self.caminho_arquivo, 'r', encoding='utf-8') as file:
                contatos = json.load(file)
            return contatos.get(entidade, {"para": [], "copia": []})
        except Exception:
            return {"para": [], "copia": []}