import time
import webbrowser

import pyautogui
import pyperclip

from leitor_csv import ler_alunos


# Link do Google Forms
FORM_URL = (
    "https://docs.google.com/forms/d/e/"
    "1FAIpQLScoFPZqF7xu8lGmSLARhmlBbTyZk7KDMYHjcm1Ii4PT5_sbAg/"
    "viewform?usp=publish-editor"
)

# AJUSTE ESTES PONTOS DE ACORDO COM A POSIÇÃO DOS ELEMENTOS NA TELA.
# São coordenadas de exemplo, não posições garantidas para o seu Forms.
POSICAO_PRIMEIRO_CAMPO = (409, 386)
POSICAO_NOVA_RESPOSTA = (418, 274)

CAMPOS = ["Nome", "RA", "Nota01", "TF01", "Nota02", "TF02"]

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.5


def digitar_texto(texto):
    """Cola o texto preservando acentos e vírgulas."""
    pyperclip.copy(str(texto))
    pyautogui.hotkey("ctrl", "v")
    time.sleep(0.7)


def preencher_aluno(aluno, numero, total):
    print(f"Preenchendo aluno {numero} de {total}: {aluno['Nome']}")

    # Clica diretamente no primeiro campo do formulário.
    pyautogui.click(*POSICAO_PRIMEIRO_CAMPO)
    time.sleep(1)

    # Preenche os seis campos na ordem das colunas do CSV.
    for indice, campo in enumerate(CAMPOS):
        digitar_texto(aluno[campo])

        # Avança para o próximo campo.
        if indice < len(CAMPOS) - 1:
            pyautogui.press("tab")
            time.sleep(1)

    # Depois do último campo, TAB deve selecionar o botão Enviar.
    pyautogui.press("tab")
    time.sleep(1)

    # Envia usando o teclado.
    pyautogui.press("enter")

    print(f"Resposta do aluno {numero} enviada.")
    time.sleep(4)


def main():
    try:
        alunos = ler_alunos()
    except (FileNotFoundError, ValueError) as erro:
        print(f"Erro ao ler o CSV: {erro}")
        return

    print(f"Total de alunos encontrados: {len(alunos)}")

    # Abre o formulário somente uma vez.
    webbrowser.open(FORM_URL)

    print("Aguardando o Google Forms carregar...")
    time.sleep(4)

    for indice, aluno in enumerate(alunos, start=1):

        # Preenche e envia a resposta atual.
        preencher_aluno(aluno, indice, len(alunos))

        # Só abre outra resposta quando ainda existem alunos.
        if indice < len(alunos):
            print("Abrindo uma nova resposta...")

            # Clica no link da confirmação, sem digitar o endereço.
            pyautogui.click(*POSICAO_NOVA_RESPOSTA)

            time.sleep(1)

    print("Processo concluído!")
    print(f"Total processado: {len(alunos)} alunos.")


if __name__ == "__main__":
    main()
