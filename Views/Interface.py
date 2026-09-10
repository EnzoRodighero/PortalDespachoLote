import streamlit as st
from Views.Components.ComponenteConfiguracao import ComponenteConfiguracao
from Views.Components.ComponenteOperacao import ComponenteOperacao
from Views.Components.ComponenteResumo import ComponenteResumo

class Interface:
    def __init__(self):
        self.comp_configuracao = ComponenteConfiguracao()
        self.comp_operacao = ComponenteOperacao()
        self.comp_resumo = ComponenteResumo()

    def configurar_pagina(self):
        self.comp_configuracao.renderizar_cabecalho()

    def renderizar_area_de_testes(self):
        self.comp_configuracao.renderizar_area_de_testes()

    def renderizar_configuracoes(self, lista_entidades, on_change_callback):
        return self.comp_configuracao.renderizar_configuracoes(lista_entidades, on_change_callback)

    def renderizar_info_destinatarios(self, emails: dict):
        self.comp_configuracao.renderizar_info_destinatarios(emails)

    def renderizar_card_operacao(self, ref, cliente, arquivos, padroes, versao):
        self.comp_operacao.renderizar_card_operacao(ref, cliente, arquivos, padroes, versao)

    def renderizar_cabecalho_resumo_sucesso(self, processo):
        self.comp_resumo.renderizar_cabecalho_resumo_sucesso(processo)

    def renderizar_cabecalho_resumo_falha(self, processo):
        self.comp_resumo.renderizar_cabecalho_resumo_falha(processo)

    def renderizar_metricas_resumo(self, total, sucessos, erros):
        self.comp_resumo.renderizar_metricas_resumo(total, sucessos, erros)

    def renderizar_item_log_sucesso(self, ref):
        self.comp_resumo.renderizar_item_log_sucesso(ref)

    def renderizar_item_log_erro(self, ref, erro):
        self.comp_resumo.renderizar_item_log_erro(ref, erro)

    def renderizar_rodape_resumo(self):
        return self.comp_resumo.renderizar_rodape_resumo()

    def renderizar_upload(self, chave_uploader):
        st.subheader("3. Anexar Arquivos (PDF)")
        return st.file_uploader(
            "Arraste os documentos | ⚠️ MÁXIMO DE 15 ARQUIVOS:", 
            accept_multiple_files=True, 
            type=["pdf"],
            key=f"uploader_v{chave_uploader}"
        )

    def renderizar_erro_limite_arquivos(self):
        st.error("❌ Limite excedido: você pode enviar no máximo 15 arquivos PDF por lote. O processo foi interrompido por segurança.")

    def renderizar_aviso_duplicatas(self, nomes_duplicados):
        lista_nomes = ", ".join([f"**{nome}**" for nome in nomes_duplicados])
        st.warning(f"⚠️ **Nota:** Os seguintes arquivos foram ignorados pois já foram anexados: {lista_nomes}.")

    def renderizar_botao_limpar(self):
        return st.button("Limpar Todos os Anexos", type="secondary")

    def renderizar_cabecalho_previa(self):
        st.divider()
        st.subheader("Relatório e Revisão de E-mails")
        st.markdown("*Clique nas operações abaixo para revisar os anexos, destinatários e textos antes do disparo.*")

    def renderizar_alertas_incompatibilidade(self, erros):
        with st.expander("⚠️ Alertas de Incompatibilidade", expanded=True):
            for erro in erros:
                st.warning(erro)

    def renderizar_erros_validacao_destinatarios(self, erros_validacao):
        st.error("❌ O disparo foi cancelado por falha na validação dos destinatários.")
        for erro in erros_validacao:
            st.warning(erro)

    def renderizar_erro_nenhuma_operacao(self):
        st.error("❌ Nenhuma operação válida para envio.")

    def renderizar_sucesso_contagem_previa(self, quantidade):
        st.success(f"✅ {quantidade} operações prontas para envio.")

    def renderizar_confirmacao_final(self, processo):
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(
            f"⚠️ **Atenção:** Você está prestes a disparar este lote referente ao processo de "
            f"<span style='color: #D4AF37; font-weight: bold; font-size: 1.1em;'>{processo}</span>.", 
            unsafe_allow_html=True
        )
        return st.checkbox("Confirmo que revisei os dados, os anexos e desejo iniciar o envio em lote.")

    def renderizar_botao_disparo(self, habilitado):
        espaco_botao = st.empty()
        clicou = espaco_botao.button("Executar Disparo em Lote", type="primary", use_container_width=True, disabled=not habilitado)
        
        if clicou:
            espaco_botao.button("Enviando E-mails...", type="primary", use_container_width=True, disabled=True)
        return clicou

    def obter_elementos_progresso(self):
        return st.progress(0), st.empty()
        
    def atualizar_status_progresso(self, elemento_texto, mensagem):
        elemento_texto.text(mensagem)