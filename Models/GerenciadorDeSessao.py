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

    def inicializar_variaveis_padrao(self):
        if not self.existe('ultimo_processo'):
            self.salvar('ultimo_processo', None)
            self.salvar('ultima_entidade', None)
            self.salvar('versao_formulario', 0)
            
        if not self.existe('chave_uploader'):
            self.salvar('chave_uploader', 0)
            
        if not self.existe('tela_atual'):
            self.salvar('tela_atual', 'operacional')

    def resetar_memoria_formulario(self):
        chaves = self.listar_chaves()
        for k in chaves:
            if k.startswith(('para_', 'cc_', 'assunto_', 'editor_')):
                self.deletar(k)

    def sincronizar_contexto(self, processo, entidade):
        if self.obter('ultimo_processo') != processo or self.obter('ultima_entidade') != entidade:
            self.salvar('ultimo_processo', processo)
            self.salvar('ultima_entidade', entidade)
            versao = self.obter('versao_formulario', 0)
            self.salvar('versao_formulario', versao + 1)

    def limpar_uploader(self):
        nova_chave = self.obter('chave_uploader', 0) + 1
        self.salvar('chave_uploader', nova_chave)
        self.reiniciar_pagina()
