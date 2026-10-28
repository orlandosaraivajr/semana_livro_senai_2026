"""Ponto de entrada: abre a janela da calculadora."""

import tkinter as tk

from calculadora.interface import CalculadoraApp


def main():
    raiz = tk.Tk()
    CalculadoraApp(raiz)
    raiz.mainloop()


if __name__ == "__main__":
    main()
