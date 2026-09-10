# Portal de Despacho em Lote

> **Demonstração Online:** Acesse a aplicação ao vivo no Streamlit Cloud através do link abaixo:  
> [**despacho-em-lote.streamlit.app** 🔗 *(Abra em uma nova aba)*](https://despacho-em-lote.streamlit.app/)

>**Nota sobre o projeto:** Esta é uma **versão de demonstração** adaptada para portfólio. Para viabilizar testes públicos imediatos e garantir a privacidade de dados, o sistema atual opera com uma base de dados local e simulação de envios. Toda a aplicação foi construída sob os princípios do **Clean Architecture** e o padrão **MVC (Model-View-Controller)**: dividida em controladores especializados, gerenciador de sessão resiliente, componentes de UI modulares e camadas de acesso a dados (DALs) totalmente desacopladas, estando pronta para integrar-se a bancos SQL, NoSQL, APIs corporativas ou serviços em nuvem.

Um sistema corporativo de automação construído em Python e Streamlit, projetado para resolver um dos maiores gargalos operacionais de processos administrativos: o envio manual e repetitivo de e-mails em lote.

---

## O Problema vs. A Solução

### O Cenário Anterior
Diariamente, equipes operacionais gastam horas do seu dia realizando um trabalho braçal e sujeito a falhas: escrever dezenas de e-mails repetitivos, buscando dados avulsos em planilhas ou outras fontes de informação, para então redigir textos padronizados manualmente, anexar os arquivos corretos um a um e cruzar os dedos para não ter enviado dados de um cliente para outro.

### O Portal de Despacho
Este sistema transforma horas de trabalho manual em meros segundos. O usuário simplesmente arrasta todos os PDFs do lote para o portal. O sistema varre instantaneamente a nomenclatura dos documentos, agrupa os arquivos correspondentes à mesma operação, cruza essa referência com as bases de dados e preenche o e-mail completo (destinatários, assunto, corpo do texto e anexos).

Ao final, o sistema dispara o lote inteiro com segurança, exibe o progresso em tempo real e entrega um **Resumo Executivo** detalhado das transmissões.

---

## Como Funciona o Agrupamento por Referência?

O grande motor do sistema é a inteligência encapsulada no módulo `AgrupadorDocumentos`.

Se o usuário arrastar 50 PDFs misturados pertencentes a várias operações diferentes (ex: `OP-1002_relatorio.pdf`, `OP-1002_comprovante.pdf`, `OP-1005_nota.pdf`), o sistema não envia 50 e-mails avulsos. Ele lê os nomes de todos os arquivos, descarta cópias duplicadas automaticamente e organiza cada documento com a sua respectiva operação. Os arquivos que compartilham a mesma raiz (ex: a referência `OP-1002`) são agrupados em um pacote exclusivo; os da `OP-1005` formam outro, e assim sucessivamente.

Em seguida, para cada grupo formado, a camada de negócio busca as informações correspondentes na base de dados (`DalPlanilhaMestre`), injeta os modelos padronizados de e-mail (`DalTemplateEmails`) e preenche dinamicamente todas as variáveis da mensagem.

---

## Prévia, Visualização e Edição Individual

Um dos grandes diferenciais de segurança e usabilidade do sistema é a etapa de conferência. Antes de qualquer disparo, a interface gera uma prévia completa de todos os pacotes organizados.

Através de componentes visuais expansíveis para cada operação, o usuário tem total controle sobre o que será enviado, podendo:

* **Visualizar os Documentos (PDF Integrado):** Abrir e conferir o conteúdo de cada PDF anexado diretamente na tela do sistema em abas individuais (via conversão dinânica base64 em iframe), garantindo que os documentos estão corretos.
* **Ajustar Campos Individualmente:** Fazer modificações pontuais no e-mail de cada cliente. Os campos ficam abertos para edição, permitindo alterar os destinatários (`Para` e `CC`), personalizar o assunto ou editar o corpo do texto de uma operação de forma isolada, sem afetar o restante do lote.

O disparo em massa permanece travado e só é executado após o usuário marcar a caixa de confirmação atestando que revisou o lote.

---

## Arquitetura de Software e Organização do Código

O projeto foi refatorado para garantir o cumprimento do princípio de **Responsabilidade Única (SRP)** e permitir fácil testabilidade e manutenção.

```text
├── Controllers/
│   ├── ControladorDespacho.py    # Facade principal: orquestra a jornada da aplicação
│   └── ControladorEmail.py       # Controlador especializado na infraestrutura e fila de disparos
├── Models/
│   ├── AgrupadorDocumentos.py    # Regra de negócio: triagem, duplicatas e consolidação do lote
│   ├── GerenciadorDeSessao.py    # Encapsulamento do st.session_state e controle de versão
│   ├── ServicoEmail.py           # Comunicação e infraestrutura SMTP
│   └── DAL/                      # Data Access Layer (Acesso aos Dados)
│       ├── DalConfiguracoesSmtp.py
│       ├── DalDestinatarios.py
│       ├── DalPlanilhaMestre.py
│       └── DalTemplateEmails.py
└── Views/
    ├── Interface.py              # Fachada da View que expõe os métodos de tela
    └── Components/               # Componentes Visuais Modulares
        ├── ComponenteConfiguracao.py
        ├── ComponenteOperacao.py
        └── ComponenteResumo.py
```

### Principais Destaques Arquiteturais:
* **Controlador como Facade Enxuta:** O `ControladorDespacho` atua como um maestro de alto nível. Ele não manipula diretamente dicionários de e-mail, variáveis de sessão ou formatações de tela, delegando cada tarefa a componentes especializados.
* **Isolamento da Notificação (`ControladorEmail`):** Toda a preparação de mensagens, tratamento de conexões SMTP, validação de formato de e-mail e laço de execução do disparo pertencem exclusivamente ao `ControladorEmail`.
* **View Baseada em Componentes:** A interface foi fracionada em submódulos (`Views/Components/`), isolando a renderização de PDFs, formulários de edição e relatórios de resumo do restante da aplicação.
* **Gestão de Sessão Resiliente (`GerenciadorDeSessao`):** As variáveis do `st.session_state` não ficam espalhadas pelo código. O `GerenciadorDeSessao` centraliza a sincronização de contextos, incremento de versões de formulários e limpeza de caches.

---

## Configurações Importantes (Atenção Desenvolvedores)

### 1. Dados de Teste vs. Conexão com Produção
Atualmente, o sistema utiliza uma base de dados local (`planilha_mestre.xlsx`) e um pacote de simulação (`pacote_de_teste.zip`) disponível para download no topo da aplicação.
* **Como alterar para produção:** A camada de dados é totalmente abstraída pelas DALs. Para conectar o sistema a um banco de dados SQL, NoSQL ou API corporativa, basta atualizar os arquivos dentro de `Models/DAL/` (como a `DalPlanilhaMestre.py`). Nenhuma linha dos controladores ou da interface precisará ser alterada.

### 2. Gerenciamento de Templates (Desacoplamento)
Os textos e assuntos dos e-mails são consumidos dinamicamente da `DalTemplateEmails` (baseada no arquivo `templates_email.json`). Isso permite que equipes de negócio alterem modelos ou criem novos fluxos sem tocar no código Python.

### 3. Modo de Simulação vs. Disparo Real
Por padrão, a aplicação inicia em modo de simulação (`modo_simulacao=True`) dentro de `Controllers/ControladorDespacho.py`:
* **Para habilitar o envio real via SMTP:**
  1. No `ControladorDespacho.py`, altere a inicialização para: `self.ctrl_email = ControladorEmail(modo_simulacao=False)`.
  2. A credencial SMTP será recuperada automaticamente pela `DalConfiguracoesSmtp` priorizando o `st.secrets` do Streamlit ou fazendo fallback para o arquivo `secrets.toml` local (baseado no `secrets.example.toml`).

---

## Proteções e Resiliência do Sistema

O sistema conta com múltiplas camadas de proteção operacional:

* **Proteção contra Sobrecarga:** Limitação nativa de tamanho por arquivo via `config.toml` e bloqueio automático no backend para lotes com mais de 15 arquivos.
* **Deduplicação de Anexos:** Identificação e descarte automático de arquivos com nomes idênticos enviados por engano, acompanhado de alerta em tela e botão para resetar os uploads (`Limpar Todos os Anexos`).
* **Validação Prévia de E-mails:** Antes de iniciar qualquer envio SMTP, o `ControladorEmail` valida a sintaxe e o formato de todos os destinatários (`Para` e `CC`) do lote, cancelando o envio de forma preventiva e apontando exatamente qual campo precisa de correção.
* **Tratamento de Falhas e Logs:** Instabilidades durante a conexão de rede não travam a aplicação. As falhas são isoladas por operação e consolidadas no **Resumo Executivo** para consulta ao final da execução.