import unittest

from calculadora.logica import Calculadora, MENSAGEM_ERRO, formatar_numero


def digitar_numero(calc, texto):
    """Simula a digitação de um número tecla por tecla."""
    for caractere in texto:
        if caractere == ".":
            calc.ponto()
        else:
            calc.digitar(caractere)


class TestFormatarNumero(unittest.TestCase):
    def test_inteiro_sem_casas_decimais(self):
        self.assertEqual(formatar_numero(5.0), "5")

    def test_decimal(self):
        self.assertEqual(formatar_numero(2.5), "2.5")

    def test_corrige_imprecisao_de_ponto_flutuante(self):
        self.assertEqual(formatar_numero(0.1 + 0.2), "0.3")

    def test_zero_negativo_vira_zero(self):
        self.assertEqual(formatar_numero(-0.0), "0")


class TestDigitacao(unittest.TestCase):
    def setUp(self):
        self.calc = Calculadora()

    def test_display_inicial_e_zero(self):
        self.assertEqual(self.calc.display, "0")

    def test_digitar_numero(self):
        digitar_numero(self.calc, "123")
        self.assertEqual(self.calc.display, "123")

    def test_zeros_a_esquerda_sao_ignorados(self):
        digitar_numero(self.calc, "007")
        self.assertEqual(self.calc.display, "7")

    def test_ponto_decimal(self):
        digitar_numero(self.calc, "3.14")
        self.assertEqual(self.calc.display, "3.14")

    def test_ponto_no_inicio_adiciona_zero(self):
        self.calc.ponto()
        self.assertEqual(self.calc.display, "0.")

    def test_apenas_um_ponto_por_numero(self):
        digitar_numero(self.calc, "1.2")
        self.calc.ponto()
        self.assertEqual(self.calc.display, "1.2")

    def test_limite_de_digitos(self):
        digitar_numero(self.calc, "1" * 30)
        self.assertEqual(len(self.calc.display), 16)

    def test_digito_invalido_gera_excecao(self):
        with self.assertRaises(ValueError):
            self.calc.digitar("a")


class TestOperacoesBasicas(unittest.TestCase):
    def setUp(self):
        self.calc = Calculadora()

    def calcular(self, a, op, b):
        digitar_numero(self.calc, a)
        self.calc.operador(op)
        digitar_numero(self.calc, b)
        self.calc.igual()
        return self.calc.display

    def test_soma(self):
        self.assertEqual(self.calcular("2", "+", "3"), "5")

    def test_subtracao(self):
        self.assertEqual(self.calcular("10", "-", "4"), "6")

    def test_subtracao_com_resultado_negativo(self):
        self.assertEqual(self.calcular("4", "-", "10"), "-6")

    def test_multiplicacao(self):
        self.assertEqual(self.calcular("6", "*", "7"), "42")

    def test_divisao(self):
        self.assertEqual(self.calcular("7", "/", "2"), "3.5")

    def test_soma_de_decimais(self):
        self.assertEqual(self.calcular("0.1", "+", "0.2"), "0.3")

    def test_divisao_por_zero_mostra_erro(self):
        self.assertEqual(self.calcular("5", "/", "0"), MENSAGEM_ERRO)

    def test_operador_invalido_gera_excecao(self):
        with self.assertRaises(ValueError):
            self.calc.operador("^")

    def test_expressao_mostra_conta_completa(self):
        self.calcular("2", "+", "3")
        self.assertEqual(self.calc.expressao, "2 + 3 =")

    def test_expressao_mostra_conta_em_andamento(self):
        digitar_numero(self.calc, "12")
        self.calc.operador("*")
        self.assertEqual(self.calc.expressao, "12 ×")


class TestContasEncadeadas(unittest.TestCase):
    def setUp(self):
        self.calc = Calculadora()

    def test_operacoes_em_sequencia(self):
        # 2 + 3 × 4 = 20 (como em uma calculadora comum, da esquerda para a direita)
        digitar_numero(self.calc, "2")
        self.calc.operador("+")
        digitar_numero(self.calc, "3")
        self.calc.operador("*")
        self.assertEqual(self.calc.display, "5")
        digitar_numero(self.calc, "4")
        self.calc.igual()
        self.assertEqual(self.calc.display, "20")

    def test_trocar_operador_antes_do_segundo_numero(self):
        digitar_numero(self.calc, "8")
        self.calc.operador("+")
        self.calc.operador("-")
        digitar_numero(self.calc, "3")
        self.calc.igual()
        self.assertEqual(self.calc.display, "5")

    def test_continuar_a_partir_do_resultado(self):
        digitar_numero(self.calc, "2")
        self.calc.operador("+")
        digitar_numero(self.calc, "3")
        self.calc.igual()
        self.calc.operador("*")
        digitar_numero(self.calc, "10")
        self.calc.igual()
        self.assertEqual(self.calc.display, "50")

    def test_digitar_apos_resultado_inicia_nova_conta(self):
        digitar_numero(self.calc, "2")
        self.calc.operador("+")
        digitar_numero(self.calc, "3")
        self.calc.igual()
        digitar_numero(self.calc, "9")
        self.assertEqual(self.calc.display, "9")
        self.assertEqual(self.calc.expressao, "")

    def test_igual_sem_operador_nao_altera_nada(self):
        digitar_numero(self.calc, "42")
        self.calc.igual()
        self.assertEqual(self.calc.display, "42")

    def test_funcao_no_segundo_numero(self):
        # 9 + √16 = 13
        digitar_numero(self.calc, "9")
        self.calc.operador("+")
        digitar_numero(self.calc, "16")
        self.calc.raiz_quadrada()
        self.calc.igual()
        self.assertEqual(self.calc.display, "13")


