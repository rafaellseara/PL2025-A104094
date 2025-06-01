# PL-Project-24-25 - Compilador para Pascal Standard

*Para correr o programa:* 
``` bash
cat exemploX.pas | python.exe .\syntax.py
```

## Parte 1: Introdução

Projeto de Processamento de Linguagens 2025

Construção de um Compilador para Pascal Standard

Realizado por:

- Pedro Teixeira - A103998
- Ricardo Sousa - A104524
- Rafael Seara - A104094

### 1. Resumo
Este relatório descreve a implementação de um compilador para a linguagem _Pascal Standard_, desenvolvido no contexto da disciplina de Processamento de Linguagens (PL) no ano de 2025. O compilador abrange as etapas principais de:
1. Análise Léxica  
2. Análise Sintática  
3. Análise Semântica  
4. Código para a Máquina Virtual (EWVM)  

---

## Parte 2: Análise Léxica (Lexer)

### 2.1 Descrição Geral  
A etapa de Análise Léxica (“lexer”) tem como objetivo transformar o texto bruto do programa Pascal em uma sequência de tokens, identificando palavras‐chave, literais, identificadores, operadores e símbolos especiais. Para isso, utilizamos a biblioteca **PLY (Python Lex‐Yacc)**, especificamente o módulo `ply.lex`, que fornece ferramentas para a definição de padrões (regex) e gera automaticamente o analisador léxico.

O arquivo principal do lexer neste projeto é o `lexer.py`, onde definimos:

1. **Lista de literais** (`literals`)  
2. **Lista de nomes de tokens** (`tokens`)  
3. **Funções `t_<NOME>` com expressões regulares** para reconhecer cada token (case‐insensitive)  
4. **Ignorância de comentários** e espaços em branco  
5. **Tratamento de erros lexicais**  
6. **Criação do objeto `lexer`**, invocando `lex.lex()`

A seguir, detalharemos cada parte, listando os tokens suportados e trechos de código relevantes.

---

### 2.2 Lista de Literais e Tokens  

#### 2.2.1 Literais  
No Pascal, vários símbolos de pontuação e operadores de uso único podem ser tratados diretamente como literais (sem identificador nomeado). No nosso `lexer.py`, definimos:

```python
literals = [';', '(', ')', '.', ':', ',', '=', '+', '-', '*', '<', '>', '[', ']', '/']
```

- `;` : separador de comandos
- `(`, `)` : delimitadores de expressões e parâmetros
- `.` : ponto final de programa (e acesso a campos, no Pascal “padrão” estendido)
- `:` : usado em declarações de tipos, rótulos e também como parte do token `:=`
- `,` : separador em parâmetros/formais/listas
- `=` / `<` / `>` : operadores de comparação (parte do reconhecimento direto de literais; comparadores com dois caracteres, como `<=`, são capturados via regex nomeada)
- `+`, `-`, `*` : operadores aritméticos unários/binários
- `[` , `]` : delimitadores de índices em arrays
- `/` : operador de divisão (não‐inteira, no caso do Pascal estendido)

#### 2.2.2 Tokens

Além dos literais, precisamos reconhecer palavras‐chave e padrões mais complexos (identificadores, números, strings, operadores compostos, etc.). A lista completa de nomes de tokens (strings) no `lexer.py` é:

```python
tokens = [
    # PALAVRAS RESERVADAS
    'PROGRAM', 'VAR', 'BEGIN', 'END', 'ARRAY', 'OF',

    # TIPOS
    'INTEGER', 'STRING', 'BOOLEAN', 

    # IDENTIFICADORES E LITERAIS
    'identifier', 'number', 'argument',

    # COMANDOS DE ENTRADA/SAÍDA
    'WRITE', 'WRITELN', 'READ', 'READLN',

    # CONTROLE DE FLUXO
    'IF', 'THEN', 'ELSE',
    'WHILE', 'FOR', 'TO', 'DO', 'DOWNTO',

    # OPERADORES E ATRIBUIÇÃO
    'assign',      # ':='
    'lowerequal',  # '<='
    'greaterequal',# '>='
    'DIV',         # 'div'
    'MOD',         # 'mod'
    'AND',         # 'and'
    'OR',          # 'or'
    'dotdot',      # '..'

    # JUÍZOS DE VALOR
    'TRUE',
    'FALSE',
    'NOT',

    # FUNÇÕES
    'LENGTH'
]
```

