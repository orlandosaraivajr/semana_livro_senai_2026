"""Interface gráfica da calculadora, construída com Tkinter."""

import tkinter as tk

from calculadora.logica import Calculadora

CORES = {
    "fundo": "#1e1e2e",
    "texto": "#f5f5f5",
    "expressao": "#a0a0b8",
    "numero": "#3a3a4f",
    "funcao": "#2a2a3c",
    "operador": "#4a4a6a",
    "igual": "#0f62fe",
    "hover": "#55557a",
}

DIGITOS = set("0123456789")
OPERADORES = set("+-*/")


class CalculadoraApp:
    """Janela da calculadora: mostra o display e repassa cliques e teclas para a lógica."""

    def __init__(self, raiz):
        self.raiz = raiz
        self.calculadora = Calculadora()
        self.botoes = {}

        self.raiz.title("Calculadora")
        self.raiz.configure(bg=CORES["fundo"])
        self.raiz.resizable(False, False)

        self.texto_expressao = tk.StringVar()
        self.texto_display = tk.StringVar()

        self._criar_display()
        self._criar_botoes()
        self.raiz.bind("<Key>", self.processar_tecla)
        self.atualizar_display()

    def _criar_display(self):
        tk.Label(
            self.raiz, textvariable=self.texto_expressao, anchor="e",
            bg=CORES["fundo"], fg=CORES["expressao"], font=("Segoe UI", 12),
            padx=12,
        ).grid(row=0, column=0, columnspan=4, sticky="ew", pady=(12, 0))

        self.label_display = tk.Label(
            self.raiz, textvariable=self.texto_display, anchor="e",
            bg=CORES["fundo"], fg=CORES["texto"], font=("Segoe UI", 32, "bold"),
            padx=12,
        )
        self.label_display.grid(row=1, column=0, columnspan=4, sticky="ew", pady=(0, 12))

    def _layout_botoes(self):
        c = self.calculadora
        return [
            [("%", c.porcentagem, "funcao"), ("CE", c.limpar_entrada, "funcao"),
             ("C", c.limpar, "funcao"), ("⌫", c.apagar, "funcao")],
            [("¹/x", c.inverso, "funcao"), ("x²", c.quadrado, "funcao"),
             ("√x", c.raiz_quadrada, "funcao"), ("÷", self._operador("/"), "operador")],
            [("7", self._digito("7"), "numero"), ("8", self._digito("8"), "numero"),
             ("9", self._digito("9"), "numero"), ("×", self._operador("*"), "operador")],
            [("4", self._digito("4"), "numero"), ("5", self._digito("5"), "numero"),
             ("6", self._digito("6"), "numero"), ("−", self._operador("-"), "operador")],
            [("1", self._digito("1"), "numero"), ("2", self._digito("2"), "numero"),
             ("3", self._digito("3"), "numero"), ("+", self._operador("+"), "operador")],
            [("±", c.inverter_sinal, "numero"), ("0", self._digito("0"), "numero"),
             (",", c.ponto, "numero"), ("=", c.igual, "igual")],
        ]

    def _criar_botoes(self):
        for linha, botoes in enumerate(self._layout_botoes(), start=2):
            for coluna, (texto, acao, tipo) in enumerate(botoes):
                botao = tk.Button(
                    self.raiz, text=texto, command=lambda a=acao: self._executar(a),
                    bg=CORES[tipo], fg=CORES["texto"], activebackground=CORES["hover"],
                    activeforeground=CORES["texto"], relief="flat", bd=0,
                    font=("Segoe UI", 16), width=4, height=1, cursor="hand2",
                )
                botao.grid(row=linha, column=coluna, padx=2, pady=2, ipadx=8, ipady=8, sticky="nsew")
                self.botoes[texto] = botao

    def _digito(self, digito):
        return lambda: self.calculadora.digitar(digito)

    def _operador(self, op):
        return lambda: self.calculadora.operador(op)

    def _executar(self, acao):
        acao()
        self.atualizar_display()

    def processar_tecla(self, evento):
        """Permite usar a calculadora pelo teclado do computador."""
        tecla, nome = evento.char, evento.keysym
        c = self.calculadora

        if tecla in DIGITOS:
            acao = self._digito(tecla)
        elif tecla in OPERADORES:
            acao = self._operador(tecla)
        elif tecla in (".", ","):
            acao = c.ponto
        elif tecla == "%":
            acao = c.porcentagem
        elif tecla == "=" or nome in ("Return", "KP_Enter"):
            acao = c.igual
        elif nome == "BackSpace":
            acao = c.apagar
        elif nome == "Escape":
            acao = c.limpar
        elif nome == "Delete":
            acao = c.limpar_entrada
        else:
            return
        self._executar(acao)

    def atualizar_display(self):
        # No Brasil usamos vírgula como separador decimal.
        texto = self.calculadora.display.replace(".", ",")
        self.texto_display.set(texto)
        self.texto_expressao.set(self.calculadora.expressao.replace(".", ","))
        tamanho = 32 if len(texto) <= 10 else 22
        self.label_display.configure(font=("Segoe UI", tamanho, "bold"))
