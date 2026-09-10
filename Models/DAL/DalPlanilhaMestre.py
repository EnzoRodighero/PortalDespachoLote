import pandas as pd

class DalPlanilhaMestre:
    def __init__(self, caminho_arquivo="planilha_mestre.xlsx"):
        self.caminho_arquivo = caminho_arquivo
        self.dados = None

    def _carregar_dados(self):
        try:
            df = pd.read_excel(self.caminho_arquivo)
            self.dados = df.to_dict('records')
        except Exception:
            self.dados = []

    def obter_dados_operacionais(self):
        if self.dados is None:
            self._carregar_dados()
        return self.dados

    def buscar_operacao(self, referencia):
        if self.dados is None:
            self._carregar_dados()
        for linha in self.dados:
            if str(linha.get('ID_Operacao', linha.get('Pedido', ''))) == str(referencia):
                return linha
        return None