- **Estrutura do programa**: `PROGRAM`, `VAR`, `BEGIN`, `END`, `ARRAY`, `OF` – definem o esqueleto e declarações do programa
- **Tipos e valores**: `INTEGER`, `STRING`, `BOOLEAN`, `TRUE`, `FALSE` – representam tipos de dados e constantes lógicas
- **Identificadores e literais**: `identifier`, `number`, `argument` – nomes de variáveis, números e argumentos de funções
- **Entrada e saída**: `READ`, `READLN`, `WRITE`, `WRITELN` – permitem comunicar com o utilizador
- **Controlo e lógica**: `IF`, `THEN`, `ELSE`, `WHILE`, `FOR`, `TO`, `DO`, `DOWNTO`, `NOT`, `AND`, `OR` – controlam o fluxo e operações lógicas
- **Operadores e funções**: `assign (:=)`, `lowerequal (<=)`, `greaterequal (>=)`, `DIV`, `MOD`, `dotdot (..)`, `LENGTH` – usados para expressões, intervalos e funções auxiliares

### 2.3 Padrões (Expressões Regulares) e Funções do Lexer

#### 2.3.1 Reconhecimento de Palavras‐Chave (Case‐Insensitive)

Cada palavra‐chave é implementada como uma função cujo nome segue o padrão `t_<PALAVRA>` e cujo docstring (primeira linha entre aspas) contém uma expressão regular que corresponde à palavra em qualquer combinação de maiúsculas/minúsculas. Exemplo para a palavra‐chave `PROGRAM`:


```python
def t_PROGRAM(t):
    r"\b[pP][rR][oO][gG][rR][aA][mM]\b"
    t.value = t.value.lower()
    return t
```

- A regex `[pP][rR][oO][gG][rR][aA][mM]` permite que cada letra da palavra "PROGRAM" seja maiúscula ou minúscula.
- Essa abordagem garante que a linguagem aceite palavras-chave em qualquer capitalização (ex: `Program`, `program`, `PROGRAM`).
- Após o reconhecimento, `t.value` é convertido para minúsculas para uniformizar o processamento.
- Esta normalização é útil nas fases sintática e semântica do compilador.
- A mesma técnica é aplicada a outras palavras-chave: `VAR`, `BEGIN`, `END`, `ARRAY`, `OF`, `FUNCTION`.
- Também se aplica a tipos (`INTEGER`, `STRING`, `BOOLEAN`) e comandos de I/O (`WRITE`, `WRITELN`, `READ`, `READLN`).

#### 2.3.2 Identificador (`identifier`)

Qualquer sequência que comece com uma letra ou underscore (`_`), seguida de letras, dígitos ou underscores, é reconhecida como `identifier` — desde que **não** corresponda a uma palavra-chave já capturada anteriormente.

Exemplo de definição em PLY:

```python
def t_identifier(t):
    r"[a-zA-Z_][a-zA-Z0-9_]*"
    return t
```

- É de observar que o PLY prioriza regexes mais longas ou mais específicas (palavras‐chave) antes de padrões genéricos. Assim, “begin” será capturado por `t_BEGIN`, não por `t_identifier`.

#### 2.3.3 Número Inteiro (`number`)

Números inteiros positivos são capturados por:

```python
def t_number(t):
    r'\d+'
    t.value = int(t.value)
    return t
```
- Não há suporte a números em ponto flutuante nem notação científica; apenas inteiros.

#### 2.3.4 Literal de String (`argument`)

Strings em Pascal são definidas entre aspas simples. Capturamos o conteúdo interno (sem as aspas) usando:

```python
def t_argument(t):
    r"\'([^\']*)\'"
    t.value = t.value[1:-1]
    return t
```

