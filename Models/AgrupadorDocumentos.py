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

    def consolidar_dados(self, lotes, dal, dal_templates, processo, str_para, str_cc):
        dados_consolidados = {}
        erros_banco = []
        
        template_bruto = dal_templates.obter_template_bruto(processo)
        texto_assunto = template_bruto.get("assunto", "[{tipo_processo}] Operação: {ID_Operacao} | Cliente: {Cliente}")
        texto_corpo = template_bruto.get("corpo", "Prezado(a),\n\nSegue a documentação do processo: {tipo_processo}.")
        
        for ref, arquivos in lotes.items():
            dados = dal.buscar_operacao(ref)
            
            if not dados:
                erros_banco.append(f"Arquivo sem correspondência no banco de dados. Ref: {ref}")
                continue
                
            contexto = dados.copy()
            contexto["tipo_processo"] = processo
            
            try:
                assunto_formatado = texto_assunto.format(**contexto)
                corpo_formatado = texto_corpo.format(**contexto)
            except KeyError as e:
                assunto_formatado = texto_assunto
                corpo_formatado = texto_corpo
                erros_banco.append(f"Aviso: Variável {e} ausente na planilha para a operação {ref}.")

            dados_consolidados[ref] = {
                'dados': dados,
                'arquivos': arquivos,
                'padroes': {
                    'para': str_para,
                    'cc': str_cc,
                    'assunto': assunto_formatado,
                    'texto': corpo_formatado,
                    'editor': corpo_formatado
                }
            }
            
        return dados_consolidados, erros_banco

    def processar_arquivos_brutos(self, arquivos_brutos, dal_planilha, dal_templates, processo, emails):
        if len(arquivos_brutos) > 15:
            return None, None, None, ["O limite máximo é de 15 arquivos por lote."]

        arquivos_unicos, nomes_duplicados = self.remover_duplicatas(arquivos_brutos)
        
        dal_planilha._carregar_dados()
        lotes, erros_agrupamento = self.agrupar(arquivos_unicos)
        
        str_para = ", ".join(emails.get("para", []))
        str_cc = ", ".join(emails.get("copia", []))
        
        dados_consolidados, erros_banco = self.consolidar_dados(
            lotes, dal_planilha, dal_templates, processo, str_para, str_cc
        )

        erros_totais = erros_agrupamento + erros_banco
        return dados_consolidados, lotes, nomes_duplicados, erros_totais
