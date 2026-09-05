import pandas as pd
import os

class DAL:
    def __init__(self, caminho_arquivo="planilha_mestre.xlsx"):
        self.caminho_arquivo = caminho_arquivo
        self.dados = None
        self._carregar_dados()

    def _carregar_dados(self):
        if os.path.exists(self.caminho_arquivo):
            self.dados = pd.read_excel(self.caminho_arquivo)

    def buscar_operacao(self, id_operacao):
        if self.dados is None:
            raise FileNotFoundError("Planilha mestre não encontrada.")
            
        linha = self.dados[self.dados['ID_Operacao'] == id_operacao]
        if linha.empty:
            return None
        return linha.iloc[0].to_dict()
