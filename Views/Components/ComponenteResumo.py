import streamlit as st

class ComponenteResumo:
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