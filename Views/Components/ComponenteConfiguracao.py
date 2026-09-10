import os
import streamlit as st

class ComponenteConfiguracao:
    def renderizar_cabecalho(self):
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

    def renderizar_info_destinatarios(self, emails: dict):
        if not emails or not emails.get("para"):
            return

        str_para = ", ".join(emails["para"])
        str_cc = ", ".join(emails["copia"]) if emails.get("copia") else "Nenhum"
        
        st.info(f"Para: {str_para} | CC: {str_cc}")
        st.divider()