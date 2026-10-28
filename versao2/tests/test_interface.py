import tkinter as tk
import unittest
from types import SimpleNamespace

from calculadora.interface import CalculadoraApp


def tecla(char="", keysym=""):
    """Cria um evento de teclado falso para os testes."""
    return SimpleNamespace(char=char, keysym=keysym or char)


class TestInterface(unittest.TestCase):
    """Testa a janela sem exibi-la. É ignorado em ambientes sem tela."""

    def setUp(self):
        try:
            self.raiz = tk.Tk()
        except tk.TclError:
            self.skipTest("Ambiente sem suporte a interface gráfica")
        self.raiz.withdraw()
        self.app = CalculadoraApp(self.raiz)

    def tearDown(self):
        self.raiz.destroy()

    def clicar(self, *textos):
        for texto in textos:
            self.app.botoes[texto].invoke()

    def test_cria_todos_os_botoes(self):
        self.assertEqual(len(self.app.botoes), 24)

    def test_conta_pelos_botoes(self):
        self.clicar("1", "2", "+", "8", "=")
        self.assertEqual(self.app.texto_display.get(), "20")
        self.assertEqual(self.app.texto_expressao.get(), "12 + 8 =")

    def test_display_usa_virgula_decimal(self):
        self.clicar("7", "÷", "2", "=")
        self.assertEqual(self.app.texto_display.get(), "3,5")

    def test_conta_pelo_teclado(self):
        for evento in (tecla("9"), tecla("*"), tecla("3"), tecla("\r", "Return")):
            self.app.processar_tecla(evento)
        self.assertEqual(self.app.texto_display.get(), "27")

    def test_virgula_do_teclado_vira_ponto_decimal(self):
        for evento in (tecla("1"), tecla(","), tecla("5")):
            self.app.processar_tecla(evento)
        self.assertEqual(self.app.calculadora.display, "1.5")

    def test_escape_limpa(self):
        self.clicar("5", "5")
        self.app.processar_tecla(tecla("", "Escape"))
        self.assertEqual(self.app.texto_display.get(), "0")

    def test_tecla_desconhecida_e_ignorada(self):
        self.clicar("4")
        self.app.processar_tecla(tecla("a"))
        self.assertEqual(self.app.texto_display.get(), "4")


if __name__ == "__main__":
    unittest.main()