- O grupo `([^\']*)` aceita qualquer caractere que não seja `'` repetido zero ou mais vezes.
- Ao armazenar `t.value`, retiramos as duas aspas extremas.

#### 2.3.5 Operador de Atribuição (`assign`)

O símbolo de atribuição em Pascal é `:=`. Para reconhecer este token antes de capturar `:` como literal, definimos:

```python
def t_assign(t):
    r":="
    return t
```

#### 2.3.6 Operadores lowerequal e greaterequal (`lowerequal`, `greaterequal`)

Os operadores de comparação `<=` e `>=` são capturados por:

```python
def t_lowerequal(t):
    r"<="
    return t

def t_greaterequal(t):
    r">="
    return t
```

- Estes tokens são necessários para expressões condicionais e loops.

#### 2.3.7 Operador de Range (`dotdot`)

Em declarações de arrays (e em slices), Pascal utiliza `..` para especificar intervalos. Implementamos:

```python
def t_dotdot(t):
    r"\.\."
    return t
```
Esse token captura exatamente dois pontos consecutivos. Se houvesse `.` sozinho, ele seria tratado como literal.

#### 2.3.8 Operadores Lógicos e Controladores de Fluxo

Algumas palavras‐chave compostas por dois ou mais caracteres, como `AND`, `OR`, `NOT`, `FOR`, `TO`, `DO`, `DOWNTO`, etc., são definidas de forma semelhante às seguintes funções:

```python
def t_NOT(t):
    r"\b[nN][oO][tT]\b"
    t.value = t.value.lower()
    return t

def t_END(t):
    r"\b[eE][nN][dD]\b" 
    t.value = t.value.lower()
    return t
```

- Cada função segue o mesmo padrão: regex case‐insensitive e conversão de `t.value` para minúsculas.

### 2.4 Tratamento de Comentários, Espaços e Erros

#### 2.4.1 Comentários

No escopo deste compilador, consideramos comentários delimitados por chaves `{ ... }` (estilo Pascal clássico). O lexer ignora completamente o conteúdo desses blocos:

```python
def t_comment(t):
    r'\{[^}]*\}'
    pass
```

-O padrão `\{[^}]*\}` corresponde a `{` seguido de qualquer número de caracteres que não sejam `}`, até encontrar `}`.
-A diretiva `pass` faz com que o token seja descartado (não retornado), ignorando o texto comentado.

#### 2.4.2 Espaços em Branco e Quebras de Linha

Espaços, tabs e quebras de linha não são significativos na análise léxica, portanto:

```python
t_ignore = " \t\n"
```

- A variável especial `t_ignore` recebe uma string com todos os caracteres a serem descartados automaticamente.  
- Isso evita que espaços e quebras de linha gerem tokens “vazios”.


#### 2.4.3 Tratamento de Erros Léxicos

Caso o lexer encontre um caractere que não corresponda a nenhum token nem faça parte de `t_ignore`, invocamos:

```python
def t_error(t):
    print('Illegal character:', t.value[0])
    t.lexer.skip(1)
```

- `t.value[0]` é o caractere ilegal encontrado.  
- Ao chamar `t.lexer.skip(1)`, avançamos um caractere e tentamos continuar a análise, evitando loops infinitos.

### 2.5 Criação do Lexer

No final do arquivo `lexer.py`, após todas as definições de tokens e regras, instanciamos o analisador léxico:

```python
lexer = lex.lex()
```

A chamada lex.lex() varre todas as funções definidas (`t_<NOME>`) e a lista `tokens`, monta as tabelas internas de correspondência de expressões regulares em ordem adequada e devolve o objeto `lexer`.

## Parte 3: Análise Sintática (Parser)

### 3.1 Descrição Geral  

A etapa de Análise Sintática recebe a sequência de tokens gerada pelo lexer e verifica se ela obedece à gramática da linguagem Pascal Standard. Para isso, utiliza-se a biblioteca **PLY (Python Lex-Yacc)**, especificamente o módulo `ply.yacc`. Também gera o código correspondente para a máquina virtual (EWVM), disponibilizada pelos docentes, para testar o funcionamento do mesmo. 

