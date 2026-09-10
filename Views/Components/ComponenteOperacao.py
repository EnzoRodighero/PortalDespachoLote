import base64
import streamlit as st

class ComponenteOperacao:
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