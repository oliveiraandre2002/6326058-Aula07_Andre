
import re


def limpar_nome(nome):
    """Converte para minúsculas e remove espaços desnecessários."""
    return " ".join(str(nome).strip().lower().split())


def limpar_ra(ra):
    """Mantém somente números e preenche RA ausente com 0."""
    ra_limpo = re.sub(r"\D", "", str(ra).strip())

    if not ra_limpo:
        return "0"

    return ra_limpo


def limpar_nota(valor, limite):
    """
    Converte notas para ponto decimal.
    Valores ausentes ou marcadores viram 0.
    Notas acima do limite são ajustadas ao limite.
    """
    valor = str(valor).strip().lower()

    if valor in ("", "n/a", "-", "falta", "faltou"):
        return "0"

    # Aceita vírgula ou ponto como separador decimal.
    valor = valor.replace(",", ".")

    try:
        nota = float(valor)
    except ValueError:
        return "0"

    if nota < 0:
        nota = 0

    if nota > limite:
        nota = limite

    return f"{nota:g}"


def limpar_aluno(aluno):
    """Limpa os dados de um aluno nas seis colunas do CSV."""
    return {
        "Nome": limpar_nome(aluno.get("Nome", "")),
        "RA": limpar_ra(aluno.get("RA", "")),
        "Nota01": limpar_nota(aluno.get("Nota01", ""), 10),
        "TF01": limpar_nota(aluno.get("TF01", ""), 2),
        "Nota02": limpar_nota(aluno.get("Nota02", ""), 10),
        "TF02": limpar_nota(aluno.get("TF02", ""), 2),
    }


if __name__ == "__main__":
    # Testes das regras de limpeza
    aluno_teste = {
        "Nome": "  LUCAS  RODRIGUES ",
        "RA": "RA100001",
        "Nota01": "12,5",
        "TF01": "FALTOU",
        "Nota02": " 8,5 ",
        "TF02": "3,0",
    }

    print(limpar_aluno(aluno_teste))

import csv
import re
from pathlib import Path


# Arquivos na mesma pasta deste código
PASTA = Path(__file__).parent
ARQUIVO_ORIGINAL = PASTA / "notas_alunos.csv"
ARQUIVO_LIMPO = PASTA / "notas_alunos_limpo.csv"

CAMPOS = ["Nome", "RA", "Nota01", "TF01", "Nota02", "TF02"]


def limpar_nome(nome):
    """Converte o nome para minúsculas e remove espaços extras."""
    return " ".join(str(nome).strip().lower().split())


def limpar_ra(ra):
    """Mantém somente números e usa 0 quando o RA estiver ausente."""
    ra_limpo = re.sub(r"\D", "", str(ra).strip())
    return ra_limpo if ra_limpo else "0"


def limpar_nota(valor, limite):
    """
    Converte vírgula decimal em ponto.
    Valores ausentes ou marcadores viram 0.
    Notas são limitadas ao máximo permitido.
    """
    valor = str(valor).strip().lower()

    if valor in ("", "n/a", "-", "falta", "faltou"):
        return "0"

    valor = valor.replace(",", ".")

    try:
        nota = float(valor)
    except ValueError:
        return "0"

    if nota < 0:
        nota = 0

    if nota > limite:
        nota = limite

    return f"{nota:g}"


def limpar_aluno(aluno):
    """Aplica as regras de limpeza às seis colunas."""
    return {
        "Nome": limpar_nome(aluno.get("Nome", "")),
        "RA": limpar_ra(aluno.get("RA", "")),
        "Nota01": limpar_nota(aluno.get("Nota01", ""), 10),
        "TF01": limpar_nota(aluno.get("TF01", ""), 2),
        "Nota02": limpar_nota(aluno.get("Nota02", ""), 10),
        "TF02": limpar_nota(aluno.get("TF02", ""), 2),
    }


def limpar_csv():
    """Lê o CSV original e grava uma cópia limpa."""
    if not ARQUIVO_ORIGINAL.exists():
        raise FileNotFoundError(
            f"Arquivo não encontrado: {ARQUIVO_ORIGINAL}"
        )

    with open(
        ARQUIVO_ORIGINAL,
        "r",
        encoding="utf-8-sig",
        newline=""
    ) as arquivo:
        leitor = csv.DictReader(arquivo, delimiter=";")

        if not leitor.fieldnames:
            raise ValueError("O CSV não possui cabeçalho.")

        leitor.fieldnames = [
            campo.strip() for campo in leitor.fieldnames
        ]

        faltando = set(CAMPOS) - set(leitor.fieldnames)

        if faltando:
            raise ValueError(
                f"Colunas ausentes no CSV: {', '.join(sorted(faltando))}"
            )

        alunos = [
            limpar_aluno(aluno)
            for aluno in leitor
            if aluno and any(
                str(valor or "").strip()
                for valor in aluno.values()
            )
        ]

    with open(
        ARQUIVO_LIMPO,
        "w",
        encoding="utf-8",
        newline=""
    ) as arquivo:
        escritor = csv.DictWriter(
            arquivo,
            fieldnames=CAMPOS,
            delimiter=";",
            lineterminator="\n"
        )

        escritor.writeheader()
        escritor.writerows(alunos)

    print("Limpeza concluída!")
    print(f"Alunos tratados: {len(alunos)}")
    print(f"Arquivo gerado: {ARQUIVO_LIMPO}")


if __name__ == "__main__":
    try:
        limpar_csv()
    except (FileNotFoundError, ValueError) as erro:
        print(f"Erro: {erro}")
