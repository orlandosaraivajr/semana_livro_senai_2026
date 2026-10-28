# 🧮 Calculadora em Python com Tkinter

Calculadora de mesa com interface gráfica feita em **Python** e **Tkinter**. É um projeto de estudo desenvolvido durante o curso de tecnologia no **SENAI**.

A calculadora já funciona, mas o objetivo principal é praticar **boas práticas de programação**: separar a lógica da interface, escrever **testes unitários** e organizar o código de um jeito fácil de entender e de manter.

---

## ✨ Funcionalidades

| Botão | Função |
|-------|--------|
| `+` `−` `×` `÷` | Quatro operações básicas |
| `=` | Mostra o resultado |
| `%` | Porcentagem (`200 + 10%` = `220`) |
| `√x` | Raiz quadrada |
| `x²` | Elevar ao quadrado |
| `¹/x` | Inverso do número |
| `±` | Inverter o sinal |
| `,` | Separador decimal |
| `C` | Limpa tudo |
| `CE` | Limpa só o número atual |
| `⌫` | Apaga o último dígito |

Outros recursos:

- **Contas em sequência**: `2 + 3 × 4` vai calculando passo a passo, como numa calculadora comum.
- **Expressão no display**: a conta em andamento (por exemplo, `12 + 8 =`) aparece acima do resultado.
- **Tratamento de erros**: divisão por zero, raiz de número negativo e números grandes demais mostram `Erro` em vez de fechar o programa.
- **Uso pelo teclado**:

  | Tecla | Ação |
  |-------|------|
  | `0`–`9` | Digitar números |
  | `+` `-` `*` `/` | Operações |
  | `Enter` ou `=` | Resultado |
  | `,` ou `.` | Decimal |
  | `%` | Porcentagem |
  | `Backspace` | Apagar |
  | `Esc` | Limpar tudo (C) |
  | `Delete` | Limpar entrada (CE) |

---

## 🚀 Como executar

### Pré-requisitos

- [Python 3.8+](https://www.python.org/downloads/)
- O Tkinter já vem com o Python no Windows e no macOS. No Linux (Ubuntu/Debian), pode ser preciso instalá-lo:

  ```bash
  sudo apt install python3-tk
  ```

O projeto **não usa bibliotecas externas**, então não é preciso rodar `pip install`.

### Rodando a calculadora

```bash
git clone <url-deste-repositorio>
cd <pasta-do-repositorio>/versao2
python main.py
```

---

## 🧪 Testes

São **56 testes unitários**, escritos com o módulo `unittest` (que já vem no Python). Para rodá-los, entre na pasta `versao2` e execute:

```bash
python -m unittest -v
```

O que é testado:

- **Lógica** (`tests/test_logica.py`): operações básicas, contas em sequência, porcentagem, raiz, quadrado, inverso, troca de sinal, os botões de limpar e a recuperação depois de um erro.
- **Interface** (`tests/test_interface.py`): os cliques nos botões e as teclas do teclado chegam até a lógica e atualizam o display. Esses testes são pulados automaticamente em ambientes sem tela, como servidores de integração contínua.

---

## 🗂️ Estrutura do projeto

```
versao2/
├── main.py                 # Abre a janela da calculadora
├── calculadora/
│   ├── __init__.py
│   ├── logica.py           # Regras da calculadora (não depende da interface)
│   └── interface.py        # Janela, botões e teclado (Tkinter)
└── tests/
    ├── __init__.py
    ├── test_logica.py      # Testes da lógica
    └── test_interface.py   # Testes da interface
```

### Por que separar lógica e interface?

A classe `Calculadora`, em `logica.py`, não sabe que existe uma janela. Ela só recebe comandos (`digitar("7")`, `operador("+")`, `igual()`) e atualiza o texto do display.

A classe `CalculadoraApp`, em `interface.py`, cuida apenas da parte visual: ela desenha os botões e repassa cada clique para a `Calculadora`.

Essa divisão traz três vantagens:

1. **Testar é fácil**: os testes da lógica rodam em milissegundos, sem abrir janela nenhuma.
2. **Trocar a interface é simples**: a mesma lógica poderia ser usada numa versão web ou de terminal.
3. **O código fica organizado**: cada arquivo tem uma responsabilidade só.

---

## 📚 O que aprendi com este projeto

- Programação orientada a objetos em Python (classes, métodos, propriedades)
- Criação de interfaces gráficas com **Tkinter** (`grid`, `Button`, `Label`, `StringVar`, eventos de teclado)
- **Testes unitários** com `unittest`
- Separação de responsabilidades
- Tratamento de exceções (`ZeroDivisionError`, `OverflowError`, `ValueError`)
- Imprecisão dos números de ponto flutuante: `0.1 + 0.2` dá `0.30000000000000004` em Python, e a calculadora formata o resultado para mostrar `0.3`
- Versionamento de código com **Git** e **GitHub**

---

## 🔭 Próximos passos

- [ ] Histórico das contas feitas
- [ ] Memória (`M+`, `M−`, `MR`, `MC`)
- [ ] Alternar entre tema claro e escuro
- [ ] Gerar um executável (`.exe`) com PyInstaller
- [ ] Rodar os testes automaticamente com GitHub Actions

---

## 👤 Autor

**Seu Nome**
Estudante de tecnologia no SENAI

- LinkedIn: [linkedin.com/in/seu-perfil](https://linkedin.com/in/seu-perfil)
- GitHub: [github.com/seu-usuario](https://github.com/seu-usuario)

---

<sub>Projeto desenvolvido para a Semana do Livro SENAI 2026.</sub>
