"""Calculadora simples com as quatro operações básicas."""


def somar(a, b):
    return a + b


def subtrair(a, b):
    return a - b


def multiplicar(a, b):
    return a * b


def dividir(a, b):
    if b == 0:
        raise ValueError("Não é possível dividir por zero.")
    return a / b


OPERACOES = {
    "1": ("Soma", "+", somar),
    "2": ("Subtração", "-", subtrair),
    "3": ("Multiplicação", "*", multiplicar),
    "4": ("Divisão", "/", dividir),
}


def ler_numero(mensagem):
    while True:
        valor = input(mensagem).strip().replace(",", ".")
        try:
            return float(valor)
        except ValueError:
            print("Valor inválido. Digite um número.")


def exibir_menu():
    print("\n=== CALCULADORA ===")
    for chave, (nome, simbolo, _) in OPERACOES.items():
        print(f"{chave} - {nome} ({simbolo})")
    print("0 - Sair")


def main():
    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "0":
            print("Até logo!")
            break

        if opcao not in OPERACOES:
            print("Opção inválida. Tente novamente.")
            continue

        nome, simbolo, funcao = OPERACOES[opcao]
        a = ler_numero("Digite o primeiro número: ")
        b = ler_numero("Digite o segundo número: ")

        try:
            resultado = funcao(a, b)
            print(f"Resultado: {a:g} {simbolo} {b:g} = {resultado:g}")
        except ValueError as erro:
            print(f"Erro: {erro}")


if __name__ == "__main__":
    main()
