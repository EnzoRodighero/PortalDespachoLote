from Models.DAL.DalConfiguracoesSmtp import DalConfiguracoesSmtp
from Models.ServicoEmail import ServicoEmail

class ControladorEmail:
    def __init__(self, modo_simulacao=True):
        self.dal_smtp = DalConfiguracoesSmtp()
        smtp_config = self.dal_smtp.obter_credenciais()

        self.notificador = ServicoEmail(
            servidor_smtp=smtp_config.get("server", ""),
            porta=smtp_config.get("port", 587),
            email_remetente=smtp_config.get("email", ""),
            senha=smtp_config.get("password", ""),
            modo_simulacao=modo_simulacao
        )

    def obter_servico(self):
        return self.notificador

    def executar_disparo(self, lotes, processo, versao, dal, sessao, interface):
        erros_validacao = []
        
        for referencia in lotes.keys():
            para_final = sessao.obter(f"para_{referencia}_v{versao}", "")
            cc_final = sessao.obter(f"cc_{referencia}_v{versao}", "")
            
            valido_para, msg_para = self.notificador.validar_formato_emails(para_final, obrigatorio=True)
            valido_cc, msg_cc = self.notificador.validar_formato_emails(cc_final, obrigatorio=False)
            
            if not valido_para or not valido_cc:
                msgs = msg_para + msg_cc
                erros_validacao.append(f"Operação {referencia}: {', '.join(msgs)}")

        if erros_validacao:
            sessao.salvar('enviando_agora', False)
            interface.renderizar_erros_validacao_destinatarios(erros_validacao)
            return 

        barra, texto_status = interface.obter_elementos_progresso()
        total = len(lotes)
        registros_log = [] 
        
        for i, (referencia, arquivos) in enumerate(lotes.items()):
            interface.atualizar_status_progresso(texto_status, f"Enviando e-mail {i+1} de {total} (Operação: {referencia})...")
            
            dados = dal.buscar_operacao(referencia)
            para_final = sessao.obter(f"para_{referencia}_v{versao}", "")
            cc_final = sessao.obter(f"cc_{referencia}_v{versao}", "")
            assunto_final = sessao.obter(f"assunto_{referencia}_v{versao}", "")
            corpo_final = sessao.obter(f"editor_{referencia}_v{versao}", "")

            if dados:
                sucesso, erro_msg = self.notificador.enviar(
                    referencia, dados, processo, assunto_final, corpo_final, para_final, cc_final, arquivos
                )
                registros_log.append({
                    'ref': referencia,
                    'sucesso': sucesso,
                    'erro': erro_msg
                })
            
            barra.progress((i + 1) / total)

        sessao.salvar('log_sucesso', registros_log)
        sessao.salvar('total_envios', len(registros_log))
        sucessos = sum(1 for l in registros_log if l['sucesso'])
        sessao.salvar('sucessos_envios', sucessos)
        sessao.salvar('erros_envios', len(registros_log) - sucessos)
        
        sessao.salvar('tela_atual', 'resumo')
        sessao.reiniciar_pagina()