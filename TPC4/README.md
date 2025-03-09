# TPC4: Analisador Léxico

2025-03-06

## Autor:
- Rafael Lopes Seara
- A104094

### Problema
Construir um analisador léxico para uma liguagem de query com a qual se podem escrever frases do género:

```
# DBPedia: obras de Chuck Berry

select ?nome ?desc where {
    ?s a dbo:MusicalArtist.
    ?s foaf:name "Chuck Berry"@en .
    ?w dbo:artist ?s.
    ?w foaf:name ?nome.
    ?w dbo:abstract ?desc
} LIMIT 100
```

### Funcionamento
O código define um analisador léxico para uma linguagem de query similar ao SPARQL, usando a biblioteca `ply.lex`. Ele identifica diferentes tipos de tokens, como palavras-chave (`select`, `where`, `LIMIT`), variáveis (`?nome`), URIs (`dbo:MusicalArtist`), strings (`"Chuck Berry"@en`), números (`1000`) e símbolos (`{}, ., :`). Cada token é reconhecido por meio de expressões regulares e processado por funções específicas. O lexer ignora espaços e quebras de linha, e caso encontre caracteres inválidos, os ignora com um aviso. A função `tokenize()` processa uma string de entrada e retorna uma lista de tokens, permitindo a análise estrutural da query.

## Instrução de utilização

 ```sh
    $ python3 main.py 
```