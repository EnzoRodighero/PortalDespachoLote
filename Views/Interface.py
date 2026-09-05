import streamlit as st
import base64
import os

class Interface:
    def configurar_pagina(self):
        st.set_page_config(page_title="Portal de Despacho em Lote", layout="wide")
        st.title("Portal de Despacho em Lote")
        st.divider()

    def renderizar_area_de_testes(self):
        st.info("💡 **Dica para testes:** Para avaliar o sistema, baixe o pacote abaixo, extraia no seu computador e arraste os PDFs para a caixa de upload.")
        caminho_zip = "pacote_de_teste.zip"
        if os.path.exists(caminho_zip):
            with open(caminho_zip, "rb") as arquivo_zip:
                st.download_button(
                    label="Baixar Pacote de PDFs para Teste",
                    data=arquivo_zip,
                    file_name="pacote_de_teste.zip",
                    mime="application/zip"
                )
        else:
            st.warning("O arquivo 'pacote_de_teste.zip' ainda não foi carregado no repositório.")
        st.divider()

    def renderizar_sucesso_base(self):
        st.success("✅ Base de dados conectada e PDFs de teste prontos para uso.")

    def renderizar_configuracoes(self, lista_entidades, on_change_callback):
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("1. Tipo de Processo")
            processo = st.selectbox(
                "Processo", 
                ["Relatório Financeiro", "Auditoria Geral"], 
                on_change=on_change_callback,
                label_visibility="collapsed"
            )
        with c2:
            st.subheader("2. Departamento")
            entidade = st.selectbox(
                "Departamento", 
                lista_entidades, 
                on_change=on_change_callback,
                label_visibility="collapsed"
            )
        return processo, entidade

    def renderizar_info_destinatarios(self, texto):
        st.info(texto)
        st.divider()

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

    def renderizar_card_operacao(self, ref, cliente, arquivos, padroes, versao):
        titulo = f"Operação: {ref} | Cliente: {cliente} | {len(arquivos)} Anexo(s)"
        
        with st.expander(titulo):
            st.markdown("**Arquivos Anexados:**")
            nomes_arquivos = [f"`{arq.name}`" for arq in arquivos]
            st.markdown(" | ".join(nomes_arquivos))
            
            with st.expander("Visualizar Documentos (PDF)"):
                abas = st.tabs([arq.name for arq in arquivos])
                for aba, arq in zip(abas, arquivos):
                    with aba:
                        base64_pdf = base64.b64encode(arq.getvalue()).decode('utf-8')
                        pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="500" type="application/pdf"></iframe>'
                        st.markdown(pdf_display, unsafe_allow_html=True)
            
            st.markdown("---")
            st.markdown("**Destinatários:**")
            c_para, c_cc = st.columns(2)
            
            with c_para:
                st.text_input("Para (separe por vírgula):", value=padroes['para'], key=f"para_{ref}_v{versao}")
            with c_cc:
                st.text_input("CC (separe por vírgula):", value=padroes['cc'], key=f"cc_{ref}_v{versao}")
            
            st.markdown("---")
            st.text_input("Assunto do E-mail:", value=padroes['assunto'], key=f"assunto_{ref}_v{versao}")
            st.text_area("Corpo do E-mail:", value=padroes['texto'], height=700, key=f"editor_{ref}_v{versao}")

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

    def renderizar_cabecalho_resumo_sucesso(self, processo):
        st.success(f"✅ Processo de **{processo}** concluído sem erros.")

    def renderizar_cabecalho_resumo_falha(self, processo):
        st.warning(f"⚠️ Processo de **{processo}** concluído com falhas de comunicação.")

    def renderizar_metricas_resumo(self, total, sucessos, erros):
        st.subheader("Resumo Executivo dos Disparos")
        c1, c2, c3 = st.columns(3)
        c1.metric("Total de Envios", total)
        c2.metric("✅ Sucesso", sucessos)
        c3.metric("❌ Falhas", erros)
        st.markdown("<br>", unsafe_allow_html=True)

    def renderizar_item_log_sucesso(self, ref):
        st.markdown(f"✅ **Operação {ref}** enviada com sucesso.")

    def renderizar_item_log_erro(self, ref, erro):
        st.error(f"❌ **Operação {ref}** falhou. (Motivo: {erro})")

    def renderizar_rodape_resumo(self):
        st.divider()
        return st.button("Iniciar Novo Lote", type="primary", use_container_width=True)

    def renderizar_erros_validacao_destinatarios(self, erros_validacao):
        st.error("❌ O disparo foi cancelado por falha na validação dos destinatários.")
        for erro in erros_validacao:
            st.warning(erro)