class TestFuncoesEspeciais(unittest.TestCase):
    def setUp(self):
        self.calc = Calculadora()

    def test_raiz_quadrada(self):
        digitar_numero(self.calc, "81")
        self.calc.raiz_quadrada()
        self.assertEqual(self.calc.display, "9")

    def test_raiz_de_numero_negativo_mostra_erro(self):
        digitar_numero(self.calc, "4")
        self.calc.inverter_sinal()
        self.calc.raiz_quadrada()
        self.assertEqual(self.calc.display, MENSAGEM_ERRO)

    def test_quadrado(self):
        digitar_numero(self.calc, "12")
        self.calc.quadrado()
        self.assertEqual(self.calc.display, "144")

    def test_quadrado_muito_grande_mostra_erro(self):
        self.calc.display = "1e200"
        self.calc.quadrado()
        self.assertEqual(self.calc.display, MENSAGEM_ERRO)

    def test_inverso(self):
        digitar_numero(self.calc, "4")
        self.calc.inverso()
        self.assertEqual(self.calc.display, "0.25")

    def test_inverso_de_zero_mostra_erro(self):
        self.calc.inverso()
        self.assertEqual(self.calc.display, MENSAGEM_ERRO)

    def test_porcentagem_simples(self):
        digitar_numero(self.calc, "50")
        self.calc.porcentagem()
        self.assertEqual(self.calc.display, "0.5")

    def test_porcentagem_em_soma(self):
        # 200 + 10% = 220
        digitar_numero(self.calc, "200")
        self.calc.operador("+")
        digitar_numero(self.calc, "10")
        self.calc.porcentagem()
        self.assertEqual(self.calc.display, "20")
        self.calc.igual()
        self.assertEqual(self.calc.display, "220")

    def test_porcentagem_em_multiplicacao(self):
        # 200 × 10% = 20
        digitar_numero(self.calc, "200")
        self.calc.operador("*")
        digitar_numero(self.calc, "10")
        self.calc.porcentagem()
        self.calc.igual()
        self.assertEqual(self.calc.display, "20")

    def test_inverter_sinal(self):
        digitar_numero(self.calc, "5")
        self.calc.inverter_sinal()
        self.assertEqual(self.calc.display, "-5")
        self.calc.inverter_sinal()
        self.assertEqual(self.calc.display, "5")

    def test_inverter_sinal_de_zero_nao_faz_nada(self):
        self.calc.inverter_sinal()
        self.assertEqual(self.calc.display, "0")


class TestLimpeza(unittest.TestCase):
    def setUp(self):
        self.calc = Calculadora()

    def test_limpar_zera_tudo(self):
        digitar_numero(self.calc, "5")
        self.calc.operador("+")
        digitar_numero(self.calc, "3")
        self.calc.limpar()
        self.assertEqual(self.calc.display, "0")
        self.assertEqual(self.calc.expressao, "")
        self.calc.igual()
        self.assertEqual(self.calc.display, "0")

    def test_limpar_entrada_mantem_conta(self):
        digitar_numero(self.calc, "5")
        self.calc.operador("+")
        digitar_numero(self.calc, "9")
        self.calc.limpar_entrada()
        self.assertEqual(self.calc.display, "0")
        digitar_numero(self.calc, "3")
        self.calc.igual()
        self.assertEqual(self.calc.display, "8")

    def test_apagar_ultimo_digito(self):
        digitar_numero(self.calc, "123")
        self.calc.apagar()
        self.assertEqual(self.calc.display, "12")

    def test_apagar_ate_o_fim_mostra_zero(self):
        digitar_numero(self.calc, "7")
        self.calc.apagar()
        self.assertEqual(self.calc.display, "0")

    def test_apagar_numero_negativo(self):
        digitar_numero(self.calc, "7")
        self.calc.inverter_sinal()
        self.calc.apagar()
        self.assertEqual(self.calc.display, "0")

    def test_apagar_nao_altera_resultado(self):
        digitar_numero(self.calc, "2")
        self.calc.operador("+")
        digitar_numero(self.calc, "3")
        self.calc.igual()
        self.calc.apagar()
        self.assertEqual(self.calc.display, "5")


class TestRecuperacaoDeErro(unittest.TestCase):
    def setUp(self):
        self.calc = Calculadora()
        self.calc.inverso()  # 1/0 coloca a calculadora em erro

    def test_esta_em_erro(self):
        self.assertTrue(self.calc.em_erro)

    def test_operador_e_ignorado_durante_erro(self):
        self.calc.operador("+")
        self.assertEqual(self.calc.display, MENSAGEM_ERRO)

    def test_digitar_apos_erro_reinicia(self):
        self.calc.digitar("4")
        self.assertEqual(self.calc.display, "4")
        self.assertFalse(self.calc.em_erro)

    def test_apagar_apos_erro_reinicia(self):
        self.calc.apagar()
        self.assertEqual(self.calc.display, "0")


if __name__ == "__main__":
    unittest.main()
