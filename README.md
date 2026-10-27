# 6326058-Aula07_Andre

# Projeto de Automação de Notas com Python

## Como testar o projeto

1. **Preparação:** abrir o projeto no VS Code e conferir o arquivo `notas_alunos.csv`.
2. **Automação:** executar `python automacao.py` para preencher e enviar os dados dos alunos no Google Forms.
3. **Retorno ao VS Code:** após processar o último aluno, retorne ao VS Code.
4. **Limpeza dos dados:** executar `python codigo_limpo.py` para padronizar nomes, RAs e notas.
5. **Cálculo das médias:** executar `python calculador.py` para calcular as médias e definir a situação dos alunos.
6. **Consulta:** pesquisar um aluno pelo nome ou RA e digitar `SAIR` para encerrar.

## Arquivos gerados

- `notas_alunos_limpo.csv`: dados padronizados.
- `notas_alunos_medias.csv`: notas, médias finais e situação dos alunos.

## Critério de aprovação

- Média final igual ou superior a **7,0**: Aprovado.
- Média final inferior a **7,0**: Reprovado.

**Observação:** execute os programas na ordem indicada e evite executar a automação novamente se as respostas já tiverem sido enviadas.
