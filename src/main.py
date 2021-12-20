import sys

from g_python.gextension import Extension

from exalemao import Exalemao

extension_info = {
    "title": "Brinquedinho do AL",
    "description": "Minha honra chama-se lealdade!",
    "version": "1.0",
    "author": "Sigm4",
}

ext = Extension(extension_info, sys.argv)

try:
    ext.start()
except ConnectionRefusedError:
    print("Por favor, mude a porta do G-Earth para 9092.")
    sys.exit(1)


if __name__ == "__main__":
    print("Feche a janela se você deseja parar, desenvolvido por Sigm4.")
    Exalemao(ext)
