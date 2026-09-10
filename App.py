from Models.GerenciadorDeSessao import GerenciadorDeSessao
from Controllers.ControladorTelas import ControladorTelas
from Controllers.ControladorDespacho import ControladorDespacho

def main():
    sessao = GerenciadorDeSessao()
    
    if not sessao.existe('ultimo_processo'):
        sessao.salvar('ultimo_processo', None)
        sessao.salvar('ultima_entidade', None)
        sessao.salvar('versao_formulario', 0)
        
    if not sessao.existe('chave_uploader'):
        sessao.salvar('chave_uploader', 0)

    if sessao.obter('tela_atual') == 'resumo':
        controlador = ControladorTelas()
        controlador.exibir_resumo()
    else:
        controlador = ControladorDespacho()
        controlador.iniciar_fluxo_operacional()

if __name__ == "__main__":
    main()