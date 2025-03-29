# TPC6: Analisador Léxico para Consultas SPARQL

2025-03-29

## Autor:
- Rafael Lopes Seara
- A104094

### Problema
Este trabalho de casa implementa um analisador léxico com a biblioteca PLY e um analisador sintático recursivo descendente em Python, capaz de avaliar expressões aritméticas simples com operações básicas.  

- **Reconhecimento** de números inteiros e operadores (`+`, `-`, `*`, `/`) através do analisador léxico.  
- **Construção** de uma árvore sintática com base nas regras da gramática.  
- **Avaliação correta** da expressão, respeitando a precedência dos operadores.  
- **Mensagens de erro claras** para erros léxicos e sintáticos.  

O grande destaque deste TPC é a implementação manual do analisador sintático, recorrendo à técnica de **análise recursiva descendente**.


### Funcionamento

O **analisador léxico** (`ana_lex.py`) usa `ply.lex` para identificar números inteiros (`NUM`) e operadores aritméticos (`PLUS`, `MINUS`, `TIMES`, `DIVIDE`), ignorando espaços e tabs, e emitindo avisos para símbolos inválidos. O **analisador sintático** (`ana_sin.py`) é implementado com descida recursiva, seguindo uma gramática que define a estrutura das expressões e construindo uma **árvore sintática** em listas aninhadas, como `['PLUS', 3, ['TIMES', 2, 4]]`.  

A **calculadora** (`calculation.py`) percorre a árvore sintática e calcula o valor final, respeitando a precedência dos operadores. O **programa principal** (`main.py`) recebe a expressão do utilizador, processa-a com os analisadores léxico e sintático, avalia o resultado e exibe os tokens, a árvore sintática e o valor final.

## Instrução de utilização

 ```sh
    $ python3 main.py
```