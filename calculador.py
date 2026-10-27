
import csv
from pathlib import Path


PASTA = Path(__file__).parent
ARQUIVO_ENTRADA = PASTA / "notas_alunos_limpo.csv"
ARQUIVO_SAIDA = PASTA / "notas_alunos_medias.csv"


def converter_nota(valor):
    """Converte uma nota para número decimal."""
    valor = str(valor).strip().replace(",", ".")

    if not valor:
        return 0.0

    try:
        return float(valor)
    except ValueError:
        return 0.0


def calcular_media(nota01, tf01, nota02, tf02):
    """Calcula a média ponderada de cada conjunto."""
    media01 = (
        converter_nota(nota01) * 8
        + converter_nota(tf01) * 2
    ) / 10

    media02 = (
        converter_nota(nota02) * 8
        + converter_nota(tf02) * 2
    ) / 10

    return (media01 + media02) / 2


def calcular_medias():
    if not ARQUIVO_ENTRADA.exists():
        raise FileNotFoundError(
            f"Arquivo não encontrado: {ARQUIVO_ENTRADA}\n"
            "Execute primeiro o codigo_limpo.py."
        )

    with open(
        ARQUIVO_ENTRADA,
        "r",
        encoding="utf-8-sig",
        newline=""
    ) as arquivo:
        leitor = csv.DictReader(arquivo, delimiter=";")

        campos = {
            "Nome", "RA", "Nota01", "TF01", "Nota02", "TF02"
        }

        if not leitor.fieldnames or not campos.issubset(
            leitor.fieldnames
        ):
            raise ValueError(
                "O CSV não contém todas as colunas necessárias."
            )

        alunos = []

        for aluno in leitor:
            if not aluno or not any(
                str(valor or "").strip()
                for valor in aluno.values()
            ):
                continue

            media = calcular_media(
                aluno["Nota01"],
                aluno["TF01"],
                aluno["Nota02"],
                aluno["TF02"]
            )

            aluno["MediaFinal"] = f"{media:.2f}"
            aluno["Situacao"] = (
                "Aprovado" if media >= 7 else "Reprovado"
            )

            alunos.append(aluno)

    campos_saida = [
        "Nome", "RA", "Nota01", "TF01", "Nota02", "TF02",
        "MediaFinal", "Situacao"
    ]

    with open(
        ARQUIVO_SAIDA,
        "w",
        encoding="utf-8",
        newline=""
    ) as arquivo:
        escritor = csv.DictWriter(
            arquivo,
            fieldnames=campos_saida,
            delimiter=";",
            lineterminator="\n"
        )
        escritor.writeheader()
        escritor.writerows(alunos)

    aprovados = sum(
        aluno["Situacao"] == "Aprovado"
        for aluno in alunos
    )

    reprovados = len(alunos) - aprovados

    print("\nCálculo das médias concluído!")
    print(f"Total de alunos: {len(alunos)}")
    print(f"Aprovados: {aprovados}")
    print(f"Reprovados: {reprovados}")
    print(f"Arquivo gerado: {ARQUIVO_SAIDA}")

    return alunos


def consultar_aluno(alunos):
    """Pesquisa um aluno pelo nome ou RA."""
    while True:
        pesquisa = input(
            "\nQual aluno você deseja consultar? "
            "(digite o nome ou RA, ou SAIR para encerrar): "
        ).strip().lower()

        if pesquisa == "sair":
            print("Consulta encerrada.")
            break

        if not pesquisa:
            print("Digite um nome ou RA válido.")
            continue

        encontrados = [
            aluno for aluno in alunos
            if pesquisa == aluno["RA"].lower()
            or pesquisa in aluno["Nome"].lower()
        ]

        if not encontrados:
            print("Nenhum aluno encontrado.")
            continue

        for aluno in encontrados:
            print("\n--- Dados do aluno ---")
            print(f"Nome: {aluno['Nome']}")
            print(f"RA: {aluno['RA']}")
            print(f"Nota 01: {aluno['Nota01']}")
            print(f"TF 01: {aluno['TF01']}")
            print(f"Nota 02: {aluno['Nota02']}")
            print(f"TF 02: {aluno['TF02']}")
            print(f"Média final: {aluno['MediaFinal']}")
            print(f"Situação: {aluno['Situacao']}")


if __name__ == "__main__":
    try:
        alunos = calcular_medias()
        consultar_aluno(alunos)
    except (FileNotFoundError, ValueError) as erro:
        print(f"Erro: {erro}")
