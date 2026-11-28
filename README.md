# 🏦 Banco-24H

**Sistema de gerenciamento bancário com interface gráfica desenvolvido em Python.**

O Banco-24H é um projeto acadêmico desenvolvido para a disciplina de **Linguagem de Programação 3**, com o objetivo de aplicar conceitos de Programação Orientada a Objetos (POO) na construção de um sistema bancário funcional.

A aplicação simula as operações de um caixa eletrônico, permitindo o gerenciamento de contas, movimentações financeiras e administração de usuários por meio de uma interface gráfica desenvolvida com Tkinter.

---

## 📌 Funcionalidades

### 👤 Área do cliente
- Cadastro de clientes com validação de CPF e telefone.
- Criação de contas com identificação individual.
- Autenticação por ID da conta e senha.
- Consulta de saldo.
- Realização de depósitos e saques.
- Transferências entre contas.
- Consulta de extrato e histórico de movimentações.
- Alteração de dados cadastrais e senha.

### 🔐 Área administrativa
- Acesso exclusivo para administrador.
- Listagem e gerenciamento de contas cadastradas.
- Consulta de transferências realizadas no sistema.
- Edição de informações dos usuários.
- Encerramento de contas.
- Reversão de transferências.

### 💾 Persistência de dados
- Armazenamento dos dados utilizando serialização com `pickle`.
- Recuperação automática dos dados ao iniciar a aplicação.
- Salvamento automático ao encerrar o sistema.
- Gravação por arquivo temporário antes da substituição do arquivo principal.
- Compatibilidade com versões anteriores dos dados armazenados.

---

## 🛠️ Tecnologias utilizadas

| Tecnologia | Aplicação |
|---|---|
| Python | Linguagem principal |
| Tkinter | Interface gráfica |
| Decimal | Precisão em operações monetárias |
| Hashlib / HMAC | Proteção e verificação de senhas |
| Pickle | Persistência e serialização de objetos |
| OS | Manipulação de arquivos |

O projeto utiliza recursos da biblioteca padrão do Python, sem necessidade de instalação de dependências externas.

---

## 🧱 Arquitetura do projeto

O sistema foi organizado em módulos, separando as entidades do domínio bancário, as regras de negócio, a interface gráfica e o ponto de entrada da aplicação.

```text
Banco-24H/
│
├── src/
│   └── models/
│       ├── admin.py
│       ├── banco.py
│       ├── cliente.py
│       ├── conta.py
│       ├── interface.py
│       ├── main.py
│       └── movimentacao.py
│
├── .gitignore
└── README.md
```

### Responsabilidade dos módulos

- **admin.py:** gerenciamento da autenticação administrativa.
- **banco.py:** gerenciamento de contas, clientes e operações bancárias.
- **cliente.py:** representação dos dados cadastrais dos clientes.
- **conta.py:** gerenciamento de saldo, autenticação e operações individuais.
- **interface.py:** construção da interface gráfica e interação com o usuário.
- **main.py:** inicialização da aplicação, carregamento e salvamento dos dados.
- **movimentacao.py:** representação e registro das movimentações financeiras.

---

## ⚙️ Como executar

### 1. Pré-requisitos

- Python 3.10 ou superior.
- Tkinter disponível na instalação do Python.

### 2. Clonar o repositório

```bash
git clone https://github.com/oalancunha/Banco-24H.git
```

### 3. Acessar o diretório

```bash
cd Banco-24H
```

### 4. Executar a aplicação

```bash
python src/models/main.py
```

No Linux, caso o comando `python` não esteja configurado:

```bash
python3 src/models/main.py
```

Na primeira execução, o sistema cria automaticamente um novo banco de dados local (`banco.pkl`).

---

## 🔑 Acesso administrativo

O sistema possui um administrador predefinido, identificado pelo ID reservado `0`.

| Campo | Valor inicial |
|---|---|
| ID | `0` |
| Senha | `BancoRoot` |

**Atenção:** essas são credenciais padrão definidas no código-fonte. O sistema é um projeto acadêmico e não deve ser utilizado para armazenar dados bancários reais.

---

## 🧠 Conceitos aplicados

Durante o desenvolvimento, foram trabalhados conceitos fundamentais de programação e engenharia de software:

- Programação Orientada a Objetos.
- Encapsulamento e organização de responsabilidades.
- Relacionamento entre classes e objetos.
- Estruturas de dados e manipulação de coleções.
- Tratamento de exceções e validação de entradas.
- Manipulação e persistência de arquivos.
- Autenticação e armazenamento de hashes de senhas.
- Regras de negócio e integridade das movimentações financeiras.
- Desenvolvimento de interfaces gráficas com programação orientada a eventos.

---

## ⚠️ Observações de segurança

Este projeto possui finalidade exclusivamente acadêmica e demonstrativa.

Embora implemente mecanismos de hash de senhas e validação de operações, ainda existem limitações para utilização em um ambiente real.

Em particular, o uso de `pickle` exige que os arquivos carregados sejam considerados confiáveis, pois a desserialização de arquivos maliciosos pode executar código.

Não utilize o sistema para armazenar informações financeiras ou pessoais reais.

---

## 🚀 Possíveis evoluções

- Migração da persistência de dados para SQLite.
- Implementação de testes automatizados.
- Aprimoramento do gerenciamento de sessões e permissões.
- Refatoração das responsabilidades das classes.
- Aprimoramento da interface e experiência do usuário.
- Implementação de relatórios e funcionalidades administrativas adicionais.

---

## 🎓 Contexto acadêmico

Projeto desenvolvido como atividade prática da disciplina **Linguagem de Programação 3**, com foco na aplicação de conceitos de POO e no desenvolvimento de uma aplicação integrada.

**Desenvolvedor:** Alan Cunha, Johnny Breno, Matheus Pimentel

**Repositório:** [github.com/oalancunha/Banco-24H](https://github.com/oalancunha/Banco-24H)
