# Portal de Despacho em Lote

> **Demonstração Online:** Acesse a aplicação ao vivo no Streamlit Cloud através do link abaixo:  
> [**despacho-em-lote.streamlit.app** 🔗 *(Abra em uma nova aba)*](https://despacho-em-lote.streamlit.app/)

Um sistema corporativo de automação construído em Python e Streamlit, projetado para resolver um dos maiores gargalos operacionais de processos administrativos: o envio manual e repetitivo de e-mails.

---

## O Problema vs. A Solução

### O Cenário Anterior
Diariamente, equipes operacionais gastam horas do seu dia realizando um trabalho braçal e sujeito a falhas: escrever dezenas de e-mails repetitivos, buscando dados avulsos em planilhas ou outras fontes de informação, para então redigir textos padronizados manualmente, anexar os arquivos corretos um a um e cruzar os dedos para não ter enviado dados de um cliente para outro.

### O Portal de Despacho
Este sistema transforma horas de trabalho manual em meros segundos. O usuário simplesmente arrasta todos os PDFs respectivos para o portal. O sistema varre instantaneamente a nomenclatura dos documentos, agrupa os arquivos correspondentes à mesma operação, cruza essa referência com o banco de dados e monta o e-mail completo (assunto, corpo do texto e anexos).

É a solução ideal para processos que exigem o envio de e-mails padronizados, onde o modelo (texto e assunto) possui pouca variação, alterando apenas os dados referentes a cada cliente. Ao final, o sistema dispara o lote inteiro com segurança e entrega um relatório dos disparos.

---

## Como Funciona o Agrupamento por Referência?

O grande motor do sistema é a inteligência de Agrupamento por Referência.

Se o usuário arrastar 50 PDFs misturados pertencentes a várias operações diferentes (ex: OP-1002_relatorio.pdf, OP-1002_comprovante.pdf, OP-1005_nota.pdf), o sistema não envia 50 e-mails avulsos. Ele lê os nomes de todos os arquivos e organiza cada documento com o seu respectivo processo. Os arquivos que compartilham a mesma raiz (ex: a referência OP-1002) são agrupados em um pacote exclusivo; os da OP-1005 formam outro, e assim sucessivamente, até organizar todos os documentos.

Em seguida, para cada grupo formado, o sistema busca os dados correspondentes na base de dados e preenche dinamicamente as informações do e-mail (Assunto e Corpo do Texto). O resultado é a geração de um e-mail bem estruturado, contendo exatamente os seus anexos correspondentes e dados específicos.

---

## Prévia, Visualização e Edição Individual

Um dos grandes diferenciais de segurança e usabilidade do sistema é a etapa de conferência. Antes que qualquer e-mail seja disparado, o sistema gera uma prévia completa de todos os pacotes organizados.

Através de uma interface com blocos expansíveis para cada operação, o usuário tem total controle sobre o que será enviado, podendo:

* **Visualizar os Documentos:** Abrir e conferir o conteúdo de cada PDF anexado diretamente na tela do sistema (visualizador integrado), garantindo visualmente que os arquivos corretos foram agrupados.
* **Ajustar Campos Individualmente:** Fazer modificações pontuais no e-mail de cada cliente. Os campos ficam abertos para edição, permitindo alterar os destinatários (Para e Com Cópia), personalizar o assunto ou adicionar observações específicas no corpo do texto de uma operação de forma isolada, sem afetar o restante do lote.

O disparo em massa permanece travado e só é executado após o usuário marcar a caixa de confirmação atestando que verificou os dados e anexos estão corretos.

---

## Configurações Importantes (Atenção Desenvolvedores)

Este repositório foi configurado de forma simplificada para facilitar a avaliação e testes. Para implementar em um ambiente de produção real, atente-se às configurações abaixo:

### 1. Dados de Teste Estáticos vs. Integração em Produção
Atualmente, o sistema conta com uma base de dados em Excel (`planilha_mestre.xlsx`) e um pacote pré-compactado (`pacote_de_teste.zip`) disponível para download direto na interface.
* **Como alterar para produção:** O sistema possui uma arquitetura modular baseada no padrão MVC. Para conectar a um banco de dados real ou a um ERP, basta alterar o arquivo `Models/DAL.py` (Data Access Layer). O restante da aplicação permanecerá intacto, podendo se conectar a bancos SQL, APIs externas ou planilhas em nuvem sem gerar impactos no Controlador.

### 2. Gerenciamento de Templates (Desacoplamento)
Para facilitar a manutenção por equipes de negócios, os textos e assuntos dos e-mails foram desacoplados do código-fonte. 
* O sistema consome dinamicamente o arquivo `templates_email.json`. Isso permite que analistas e gestores criem novos modelos de e-mail ou editem textos existentes sem precisarem alterar nenhuma linha de código Python.

### 3. Modo de Simulação de E-mail (Segurança no Portfólio)
Por padrão, o envio de e-mails está ativado em Modo de Simulação (`modo_simulacao=True`) no arquivo `Controllers/ControladorPrincipal.py`. Isso garante que a interface e relatórios funcionem sem realizar disparos de e-mails reais.
* **Como habilitar o envio real:**
  1. No arquivo `Controllers/ControladorPrincipal.py`, altere a inicialização para: `self.notificador = ServicoEmail(modo_simulacao=False)`
  2. **Localmente:** Crie a pasta `.streamlit` na raiz e adicione o arquivo `secrets.toml` com suas credenciais SMTP (baseado no `secrets.example.toml`).
  3. **Na Nuvem:** Acesse o painel da sua aplicação no Streamlit Cloud, vá em **Settings > Secrets** e insira as suas credenciais.

---

## Proteções e Resiliência do Sistema

O sistema foi desenhado para manter a estabilidade mesmo diante de imprevistos. Ele possui as seguintes camadas de proteção:

* **Proteção contra Sobrecarga:** O sistema possui dupla validação para evitar o consumo excessivo de memória no servidor. O upload é limitado nativamente a 2 MB por arquivo (via `config.toml`) e o back-end bloqueia automaticamente tentativas de envio de lotes com mais de 15 documentos.
* **Prevenção contra Arquivos Duplicados:** Se o usuário anexar o mesmo arquivo duas vezes acidentalmente, o sistema identifica e descarta a cópia preventivamente. A interface exibe um alerta detalhando os nomes exatos dos arquivos ignorados e disponibiliza um botão de "Limpar Anexos" para reiniciar o lote de forma fácil.
* **Validação Antecipada de Dados:** Antes de iniciar a fila de envios, o sistema verifica todos os destinatários informados. Se houver um e-mail digitado incorretamente em alguma das caixas de texto, a operação é bloqueada preventivamente, indicando na tela exatamente onde está o erro para correção.
* **Tolerância a Falhas de Conexão:** Se o servidor de e-mail da empresa apresentar instabilidade durante a operação, o sistema não é interrompido de forma abrupta. Ele isola a falha, registra o erro na operação afetada, continua processando o restante da fila normalmente e exibe um relatório final detalhando o motivo do problema.
