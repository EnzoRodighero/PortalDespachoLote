import streamlit as st

class GerenciadorDeSessao:
    def obter(self, chave, padrao=None):
        return st.session_state.get(chave, padrao)

    def salvar(self, chave, valor):
        st.session_state[chave] = valor

    def existe(self, chave):
        return chave in st.session_state

    def deletar(self, chave):
        if chave in st.session_state:
            del st.session_state[chave]

    def limpar(self):
        st.session_state.clear()

    def reiniciar_pagina(self):
        st.rerun()
        
    def listar_chaves(self):
        return list(st.session_state.keys())
