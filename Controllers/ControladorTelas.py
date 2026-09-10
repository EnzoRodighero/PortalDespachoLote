from Models.GerenciadorDeSessao import GerenciadorDeSessao
from Views.Interface import Interface

class ControladorTelas:
    def __init__(self):
        self.sessao = GerenciadorDeSessao()
        self.interface = Interface()

    def exibir_resumo(self):
        self.interface.configurar_pagina()
        processo = self.sessao.obter('ultimo_processo')
        
        if self.sessao.obter('erros_envios') == 0:
            self.interface.renderizar_cabecalho_resumo_sucesso(processo)
        else:
            self.interface.renderizar_cabecalho_resumo_falha(processo)
            
        self.interface.renderizar_metricas_resumo(
            self.sessao.obter('total_envios'),
            self.sessao.obter('sucessos_envios'),
            self.sessao.obter('erros_envios')
        )
        
        for log in self.sessao.obter('log_sucesso'):
            if log['sucesso']:
                self.interface.renderizar_item_log_sucesso(log['ref'])
            else:
                self.interface.renderizar_item_log_erro(log['ref'], log['erro'])
                
        if self.interface.renderizar_rodape_resumo():
            chave_atual = self.sessao.obter('chave_uploader', 0)
            self.sessao.limpar()
            self.sessao.salvar('chave_uploader', chave_atual + 1)
            self.sessao.reiniciar_pagina()