No projeto, as definições de regras sintáticas estão no arquivo `syntax.py`. O PLY, ao processar essas regras, gera automaticamente o arquivo `parsetab.py`, contendo tabelas de análise (LR) para uso interno, mas não precisamos editá-lo manualmente.

---

### 3.2 Gramática

Começou-se por definir uma gramática apta a reconhecer todos os tokens produzidos pelo analisador léxico e a construir um parser que verifica a estrutura do código fonte de forma correta.

Apresentamos em baixo um excerto com o resumo das regras implementadas:

```python
Pascal_Prog                 : PROGRAM identifier ';' Var_Declaration Code

Var_Declaration             : VAR Var_Lines
                            | 

Var_Lines                   : Var_Lines Var_Line
                            | Var_Line
                            | 

Var_Line                    : Var_Names ':' Type ';'

Var_Names                   : Var_Names ',' identifier
                            | identifier

Type                        : INTEGER
                            | STRING
                            | BOOLEAN
                            | ARRAY '[' number dotdot number ']' OF Type

Code                        : BEGIN Lines_Of_Code END '.'

Lines_Of_Code               : Program_Line_Sequence
                            | Program_Line_Sequence Program_Line_No_Semi_Colon
                            | Program_Line_No_Semi_Colon
                            | 

Program_Line_Sequence       : Program_Line_Sequence Program_Line
                            | Program_Line

Program_Line                : Write_Line ';'
                            | Write_Line_No_ln ';'
                            | Read_Line ';'
                            | Read_Line_ln ';'
                            | Assignment ';'
                            | If_Statement ';'
                            | Block ';'
                            | For_Statement ';'
                            | While_Statement ';'

Program_Line_No_Semi_Colon  : Write_Line
                            | Write_Line_No_ln
                            | Read_Line
                            | Read_Line_ln
                            | Assignment
                            | If_Statement_Complete
                            | If_Statement_Incomplete
                            | Block
                            | For_Statement
                            | While_Statement

Write_Line                  : WRITELN '(' Write_Args ')'

Write_Line_No_ln            : WRITE '(' Write_Args ')'

Write_Args                  : Write_Args ',' Write_Arg
                            | Write_Arg

Write_Arg                   : argument
                            | identifier

Read_Line                   : READ '(' identifier ')'
                            | READLN '(' identifier '[' Expression ']' ')'

Read_Line_ln                : READLN '(' identifier ')'

Assignment                  : identifier assign Expression

Expression                  : Expression '+' Expression
                            | Expression '-' Expression
                            | Expression '*' Expression
                            | Expression '/' Expression
                            | Expression '>' Expression
                            | Expression '<' Expression
                            | Expression '=' Expression
                            | Expression lowerequal Expression
                            | Expression greaterequal Expression
                            | Expression DIV Expression
                            | Expression MOD Expression
                            | Expression AND Expression
                            | Expression OR Expression
                            | '(' Expression ')'
                            | identifier
                            | identifier '[' Expression ']'
                            | number
                            | argument
                            | TRUE
                            | FALSE
                            | NOT Expression
                            | LENGTH '(' identifier ')'

If_Statement                : If_Statement_Complete
                            | If_Statement_Incomplete

If_Statement_Complete       : IF Expression THEN Program_Line_No_Semi_Colon ELSE Program_Line_No_Semi_Colon

If_Statement_Incomplete     : IF Expression THEN Program_Line_No_Semi_Colon

For_Statement               : FOR identifier assign Expression TO Expression DO Program_Line_No_Semi_Colon
                            | FOR identifier assign Expression DOWNTO Expression DO Program_Line_No_Semi_Colon

While_Statement             : WHILE Expression DO Program_Line_No_Semi_Colon

Block                       : BEGIN Lines_Of_Code END

```

Esta gramática cobre os principais elementos da linguagem:

- **Estrutura do programa**: Começa com a palavra-chave PROGRAM, seguida da declaração de variáveis e do bloco principal de código entre BEGIN ... END.

- **Declarações de variáveis**: Suporta tipos primitivos (integer, string, boolean) e vetores (array) com intervalos definidos, permitindo estruturas de dados simples.

