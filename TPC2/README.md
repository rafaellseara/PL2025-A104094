# TPC2: Análise de um dataset de obras musicais

2025-02-10

## Autor:
- Rafael Lopes Seara
- A104094

### Problema
Pretende-se um programa que leia um *dataset* de obras músicais e cálcule os seguintes resultados:
1. Lista **ordenada alfabeticamente** dos **compositores** musicais;
2. Distribuição das **obras por período**: quantas obras catalogadas em cada período;
3. Dicionário em que a cada período está a associada uma **lista alfabética** dos títulos das obras desse período.

### Funcionamento
O código lê um arquivo CSV, ajusta quebras de linha internas aos campos e separa os dados usando um delimitador ponto-e-vírgula (através de regex), respeitando os campos entre aspas. Em seguida, extrai os compositores (ordenados alfabeticamente), agrupa obras por período e conta a quantidade de obras para cada período, exibindo esses resultados.

## Instrução de utilização

 ```sh
    $ python3 main.py <dataset_path>
```
