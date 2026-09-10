from Models.DAL.DalPlanilhaMestre import DalPlanilhaMestre
from Models.DAL.DalTemplateEmails import DalTemplateEmails
from Models.DAL.DalDestinatarios import DalDestinatarios
from Models.AgrupadorDocumentos import AgrupadorDocumentos
from Models.GerenciadorDeSessao import GerenciadorDeSessao
from Views.Interface import Interface
from Controllers.ControladorEmail import ControladorEmail

class ControladorDespacho:
    def __init__(self):
        self.dal = DalPlanilhaMestre()
        self.dal_templates = DalTemplateEmails()
        self.contatos = DalDestinatarios()

        self.agrupador = AgrupadorDocumentos()
        self.interface = Interface()
        self.sessao = GerenciadorDeSessao()

        self.ctrl_email = ControladorEmail(modo_simulacao=True)

    def iniciar_fluxo_operacional(self):
        self.interface.configurar_pagina()
        self.interface.renderizar_area_de_testes()

        processo, entidade = self.interface.renderizar_configuracoes(
            self.contatos.listar_entidades(), 
            self.sessao.resetar_memoria_formulario
        )
        self.sessao.sincronizar_contexto(processo, entidade)

        emails = self.contatos.buscar_emails(entidade)
        self.interface.renderizar_info_destinatarios(emails)
        
        arquivos_brutos = self.interface.renderizar_upload(self.sessao.obter('chave_uploader'))
        if not arquivos_brutos:
            return

        if self.interface.renderizar_botao_limpar():
            self.sessao.limpar_uploader()

        dados_consolidados, lotes, nomes_duplicados, erros_totais = self.agrupador.processar_arquivos_brutos(
            arquivos_brutos, self.dal, self.dal_templates, processo, emails
        )

        if nomes_duplicados:
            self.interface.renderizar_aviso_duplicatas(nomes_duplicados)

        self.interface.renderizar_cabecalho_previa()

        if erros_totais:
            self.interface.renderizar_alertas_incompatibilidade(erros_totais)

        if not dados_consolidados:
            self.interface.renderizar_erro_nenhuma_operacao()
            return

        self.interface.renderizar_sucesso_contagem_previa(len(dados_consolidados))
        versao_form = self.sessao.obter('versao_formulario')

        for ref, info in dados_consolidados.items():
            self.interface.renderizar_card_operacao(
                ref, 
                info['dados'].get('Cliente', ''), 
                info['arquivos'], 
                info['padroes'], 
                versao_form
            )
        
        usuario_confirmou = self.interface.renderizar_confirmacao_final(processo)
        if self.interface.renderizar_botao_disparo(habilitado=usuario_confirmou):
            self.ctrl_email.executar_disparo(
                lotes=lotes, 
                processo=processo, 
                versao=versao_form, 
                dal=self.dal, 
                sessao=self.sessao, 
                interface=self.interface
            )