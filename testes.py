import sys
import os

for arq in os.listdir("scripts_a_ler"):
    caminho_completo = os.path.join("scripts_a_ler", arq)
    print(f"Lendo o arquivo: {caminho_completo}")