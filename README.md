# Multi-Agent Wedding Planner

Projeto de estudo/portfólio que implementa um sistema **multiagente** com [LangChain](https://python.langchain.com/) para planejamento de casamentos. Um agente principal recebe o briefing do usuário e delega pesquisas na web para dois subagentes, consolidando tudo em um plano final.

Há duas formas de execução: uma **interface web em Streamlit** (`app.py`) e um **script de linha de comando** (`main.py`).

---

## Arquitetura

```
                        ┌──────────────────────────────┐
   Briefing do  ───────▶│   Wedding Planner (main)     │
   usuário              │   modelo: gpt-5-nano         │
                        │   tools: delegate_to_sub1/2  │
                        └───────┬──────────────┬───────┘
                                │              │
                    delegate_to_subagent1  delegate_to_subagent2
                                │              │
                        ┌───────▼──────┐ ┌─────▼────────┐
                        │  Subagent 1  │ │  Subagent 2  │
                        │  tool:       │ │  tool:       │
                        │  search_web  │ │  search_web  │
                        └───────┬──────┘ └─────┬────────┘
                                │              │
                                └──────┬───────┘
                                       ▼
                                 Tavily Search API
```

O agente principal não pesquisa diretamente: ele só enxerga os subagentes como _tools_. Cada subagente é um agente completo, com acesso à ferramenta `search_web` (Tavily). A resposta de cada subagente volta como string para o agente principal, que sintetiza o plano final.

Os agentes e os clients (OpenAI e Tavily) são criados **sob demanda**, na primeira delegação, e reaproveitados via `functools.lru_cache`. Importar `agents.py` não dispara chamada nem exige chave de API; `reset_agent_clients()` descarta os caches para que novas chaves passem a valer.

---

## Estrutura do repositório

| Arquivo                           | Responsabilidade                                                                                                                                                                                            |
| --------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `models.py`                       | Carrega o `.env` e expõe `get_openai_model()`, que cria o chat model (`init_chat_model("gpt-5-nano")`) sob demanda e o mantém em cache.                                                                     |
| `tools.py`                        | Define a tool `search_web`, que consulta a API da Tavily (`max_results=5`, `include_answer=True`) e formata o resumo e os resultados como texto. O client vem de `get_tavily_client()`, criado sob demanda. |
| `agents.py`                       | Tools de delegação `delegate_to_subagent1` / `delegate_to_subagent2` e os construtores em cache `get_subagent1()` / `get_subagent2()`. `reset_agent_clients()` limpa todos os caches.                       |
| `prompts.py`                      | `WEDDING_PLANNER_AGENT_PROMPT` (system prompt do agente principal, com placeholder `{requirements}`) e `USER_PROMPT_FOR_MAIN_AGENT`.                                                                        |
| `main.py`                         | Execução via terminal: lê os requisitos com `input()`, cria o agente principal e imprime a resposta.                                                                                                        |
| `app.py`                          | Aplicação Streamlit: formulário de briefing, checagem de chaves, execução do agente, histórico de execuções e exportação em Markdown.                                                                       |
| `src/multi_agent_acl/__init__.py` | Entry point declarado em `[project.scripts]` (atualmente apenas um placeholder).                                                                                                                            |
| `.env_exemple`                    | Modelo das variáveis de ambiente necessárias.                                                                                                                                                               |

---

## Pré-requisitos

- Python **3.12+** (fixado em `.python-version`)
- [uv](https://docs.astral.sh/uv/) para gerenciamento de dependências (há `uv.lock` versionado)
- Chave da **OpenAI** (`OPENAI_API_KEY`)
- Chave da **Tavily** (`TAVILY_API_KEY`)

## Instalação

```bash
git clone <url-do-repositorio>
cd Multi-agent-ACL

# instala as dependências a partir do uv.lock
uv sync
```

Crie o arquivo `.env` a partir do exemplo:

```bash
cp .env_exemple .env
```

```dotenv
OPENAI_API_KEY="sk-..."
TAVILY_API_KEY="tvly-..."
```

> O `.env` está no `.gitignore` e não deve ser versionado.

---

## Uso

### Interface web (Streamlit)

```bash
uv run streamlit run app.py
```

A aplicação oferece:

- **Formulário de briefing** — casal, local, data, número de convidados, moeda, faixa de orçamento, escopo do evento, estilo, prioridades de planejamento, tom, _must-haves_, restrições e tradições familiares.
- **Painel de runtime** na sidebar — indica se `OPENAI_API_KEY` e `TAVILY_API_KEY` estão disponíveis. As chaves podem vir do `.env`, dos _secrets_ do Streamlit ou serem digitadas direto na sidebar (sobrescrevem as demais em `os.environ`). O botão de gerar plano fica desabilitado enquanto faltar alguma chave.
- **Botão "Load sample brief"** — preenche o formulário com um exemplo completo.
- **Histórico de execuções** — cada plano gerado é guardado em `st.session_state` com título, requisitos, conteúdo, duração e timestamp, e pode ser baixado em Markdown.

O briefing do formulário é convertido pela função `build_requirements()` em um texto estruturado, que é injetado no `WEDDING_PLANNER_AGENT_PROMPT`. O plano solicitado ao agente inclui resumo executivo, recomendações de local e fornecedores, alocação de orçamento, cronograma e riscos/questões em aberto.

Os clientes dos agentes são carregados sob demanda e cacheados com `@st.cache_resource`; o botão **"Refresh agent clients"** limpa esse cache.

### Linha de comando

```bash
uv run python main.py
```

O script pede os requisitos por `input()`, monta o system prompt, cria o agente principal com as duas tools de delegação e imprime a última mensagem da resposta. O logging (`INFO`) mostra cada etapa, incluindo as queries delegadas a cada subagente.
