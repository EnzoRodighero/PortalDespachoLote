from Models.DAL import DAL
from Models.AgrupadorDocumentos import AgrupadorDocumentos
from Models.GerenciadorContatos import GerenciadorContatos
from Models.ServicoEmail import ServicoEmail
from Models.GerenciadorDeSessao import GerenciadorDeSessao
from Views.Interface import Interface 

class ControladorPrincipal:
    def __init__(self):
        self.dal = DAL()
        self.agrupador = AgrupadorDocumentos()
        self.contatos = GerenciadorContatos()
        self.notificador = ServicoEmail(modo_simulacao=True)
        self.interface = Interface()
        self.sessao = GerenciadorDeSessao()

        if not self.sessao.existe('ultimo_processo'):
            self.sessao.salvar('ultimo_processo', None)
            self.sessao.salvar('ultima_entidade', None)
            self.sessao.salvar('versao_formulario', 0)
            
        if not self.sessao.existe('chave_uploader'):
            self.sessao.salvar('chave_uploader', 0)

    def resetar_memoria(self):
        chaves = self.sessao.listar_chaves()
        for k in chaves:
            if k.startswith(('para_', 'cc_', 'assunto_', 'editor_')):
                self.sessao.deletar(k)

    def executar(self):
        self.interface.configurar_pagina()
        
        if self.sessao.obter('tela_atual') == 'resumo':
            processo = self.sessao.obter('ultimo_processo')
            
            if self.sessao.obter('erros_envios') == 0:
                self.interface.renderizar_cabecalho_resumo_sucesso(processo)
            else:
                self.interface.renderizar_cabecalho_resumo_falha(processo)
                
            self.interface.renderizar_metricas_resumo(
                self.sessao.obter('total_envios'),
                self.sessao.obter('sucessos_envios'),
                self.sessao.obter('erros_envios')
            )
            
            for log in self.sessao.obter('log_sucesso'):
                if log['sucesso']:
                    self.interface.renderizar_item_log_sucesso(log['ref'])
                else:
                    self.interface.renderizar_item_log_erro(log['ref'], log['erro'])
                    
            if self.interface.renderizar_rodape_resumo():
                chave_atual = self.sessao.obter('chave_uploader', 0)
                self.sessao.limpar()
                self.sessao.salvar('chave_uploader', chave_atual + 1)
                self.sessao.reiniciar_pagina()
            return 
        
        self.interface.renderizar_area_de_testes()

        processo, entidade = self.interface.renderizar_configuracoes(
            self.contatos.listar_entidades(), 
            self.resetar_memoria
        )
        
        if self.sessao.obter('ultimo_processo') != processo or self.sessao.obter('ultima_entidade') != entidade:
            self.sessao.salvar('ultimo_processo', processo)
            self.sessao.salvar('ultima_entidade', entidade)
            versao = self.sessao.obter('versao_formulario')
            self.sessao.salvar('versao_formulario', versao + 1)

        emails = self.contatos.buscar_emails(entidade)
        
        if emails["para"]:
            str_cc = ", ".join(emails["copia"]) if emails["copia"] else "Nenhum"
            texto_info = f"Para: {', '.join(emails['para'])} | CC: {str_cc}"
            self.interface.renderizar_info_destinatarios(texto_info)
        
        arquivos_brutos = self.interface.renderizar_upload(self.sessao.obter('chave_uploader'))

        if arquivos_brutos:
            if self.interface.renderizar_botao_limpar():
                nova_chave = self.sessao.obter('chave_uploader') + 1
                self.sessao.salvar('chave_uploader', nova_chave)
                self.sessao.reiniciar_pagina()

            if len(arquivos_brutos) > 15:
                self.interface.renderizar_erro_limite_arquivos()
                return 

            arquivos_unicos, nomes_duplicados = self.agrupador.remover_duplicatas(arquivos_brutos)
            if nomes_duplicados:
                self.interface.renderizar_aviso_duplicatas(nomes_duplicados)
                
            self.dal._carregar_dados() 
            lotes, erros_agrupamento = self.agrupador.agrupar(arquivos_unicos)
            
            str_para = ", ".join(emails["para"])
            str_cc = ", ".join(emails["copia"]) if emails["copia"] else ""
            
            dados_consolidados, erros_banco = self.agrupador.consolidar_dados(
                lotes, self.dal, self.notificador, processo, str_para, str_cc
            )

            erros_totais = erros_agrupamento + erros_banco

            self.interface.renderizar_cabecalho_previa()

            if erros_totais:
                self.interface.renderizar_alertas_incompatibilidade(erros_totais)

            if not dados_consolidados:
                self.interface.renderizar_erro_nenhuma_operacao()
            else:
                self.interface.renderizar_sucesso_contagem_previa(len(dados_consolidados))
                
                versao_form = self.sessao.obter('versao_formulario')
                for ref, info in dados_consolidados.items():
                    self.interface.renderizar_card_operacao(
                        ref, 
                        info['dados']['Cliente'], 
                        info['arquivos'], 
                        info['padroes'], 
                        versao_form
                    )
                
                usuario_confirmou = self.interface.renderizar_confirmacao_final(processo)
                if self.interface.renderizar_botao_disparo(habilitado=usuario_confirmou):
                    self._executar_disparo(lotes, processo, versao_form)

    def _executar_disparo(self, lotes, processo, versao):
        erros_validacao = []
        
        for referencia in lotes.keys():
            para_final = self.sessao.obter(f"para_{referencia}_v{versao}", "")
            cc_final = self.sessao.obter(f"cc_{referencia}_v{versao}", "")
            
            valido_para, msg_para = self.notificador.validar_formato_emails(para_final, obrigatorio=True)
            valido_cc, msg_cc = self.notificador.validar_formato_emails(cc_final, obrigatorio=False)
            
            if not valido_para or not valido_cc:
                msgs = msg_para + msg_cc
                erros_validacao.append(f"Operação {referencia}: {', '.join(msgs)}")

        if erros_validacao:
            self.sessao.salvar('enviando_agora', False)
            self.interface.renderizar_erros_validacao_destinatarios(erros_validacao)
            return 

        barra, texto_status = self.interface.obter_elementos_progresso()
        total = len(lotes)
        registros_log = [] 
        
        for i, (referencia, arquivos) in enumerate(lotes.items()):
            self.interface.atualizar_status_progresso(texto_status, f"Enviando e-mail {i+1} de {total} (Operação: {referencia})...")
            
            dados = self.dal.buscar_operacao(referencia)
            para_final = self.sessao.obter(f"para_{referencia}_v{versao}", "")
            cc_final = self.sessao.obter(f"cc_{referencia}_v{versao}", "")
            assunto_final = self.sessao.obter(f"assunto_{referencia}_v{versao}", "")
            corpo_final = self.sessao.obter(f"editor_{referencia}_v{versao}", "")

            if dados:
                sucesso, erro_msg = self.notificador.enviar(referencia, dados, processo, assunto_final, corpo_final, para_final, cc_final, arquivos)
                registros_log.append({
                    'ref': referencia,
                    'sucesso': sucesso,
                    'erro': erro_msg
                })
            
            barra.progress((i + 1) / total)

        self.sessao.salvar('log_sucesso', registros_log)
        self.sessao.salvar('total_envios', len(registros_log))
        sucessos = sum(1 for l in registros_log if l['sucesso'])
        self.sessao.salvar('sucessos_envios', sucessos)
        self.sessao.salvar('erros_envios', len(registros_log) - sucessos)
        
        self.sessao.salvar('tela_atual', 'resumo')
        self.sessao.reiniciar_pagina()
