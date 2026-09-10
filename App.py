from Models.GerenciadorDeSessao import GerenciadorDeSessao
from Controllers.ControladorTelas import ControladorTelas
from Controllers.ControladorDespacho import ControladorDespacho

def main():
    sessao = GerenciadorDeSessao()
    sessao.inicializar_variaveis_padrao()

    if sessao.obter('tela_atual') == 'resumo':
        controlador = ControladorTelas()
        controlador.exibir_resumo()
    else:
        controlador = ControladorDespacho()
        controlador.iniciar_fluxo_operacional()

if __name__ == "__main__":
    main()
