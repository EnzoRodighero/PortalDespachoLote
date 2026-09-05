import re

class AgrupadorDocumentos:
    def __init__(self, padrao=r'AUD-\d{5}'):
        self.padrao = padrao

    def agrupar(self, arquivos):
        lotes_validos = {}
        erros = []
        
        for arquivo in arquivos:
            resultado = re.search(self.padrao, arquivo.name)
            if not resultado:
                erros.append(f"❌ '{arquivo.name}': ID não localizado no nome do arquivo.")
                continue
            
            referencia = resultado.group(0)
            lotes_validos.setdefault(referencia, []).append(arquivo)
                
        return lotes_validos, erros

    def remover_duplicatas(self, arquivos_brutos):
        nomes_vistos = set()
        arquivos_unicos = []
        nomes_duplicados = []
        
        for arquivo in arquivos_brutos:
            if arquivo.name not in nomes_vistos:
                nomes_vistos.add(arquivo.name)
                arquivos_unicos.append(arquivo)
            else:
                if arquivo.name not in nomes_duplicados:
                    nomes_duplicados.append(arquivo.name)
                    
        return arquivos_unicos, nomes_duplicados

    def consolidar_dados(self, lotes, banco_dados, notificador, processo, str_para, str_cc):
        dados_consolidados = {}
        erros_banco = []

        for ref, arquivos_lote in lotes.items():
            dados = banco_dados.buscar_operacao(ref)
            
            if dados:
                dados_consolidados[ref] = {
                    'arquivos': arquivos_lote,
                    'dados': dados,
                    'padroes': {
                        'para': str_para,
                        'cc': str_cc,
                        'assunto': notificador.montar_assunto_padrao(dados, processo),
                        'texto': notificador.montar_corpo_padrao(dados, processo)
                    }
                }
            else:
                erros_banco.append(f"A operação {ref} não foi encontrada na base de dados.")
                
        return dados_consolidados, erros_banco
