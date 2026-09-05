import time
import smtplib
import re
import json
import os
from email.message import EmailMessage
import streamlit as st

class ServicoEmail:
    def __init__(self, modo_simulacao=True, caminho_templates="templates_email.json"):
        self.modo_simulacao = modo_simulacao
        self.templates = self._carregar_templates(caminho_templates)

    def _carregar_templates(self, caminho):
        if os.path.exists(caminho):
            with open(caminho, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            st.warning(f"Aviso: Arquivo de templates '{caminho}' não encontrado. Usando fallback.")
            return {}

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

    def montar_assunto_padrao(self, dados, tipo_processo):
        template = self.templates.get(tipo_processo, {}).get(
            "assunto", 
            "[{tipo_processo}] Operação: {ID_Operacao} | Cliente: {Cliente}"
        )
        
        contexto = dados.copy()
        contexto["tipo_processo"] = tipo_processo
        
        return template.format(**contexto)

    def montar_corpo_padrao(self, dados, tipo_processo):
        template = self.templates.get(tipo_processo, {}).get(
            "corpo", 
            "Prezado(a) {Gerente_Responsavel},\n\nSegue a documentação do processo: {tipo_processo}."
        )
        
        contexto = dados.copy()
        contexto["tipo_processo"] = tipo_processo
        
        return template.format(**contexto)

    def enviar(self, id_operacao, dados, tipo_processo, assunto_texto, corpo_texto, para_final, cc_final, anexos):
        if self.modo_simulacao:
            time.sleep(1)
            return True, ""
            
        try:
            msg = EmailMessage()
            msg['Subject'] = assunto_texto
            msg['From'] = st.secrets["smtp"]["email"]
            msg['To'] = para_final
            
            if cc_final.strip(): 
                msg['Cc'] = cc_final
            
            msg.set_content(corpo_texto)

            for arquivo in anexos:
                msg.add_attachment(arquivo.getvalue(), maintype='application', subtype='pdf', filename=arquivo.name)

            with smtplib.SMTP(st.secrets["smtp"]["server"], st.secrets["smtp"]["port"]) as server:
                server.starttls()
                server.login(st.secrets["smtp"]["email"], st.secrets["smtp"]["password"])
                server.send_message(msg)
                
            return True, "" 

        except Exception as e:
            return False, str(e)
