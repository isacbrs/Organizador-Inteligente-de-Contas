# Documentação Técnica - Feature 1.3: CRUD de Contas e Multitenancy

# 1. Visão Geral
A Feature 1.3 estabelece a camada de persistência de dados para o gerenciamento de faturas (CRUD). O principal requisito arquitetural resolvido nesta etapa é o **Multitenancy** (isolamento de inquilinos), garantindo que os dados financeiros de cada usuário sejam estritamente isolados em nível de banco de dados e de aplicação.

# 2. Stack Tecnológica
* **Roteamento e Segurança:** FastAPI (Python)
* **Validação de Contratos (DTOs):** Pydantic
* **Banco de Dados e IAM:** Supabase (PostgreSQL / GoTrue)

# 3. Detalhes de Implementação e Segurança

# 3.1. Proteção em Nível de Banco de Dados (RLS)
A tabela `contas` foi projetada com uma restrição de chave estrangeira (`user_id`) vinculada diretamente à tabela `auth.users` do Supabase. Para garantir o isolamento absoluto (Zero-Trust), o **Row Level Security (RLS)** foi ativado. 

Políticas rigorosas foram estabelecidas no PostgreSQL para que operações de `SELECT`, `INSERT`, `UPDATE` e `DELETE` só sejam executadas se o `auth.uid()` da transação for estritamente igual ao `user_id` proprietário da linha. Isso impede o vazamento de dados mesmo em caso de falha na camada de aplicação.

# 3.2. Validação de Contratos (Pydantic DTOs)
Para mitigar injeções de dados malformados e garantir a integridade do banco de dados, o tráfego HTTP é sanitizado via Pydantic:
* `ContaCreate`: Valida e tipa os dados de entrada no método POST, forçando, por exemplo, que a variável `data_vencimento` respeite o padrão ISO 8601 (YYYY-MM-DD) nativamente.
* `ContaResponse`: Padroniza a resposta JSON, omitindo dados sensíveis e tipando explicitamente as saídas para consumo seguro do Front-end.

# 3.3. Injeção de Dependências e Interceptação JWT
A API utiliza o sistema de `Depends` do FastAPI para proteger os *endpoints*. 
A cada requisição, o token JWT (Bearer) é extraído do *Header* e validado contra o serviço de autenticação (`supabase.auth.get_user`). O identificador único do usuário (UUID) é recuperado no Back-end e injetado nos *payloads* de persistência, impossibilitando que um usuário forje requisições em nome de terceiros.

# 4. Fluxo de Execução (Lifecycle)
1. O Front-end realiza uma requisição `POST /contas` contendo o *payload* da fatura e o token JWT no cabeçalho.
2. O FastAPI intercepta a requisição e valida a assinatura e vigência do JWT.
3. O Pydantic sanitiza o *payload* (rejeitando com HTTP 422 em caso de não conformidade).
4. O *Controller* recupera o UUID do token e orquestra a inserção dos dados.
5. O PostgreSQL aplica as regras de RLS e confirma a transação.
6. A API retorna `HTTP 201 Created` com o objeto persistido.