- **Comandos**: A gramática reconhece comandos de leitura (READ, READLN), escrita (WRITE, WRITELN), atribuições (:=), blocos (BEGIN ... END), condicionais (IF ... THEN ... ELSE) e ciclos (FOR, WHILE).

- **Expressões**: Permite expressões aritméticas, booleanas e comparativas, com suporte para indexação de arrays, chamadas LENGTH e operações lógicas como AND, OR, NOT.

- **Controle de fluxo**: O suporte a IF, FOR e WHILE permite criar programas estruturados e com decisões lógicas.

### 3.3 Estrutura de Suporte à Análise

As variáveis auxiliares do parser são estruturas internas usadas para armazenar e controlar o estado da compilação à medida que o parser analisa o código fonte Pascal. Elas não fazem parte da gramática em si, mas são essenciais para gerar corretamente o código EWVM e garantir que o programa seja semanticamente válido. Neste projeto, estas variáveis são:

- `parser.index`
  - **Função**: Contador global de posições de memória.
  - **Usado para**: Atribuir endereços consecutivos a variáveis declaradas.
  - **Como funciona**: Sempre que uma variável é declarada, `parser.index` é incrementado.
  - **No caso de arrays**: O índice avança múltiplas posições (uma por elemento do array).

- `parser.regists`
  - **Tipo**: Dicionário nome_variável → endereço
  - **Função**: Associa cada identificador ao índice na memória EWVM.
  - **Exemplo**: `parser.regists["x"] = 0 → a` variável `x` está no índice 0 da stack global.

- `parser.var_types`
  - **Tipo**: Dicionário nome_variável → tipo
  - **Função**: Guarda o tipo de cada variável, incluindo informações detalhadas no caso de arrays.
  - **Tipos possíveis**: `integer`, `string`, `boolean`, ou ('array', início, fim, tipo_elemento)
  - **Essencial para**: Saber como inicializar variáveis e gerar o código correto (ex: `WRITEI` vs `WRITES`, `STOREG` vs `STOREN`).

- `parser.labels`
  - **Tipo**: Lista de strings usadas como nomes de labels
  - **Função**: Geração de labels únicos para `IF`, `FOR`, `WHILE` etc.
  - **Exemplo**: L0, L1, L2...
  - **Evita conflitos**: Ao usar `len(parser.labels)` para gerar labels únicos.

- `parser.success`
  - **Tipo**: Booleano
  - **Função**: Indica se a análise sintática e semântica foi bem-sucedida.
  - **Se for False**: O parsing é interrompido e o código EWVM não é impresso.
  - **Usado para**: Detetar erros como variáveis não declaradas, duplicadas, ou tipos inválidos.

## Parte 4: Implementação

### Expressões e Operações

A produção Expression permite compor expressões complexas com operadores aritméticos, relacionais, lógicos e específicos da linguagem Pascal como DIV e MOD. Cada operador é mapeado diretamente para a sua instrução correspondente na EWVM, através do dicionário ops.

#### Tipos de operações suportadas
- **Aritméticas**: `+`, `-`, `*`, `/`, `DIV`, `MOD`

  - Traduzem-se para: `ADD`, `SUB`, `MUL`, `DIV`, `DIV`, `MOD`

  - `DIV` e `MOD` refletem o comportamento de divisão inteira e módulo em Pascal.

- **Comparação**: `=`, `<`, `>`, `<=`, `>=`

  - Traduzem-se para: `EQUAL`, `INF`, `SUP`, `INFEQ`, `SUPEQ`

  - Usadas para condições em ciclos e `if`'s.

- **Booleanas**: `AND`, `OR`

  - Traduzem-se para: `AND`, `OR`

  - Permitem conjunções e disjunções lógicas entre expressões.


## Parte 5: Testes

Para este projeto, foram disponibilizados 7 exemplos de programas Pascal para testarmos o funiconamento do nosso compilador. Estes exemplos abordavam diferentes construções da linguagem: 

