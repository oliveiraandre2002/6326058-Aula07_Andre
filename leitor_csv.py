import csv
from pathlib import Path


CAMPOS = ["Nome", "RA", "Nota01", "TF01", "Nota02", "TF02"]


def normalizar(texto):
    return "".join(
        caractere
        for caractere in texto.strip().casefold()
        if caractere.isalnum()
    )


def ler_alunos():
    caminho_csv = Path(__file__).resolve().parent / "notas_alunos.csv"

    if not caminho_csv.exists():
        raise FileNotFoundError(
            f"Arquivo CSV não encontrado: {caminho_csv}"
        )

    with caminho_csv.open(
        "r", encoding="utf-8-sig", newline=""
    ) as arquivo:

        primeira_linha = arquivo.readline()

        if not primeira_linha.strip():
            raise ValueError("O arquivo CSV está vazio.")

        separador = (
            ";" if primeira_linha.count(";") > primeira_linha.count(",")
            else ","
        )

        arquivo.seek(0)
        leitor = csv.reader(arquivo, delimiter=separador)

        cabecalho = next(leitor, None)

        if not cabecalho:
            raise ValueError("O CSV não possui cabeçalho.")

        indices = {
            normalizar(nome): indice
            for indice, nome in enumerate(cabecalho)
        }

        campos_normalizados = {
            normalizar(campo): campo for campo in CAMPOS
        }

        faltantes = [
            campo
            for campo in CAMPOS
            if normalizar(campo) not in indices
        ]

        if faltantes:
            raise ValueError(
                "Colunas ausentes no CSV: " + ", ".join(faltantes)
            )

        alunos = []

        for numero_linha, linha in enumerate(leitor, start=2):
            if not linha or all(not valor.strip() for valor in linha):
                continue

            aluno = {}

            for campo in CAMPOS:
                indice = indices[normalizar(campo)]

                aluno[campo] = (
                    linha[indice].strip()
                    if indice < len(linha)
                    else ""
                )

            if not aluno["Nome"] and not aluno["RA"]:
                continue

            alunos.append(aluno)

    if not alunos:
        raise ValueError("Nenhum aluno foi encontrado no CSV.")

    return alunos
  