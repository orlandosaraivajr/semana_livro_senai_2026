"""Regras de funcionamento da calculadora, independentes da interface gráfica.

Manter a lógica separada da tela permite testá-la com testes unitários
sem precisar abrir nenhuma janela.
"""

import math
import operator

MAX_DIGITOS = 16
MENSAGEM_ERRO = "Erro"

# Cada operador mapeia para a função que o executa e o símbolo exibido na tela.
OPERACOES = {
    "+": (operator.add, "+"),
    "-": (operator.sub, "−"),
    "*": (operator.mul, "×"),
    "/": (operator.truediv, "÷"),
}


def formatar_numero(valor):
    """Converte um número em texto, sem casas decimais desnecessárias."""
    texto = f"{valor:.12g}"
    return "0" if texto == "-0" else texto


class Calculadora:
    """Simula o comportamento de uma calculadora comum.

    O atributo ``display`` guarda o número mostrado na tela e ``expressao``
    guarda a conta em andamento (por exemplo, ``"12 +"``).
    """

    def __init__(self):
        self.limpar()

    @property
    def em_erro(self):
        return self.display == MENSAGEM_ERRO

    # ---------- Entrada de números ----------

    def digitar(self, digito):
        if digito not in "0123456789" or len(digito) != 1:
            raise ValueError(f"Dígito inválido: {digito!r}")
        if self.em_erro:
            self.limpar()
        if self._operador is None:
            self.expressao = ""

        if self._novo_numero or self.display == "0":
            self.display = digito
            self._novo_numero = False
        elif len(self.display) < MAX_DIGITOS:
            self.display += digito
        self._aguardando_operando = False

    def ponto(self):
        if self.em_erro:
            self.limpar()
        if self._operador is None:
            self.expressao = ""

        if self._novo_numero:
            self.display = "0."
            self._novo_numero = False
        elif "." not in self.display and len(self.display) < MAX_DIGITOS:
            self.display += "."
        self._aguardando_operando = False

    # ---------- Operações com dois números ----------

    def operador(self, op):
        if op not in OPERACOES:
            raise ValueError(f"Operador inválido: {op!r}")
        if self.em_erro:
            return

        if self._operador is not None and not self._aguardando_operando:
            # Contas encadeadas: 2 + 3 + ... calcula 2 + 3 antes de continuar.
            if not self._calcular():
                return
        elif self._operador is None:
            self._acumulador = self._valor_atual()

        self._operador = op
        self._novo_numero = True
        self._aguardando_operando = True
        self.expressao = f"{formatar_numero(self._acumulador)} {OPERACOES[op][1]}"

    def igual(self):
        if self.em_erro or self._operador is None:
            return
        simbolo = OPERACOES[self._operador][1]
        expressao = f"{formatar_numero(self._acumulador)} {simbolo} {self.display} ="
        if self._calcular():
            self.expressao = expressao
            self._operador = None
            self._acumulador = None

    # ---------- Operações com um número ----------

    def raiz_quadrada(self):
        self._aplicar_funcao(math.sqrt)

    def quadrado(self):
        self._aplicar_funcao(lambda valor: valor ** 2)

    def inverso(self):
        self._aplicar_funcao(lambda valor: 1 / valor)

    def porcentagem(self):
        """Em somas e subtrações, calcula a porcentagem do primeiro número.

        Exemplo: 200 + 10% resulta em 200 + 20. Nos demais casos, divide por 100.
        """
        if self._operador in ("+", "-"):
            base = self._acumulador
            self._aplicar_funcao(lambda valor: base * valor / 100)
        else:
            self._aplicar_funcao(lambda valor: valor / 100)

    def inverter_sinal(self):
        if self.em_erro or self._valor_atual() == 0:
            return
        if self.display.startswith("-"):
            self.display = self.display[1:]
        else:
            self.display = "-" + self.display
        self._aguardando_operando = False

    # ---------- Limpeza ----------

    def limpar(self):
        """Botão C: zera tudo, inclusive a conta em andamento."""
        self.display = "0"
        self.expressao = ""
        self._acumulador = None
        self._operador = None
        self._novo_numero = True
        self._aguardando_operando = False

    def limpar_entrada(self):
        """Botão CE: zera apenas o número que está sendo digitado."""
        if self.em_erro:
            self.limpar()
            return
        self.display = "0"
        self._novo_numero = True
        self._aguardando_operando = False

    def apagar(self):
        """Botão ⌫: remove o último caractere digitado."""
        if self.em_erro:
            self.limpar()
            return
        if self._novo_numero:
            return
        self.display = self.display[:-1]
        if self.display in ("", "-"):
            self.display = "0"

    # ---------- Auxiliares ----------

    def _valor_atual(self):
        return float(self.display)

    def _calcular(self):
        funcao = OPERACOES[self._operador][0]
        try:
            resultado = funcao(self._acumulador, self._valor_atual())
        except (ZeroDivisionError, OverflowError):
            self._mostrar_erro()
            return False
        if not self._mostrar_resultado(resultado):
            return False
        self._acumulador = resultado
        return True

    def _aplicar_funcao(self, funcao):
        if self.em_erro:
            return
        try:
            resultado = funcao(self._valor_atual())
        except (ZeroDivisionError, OverflowError, ValueError):
            self._mostrar_erro()
            return
        if self._mostrar_resultado(resultado):
            self._aguardando_operando = False

    def _mostrar_resultado(self, resultado):
        if not math.isfinite(resultado):
            self._mostrar_erro()
            return False
        self.display = formatar_numero(resultado)
        self._novo_numero = True
        return True

    def _mostrar_erro(self):
        self.limpar()
        self.display = MENSAGEM_ERRO