### Declaração de Programa
```Pascal
program NomeDoPrograma;
```
Exemplos: HelloWorld, Maior3, Fatorial, NumeroPrimo, etc.

### Declaração de Variáveis
```Pascal
var
    nomeVariavel: Tipo;
```
Exemplos:
```Pascal
var
    num1, num2, num3, maior: Integer;
    numeros: array[1..5] of integer;
```

### Tipos de Dados
- Integer
- String
- Boolean
- Array

### Estruturas de Controlo
- Condicional (if-then-else)
  ```Pascal
  if condição then
    instrução
  else
    instrução;
  ```

- Ciclo for
  ```Pascal
  for i := 1 to n do
    instrução;
  ```

- Ciclo while
  ```Pascal
  while condição do
  begin
    instruções;
  end;
  ```

### Entrada e Saída
- `ReadLn()` – leitura de dados.
- `Write()` / `WriteLn()` – escrita de dados.

### Atribuições
```Pascal
variável := valor;
```
Exemplo:
```pascal
fat := fat * i;
```

### Funcões definidas pelo Utilizador
```Pascal
function NomeFuncao(parametros): TipoRetorno;
```
Exemplo:
```Pascal
function BinToInt(bin: string): integer;
```

### Funções e Operadores Nativos
- `length()` – comprimento de uma string.

- `mod` – operador de resto da divisão inteira.

- `div` – divisão inteira.

- `:=` – operador de atribuição.

### Arrays
```Pascal
array[1..5] of integer;
```
Usado para armazenar múltiplos valores numéricos.

### Indexação de Strings
```Pascal
bin[i]
```
Para aceder aos caracteres de uma string.

### Exemplo de Funcionamento
Começamos por compilar um dos exemplos no nosso compilador. Para este exemplo, vamos usar o `exemplo6.pas`

```Pascal
program BinarioParaInteiro;
var
    bin: string;
    i, valor, potencia: integer;
begin
    writeln('Introduza uma string binária:');
    readln(bin);

    valor := 0;
    potencia := 1;
    for i := length(bin) downto 1 do
    begin
        if bin[i] = '1' then
            valor := valor + potencia;
        potencia := potencia * 2;
    end;
    
    writeln('O valor inteiro correspondente é: ', valor);
end.
```

No terminal, escrevemos o seguinte comando:
```
cat exemplos/exemplo6.pas | python3 syntax.py
```

E o resultado será:
```
PUSHS ""
PUSHI 0
PUSHI 0
PUSHI 0
START
PUSHS "Introduza uma string binária:"
WRITES
WRITELN
READ
STOREG 0
PUSHI 0
STOREG 2
PUSHI 1
STOREG 3
PUSHG 0
STRLEN
STOREG 1
L1:
PUSHG 1
PUSHI 1
SUPEQ
JZ L2
PUSHG 0
PUSHG 1
PUSHI 1
SUB
CHARAT
PUSHS "1"
PUSHI 0
CHARAT
EQUAL
JZ L0
PUSHG 2
PUSHG 3
ADD
STOREG 2
L0:
PUSHG 3
PUSHI 2
MUL
STOREG 3
PUSHG 1
PUSHI 1
SUB
STOREG 1
JUMP L1
L2:
PUSHS "O valor inteiro correspondente é: "
WRITES
PUSHG 2
WRITEI
WRITELN
STOP

Frase válida:  program BinarioParaInteiro;
var
    bin: string;
    i, valor, potencia: integer;
begin
    writeln('Introduza uma string binária:');
    readln(bin);

    valor := 0;
    potencia := 1;
    for i := length(bin) downto 1 do
    begin
        if bin[i] = '1' then
            valor := valor + potencia;
        potencia := potencia * 2;
    end;
    
    writeln('O valor inteiro correspondente é: ', valor);
end.
```

