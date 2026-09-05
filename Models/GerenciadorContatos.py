import json
import os

class GerenciadorContatos:
    def __init__(self, caminho_arquivo="contatos.json"):
        self.caminho_arquivo = caminho_arquivo
        self.contatos = {"Selecione...": {"para": [], "copia": []}}
        
        if os.path.exists(self.caminho_arquivo):
            with open(self.caminho_arquivo, "r", encoding="utf-8") as arquivo:
                self.contatos = json.load(arquivo)

    def listar_entidades(self):
        return list(self.contatos.keys())

    def buscar_emails(self, entidade):
        return self.contatos.get(entidade, {"para": [], "copia": []})