import json

class DalTemplateEmails:
    def __init__(self, caminho_arquivo="templates_email.json"):
        self.caminho_arquivo = caminho_arquivo
        self.templates = self._carregar_templates()

    def _carregar_templates(self):
        try:
            with open(self.caminho_arquivo, 'r', encoding='utf-8') as file:
                return json.load(file)
        except Exception:
            return {}

    def obter_template_bruto(self, tipo_processo):
        return self.templates.get(tipo_processo, {})