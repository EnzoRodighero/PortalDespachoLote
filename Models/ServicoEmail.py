import time
import smtplib
import re
from email.message import EmailMessage

class ServicoEmail:
    def __init__(self, servidor_smtp, porta, email_remetente, senha, modo_simulacao=True):
        self.servidor = servidor_smtp
        self.porta = porta
        self.remetente = email_remetente
        self.senha = senha
        self.modo_simulacao = modo_simulacao

    def validar_formato_emails(self, string_emails, obrigatorio=True):
        if not string_emails.strip():
            if obrigatorio:
                return False, ["O campo não pode estar vazio."]
            return True, [] 
            
        padrao = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        lista_emails = [e.strip() for e in string_emails.split(',') if e.strip()]
        
        invalidos = []
        for email in lista_emails:
            if not re.match(padrao, email):
                invalidos.append(f"E-mail inválido: {email}")
                
        if invalidos:
            return False, invalidos
        return True, []

    def enviar(self, id_operacao, dados, tipo_processo, assunto_texto, corpo_texto, para_final, cc_final, anexos):
        if self.modo_simulacao:
            time.sleep(1)
            return True, ""
            
        try:
            msg = EmailMessage()
            msg['Subject'] = assunto_texto
            msg['From'] = self.remetente
            msg['To'] = para_final
            
            if cc_final.strip(): 
                msg['Cc'] = cc_final
            
            msg.set_content(corpo_texto)

            if anexos:
                for arquivo in anexos:
                    msg.add_attachment(arquivo.getvalue(), maintype='application', subtype='pdf', filename=arquivo.name)

            with smtplib.SMTP(self.servidor, self.porta) as server:
                server.starttls()
                server.login(self.remetente, self.senha)
                server.send_message(msg)
                
            return True, "" 

        except Exception as e:
            return False, str(e)