Como podemos verificar, o compilador validou o programa fornecido e escreveu o código EWVM para ser testado na plataforma oficial da máquina virtual [EWVM](https://ewvm.epl.di.uminho.pt)


## Parte 6: Considerações Adicionais

No início da realização do projeto optámos por não utilizar uma representação intermédia como a Árvore de Sintaxe Abstrata (AST), privilegiando uma estratégia em que o código da EWVM é gerado diretamente durante a análise gramatical. Esta abordagem reduziu a complexidade da implementação e permitiu produzir resultados imediatos. Contudo, esta decisão também implicou abrir mão de certas vantagens que a AST oferece, como a possibilidade de realizar otimizações mais profundas ou análises semânticas avançadas.

O compilador implementa um conjunto razoável de verificações semânticas básicas, incluindo:

- Deteção de variáveis não declaradas;

- Prevenção de duplicações em declarações;

- Verificação de tipos em operações aritméticas, booleanas e de atribuição;

- Validação de acessos a arrays e uso correto de índices.

Embora não tenha sido incluído suporte a subprogramas (como funções ou procedimentos), o sistema consegue já lidar com blocos aninhados, ciclos, expressões complexas, leitura e escrita, o que permite compilar programas funcionais e relativamente expressivos.

O tratamento de erros no compilador foi concebido para atuar em três níveis distintos. A **nível léxico**, são identificados símbolos inválidos, que são posteriormente ignorados para permitir que a análise prossiga sem interrupções. No **plano sintático**, o compilador deteta construções mal formadas durante o processo de parsing, emitindo mensagens de erro apropriadas e utilizando a variável `parser.success` para indicar se o processo pode continuar. Por fim, na **vertente semântica**, são realizadas verificações manuais durante as ações associadas às produções da gramática, com o objetivo de identificar incompatibilidades de tipo, acessos incorretos a variáveis ou outros erros de lógica que não podem ser captados pelas fases anteriores.

A separação do código por responsabilidades (`lexer.py` e `syntax.py`) permitiu modularizar o projeto e facilitou a implementação faseada. O uso de variáveis auxiliares como `parser.regists`, `parser.var_types` e `parser.labels` revelou-se essencial para o controlo de contexto, alocação de memória e gestão de saltos e ciclos.

## Parte 7: Trabalho Futuro

Apesar de o compilador atual já suportar uma boa parte da linguagem Pascal e conseguir gerar código funcional para a EWVM, existem várias direções possíveis para evoluir o projeto e torná-lo mais completo, robusto e escalável:

### Suporte a Subprogramas (Procedimentos e Funções)
Uma das principais extensões futuras seria a introdução de procedimentos e funções. Isso exigiria alterações na gramática e uma gestão mais sofisticada do ambiente de execução.

### Construção de AST (Árvore de Sintaxe Abstrata)
Passar da geração direta de código para uma fase intermédia baseada em AST permitiria:

- Separar claramente a análise sintática da geração de código;
- Aplicar transformações, otimizações e análises mais sofisticadas.

### Melhorias no Tratamento de Erros
O sistema de deteção de erros pode ser melhorado com:

- Sugestões de correção;
- Realce da linha e coluna exata dos erros;
- Continuação robusta após erros para deteção múltipla numa só execução.


## Parte 8: Conclusão

O desenvolvimento deste compilador para a linguagem Pascal permitiu consolidar conhecimentos fundamentais sobre análise léxica, análise sintática, geração de código e verificação semântica, num contexto prático e aplicável.

A opção por uma abordagem de tradução direta durante o parsing mostrou-se eficaz para produzir código imediato e funcional para a EWVM, mantendo o sistema relativamente simples e compreensível. Apesar de não ter sido construída uma AST, foi possível gerar programas corretos com suporte a variáveis, estruturas de controlo, expressões, leitura e escrita.

Ao longo do projeto, foram implementadas várias verificações de segurança e coerência semântica que contribuíram para uma execução mais previsível e confiável dos programas. O tratamento de erros foi planeado para atuar em diferentes fases do processo de compilação, garantindo feedback útil ao utilizador.

No geral, o projeto alcançou os seus objetivos principais e representa uma base sólida para futuras extensões, como a introdução de subprogramas, otimizações de código ou a adoção de uma arquitetura baseada em AST. O resultado final é um compilador funcional, educativo e extensível, capaz de traduzir uma sublinguagem relevante de Pascal para a máquina virtual EWVM.
