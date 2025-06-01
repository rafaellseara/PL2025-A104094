from lexer import tokens, literals
import ply.yacc as yacc

precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'lowerequal', 'greaterequal', '<', '>'),
    ('left', '+', '-'),
    ('left', '*', '/', 'DIV', 'MOD'),
    ('right', 'NOT'),
)

def p_pascal_prog(p):
    """
    Pascal_Prog : PROGRAM identifier ';' Var_Declaration Code
    """
    init_code = []
    for var, tipo in p[4]:
        if tipo == "integer":
            init_code.append("PUSHI 0")
        elif tipo == "string":
            init_code.append('PUSHS ""')
        elif tipo == "boolean":
            init_code.append("PUSHI 0")
        elif tipo == "array":
            try:
                start, end, element_type = parser.var_types[var][1:]
                size = end - start + 1
                for _ in range(size):
                    if element_type == "integer":
                        init_code.append("PUSHI 0")
                    elif element_type == "string":
                        init_code.append('PUSHS ""')
                    elif element_type == "boolean":
                        init_code.append("PUSHI 0")
                    else:
                        raise ValueError(f"Tipo de elemento desconhecido '{element_type}' no array '{var}'")
            except KeyError:
                print(f"Erro: variável '{var}' não encontrada em var_types.")
                parser.success = False
        else:
            print(f"Erro: tipo desconhecido '{tipo}' para a variável '{var}'")
            parser.success = False
    if not parser.success:
        return
    final_code = init_code + p[5]
    print("\n".join(final_code))

# VARIÁVEIS #######################################################

def p_no_var_declaration(p):
    """
    Var_Declaration :
    """
    p[0] = []

def p_var_declaration(p):
    """
    Var_Declaration : VAR Var_Lines
    """
    p[0] = p[2]

def p_var_lines_empty(p):
    """
    Var_Lines : 
    """
    p[0] = []

def p_var_lines(p): 
    """
    Var_Lines : Var_Lines Var_Line
              | Var_Line
    """
    if len(p) == 3:
        p[0] = p[1] + p[2]  
    else:
        p[0] = p[1]

def p_var_line(p):
    """
    Var_Line : Var_Names ':' Type ';'
    """
    var_type = p[3]
    vars_info = []
    for name in p[1]:
        if name in parser.regists:
            print(f"Erro: variável '{name}' já declarada.")
            parser.success = False
        else:
            try:
                if isinstance(var_type, tuple) and var_type[0] == 'array':
                    start, end, element_type = var_type[1], var_type[2], var_type[3]
                    size = end - start + 1
                    parser.regists[name] = parser.index
                    parser.index += size
                    parser.var_types[name] = ('array', start, end, element_type)
                    vars_info.append((name, 'array'))
                else:
                    parser.regists[name] = parser.index
                    parser.index += 1
                    parser.var_types[name] = var_type
                    vars_info.append((name, var_type))
            except Exception as e:
                print(f"Erro ao processar variável '{name}': {e}")
                parser.success = False
    p[0] = vars_info

def p_type(p):
    """
    Type : INTEGER
         | STRING
         | BOOLEAN
    """
    p[0] = p[1]

def p_type_array(p):
    """
    Type : ARRAY '[' number dotdot number ']' OF Type
    """
    if p[3] > p[5]:
        print(f"Erro: limites inválidos para array: {p[3]}..{p[5]}")
        parser.success = False
        p[0] = None
    else:
        p[0] = ('array', p[3], p[5], p[8])  

def p_var_names(p):
    """
    Var_Names : Var_Names ',' identifier
    """
    if p[3] in p[1]:
        print(f"Erro: variável '{p[3]}' duplicada na mesma declaração.")
        parser.success = False
    p[0] = p[1] + [p[3]]

def p_var_names_single(p):
    """
    Var_Names : identifier
    """
    p[0] = [p[1]]

#################################################################

# ESTRUTURA #####################################################

def p_code(p):
    """
    Code : BEGIN Lines_Of_Code END '.'
    """
    if not isinstance(p[2], list):
        print("Erro: código inválido dentro do bloco BEGIN...END.")
        parser.success = False
        p[0] = []
    else:
        p[0] = ['START'] + p[2] + ['STOP']

#################################################################

# CÓDIGO ########################################################

def p_lines_of_code_empty(p):
    """
    Lines_Of_Code : 
    """
    p[0] = []

def p_lines_of_code(p):
    """
    Lines_Of_Code : Program_Line_Sequence
                  | Program_Line_Sequence Program_Line_No_Semi_Colon
                  | Program_Line_No_Semi_Colon
    """
    if len(p) == 3:
        p[0] = p[1] + p[2]
    else:
        p[0] = p[1]

def p_program_line_sequence(p):
    """
    Program_Line_Sequence : Program_Line_Sequence Program_Line
                          | Program_Line
    """
    if len(p) == 3:
        p[0] = p[1] + p[2]
    else:
        p[0] = p[1]

def p_program_line(p):
    """
    Program_Line : Write_Line ';'
                 | Write_Line_No_ln ';'
                 | Read_Line ';'
                 | If_Statement ';'
                 | Assignment ';'
                 | Read_Line_ln ';'
                 | Block ';'
                 | For_Statement ';'
                 | While_Statement ';'
    """
    p[0] = p[1]

def p_program_line_no_semi_colon(p):
    """
    Program_Line_No_Semi_Colon : Write_Line
                               | Write_Line_No_ln
                               | Read_Line
                               | If_Statement_Complete
                               | If_Statement_Incomplete
                               | Assignment
                               | Read_Line_ln
                               | Block
                               | For_Statement
                               | While_Statement
    """
    p[0] = p[1]

#################################################################

# WRITELN #######################################################

def gerar_codigo_write(args):
    code = []
    for arg in args:
        if isinstance(arg, str) and arg.startswith('"'):
            code.append(f'PUSHS {arg}')
            code.append('WRITES')

        elif isinstance(arg, tuple) and arg[0] == 'var':
            var_name, tipo = arg[1], arg[2]
            if var_name not in parser.regists:
                print(f"Erro: variável '{var_name}' não declarada.")
                parser.success = False
                continue
            var_index = parser.regists[var_name]
            code.append(f'PUSHG {var_index}')
            if tipo == 'integer' or tipo == 'boolean':
                code.append('WRITEI')
            elif tipo == 'real':
                code.append('WRITEF')
            elif tipo == 'string':
                code.append('WRITES')
            else:
                print(f"Erro: tipo '{tipo}' não suportado em WRITELN.")
                parser.success = False

        elif isinstance(arg, tuple) and arg[0] == 'array_elem':
            access_code = arg[1]
            elem_type = arg[2]
            code += access_code
            if elem_type == 'integer' or elem_type == 'boolean':
                code.append('WRITEI')
            elif elem_type == 'real':
                code.append('WRITEF')
            elif elem_type == 'string':
                code.append('WRITES')
            else:
                print(f"Erro: tipo de elemento '{elem_type}' não suportado em WRITELN.")
                parser.success = False
        else:
            print(f"Erro: argumento inválido '{arg}' em WRITELN.")
            parser.success = False
    return code

def p_write_line(p):
    """
    Write_Line : WRITELN '(' Write_Args ')' 
    """
    p[0] = gerar_codigo_write(p[3]) + ['WRITELN']

def p_write_line_no_ln(p):
    """
    Write_Line_No_ln : WRITE '(' Write_Args ')' 
    """
    p[0] = gerar_codigo_write(p[3])

def p_write_args_multiple(p):
    """
    Write_Args : Write_Args ',' Write_Arg
    """
    p[0] = p[1] + [p[3]]

def p_write_args_single(p):
    """
    Write_Args : Write_Arg
    """
    p[0] = [p[1]]

def p_write_arg_argument(p):
    """
    Write_Arg : argument
    """
    p[0] = f'"{p[1]}"' 

def p_write_arg_identifier(p):
    """
    Write_Arg : identifier
    """
    var_name = p[1]
    if var_name not in parser.regists:
        print(f"Erro: variável '{var_name}' não declarada.")
        parser.success = False
        p[0] = ('var', -1, None)
    else:
        tipo = parser.var_types[var_name]
        p[0] = ('var', var_name, tipo)

def p_write_arg_array(p):
    """
    Write_Arg : identifier '[' Expression ']'
    """
    var_name = p[1]
    index_code, index_type = p[3]

    if var_name not in parser.regists or parser.var_types[var_name][0] != 'array':
        print(f"Erro: variável '{var_name}' não é um array ou não foi declarada.")
        parser.success = False
        p[0] = ('array_elem', [], 'integer') 
        return

    if index_type != 'integer':
        print(f"Erro: índice de array '{var_name}' deve ser do tipo integer, mas recebeu '{index_type}'.")
        parser.success = False

    var_info = parser.var_types[var_name]
    base_address = parser.regists[var_name]
    start_index = var_info[1]
    element_type = var_info[3]

    access_code = ["PUSHGP"] + index_code + [f"PUSHI {start_index - base_address}", "SUB", "LOADN"]

    p[0] = ('array_elem', access_code, element_type)

#################################################################

# READ ##########################################################

def p_read_line(p):
    """
    Read_Line : READ '(' identifier ')'
    """
    var_name = p[3]
    if var_name not in parser.regists:
        print(f"Erro: variável '{var_name}' não declarada.")
        parser.success = False
        p[0] = []
        return

    index = parser.regists[var_name]
    var_type = parser.var_types[var_name]

    code = ["READ"]
    if var_type == "integer" or var_type == "boolean":
        code.append("ATOI")
    elif var_type == "real":
        code.append("ATOF")
    elif var_type == "string":
        pass  
    else:
        print(f"Erro: tipo '{var_type}' não suportado em READ.")
        parser.success = False
    code.append(f"STOREG {index}")

    p[0] = code

def p_read_line_ln(p):
    """
    Read_Line_ln : READLN '(' identifier ')'
    """
    var_name = p[3]
    if var_name not in parser.regists:
        print(f"Erro: variável '{var_name}' não declarada.")
        parser.success = False
        p[0] = []
        return

    index = parser.regists[var_name]
    var_type = parser.var_types[var_name]

    code = ["READ"]
    if var_type == "integer" or var_type == "boolean":
        code.append("ATOI")
    elif var_type == "real":
        code.append("ATOF")
    elif var_type == "string":
        pass  
    else:
        print(f"Erro: tipo '{var_type}' não suportado em READLN.")
        parser.success = False

    code.append(f"STOREG {index}")
    p[0] = code

def p_read_line_array(p):
    """
    Read_Line : READLN '(' identifier '[' Expression ']' ')'
    """
    var_name = p[3]
    index_code, index_type = p[5]

    if var_name not in parser.regists or parser.var_types[var_name][0] != 'array':
        print(f"Erro: variável '{var_name}' não é um array ou não foi declarada.")
        parser.success = False
        return

    if index_type != 'integer':
        print(f"Erro: índice de array '{var_name}' deve ser do tipo integer.")
        parser.success = False

    start = parser.var_types[var_name][1]
    base_address = parser.regists[var_name]
    element_type = parser.var_types[var_name][3]

    code = ["PUSHGP"] + index_code + [f"PUSHI {start - base_address}", "SUB", "READ"]

    if element_type == "integer" or element_type == "boolean":
        code.append("ATOI")
    elif element_type == "real":
        code.append("ATOF")
    elif element_type == "string":
        pass
    else:
        print(f"Erro: tipo de elemento desconhecido '{element_type}' no array '{var_name}'.")
        parser.success = False
        return

    code.append("STOREN")
    p[0] = code

#################################################################

## Expressions ##################################################

def p_expression_binop(p):
    """
    Expression : Expression '+' Expression
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
    """
    ops = {
        '+': 'ADD', '-': 'SUB', '*': 'MUL', '/': 'DIV',
        '>': 'SUP', '<': 'INF', '=': 'EQUAL',
        '<=': 'INFEQ', '>=': 'SUPEQ',
        'div': 'DIV', 'mod': 'MOD',
        'and': 'AND', 'or': 'OR'
    }

    left_code, left_type = p[1]
    right_code, right_type = p[3]
    op = p[2].lower()

    def is_char_literal(code):
        return (
            len(code) == 1 and
            code[0].startswith('PUSHS "') and
            len(code[0]) == len('PUSHS "X"')
        )

    if op in ['=', '<>', '<', '>', '<=', '>=']:
        if is_char_literal(left_code):
            left_code += ["PUSHI 0", "CHARAT"]
            left_type = 'integer'
        if is_char_literal(right_code):
            right_code += ["PUSHI 0", "CHARAT"]
            right_type = 'integer'

    if op in ['+', '-', '*', '/', 'div', 'mod']:
        if left_type != right_type or left_type != 'integer':
            print(f"Erro: operador '{op}' só é permitido entre inteiros.")
            parser.success = False
            p[0] = ([], None)
            return
        result_type = 'integer'
    elif op in ['and', 'or']:
        if left_type != right_type or left_type != 'boolean':
            print(f"Erro: operador lógico '{op}' só funciona com booleanos.")
            parser.success = False
            p[0] = ([], None)
            return
        result_type = 'boolean'
    else: 
        if left_type != right_type:
            print(f"Erro: tipos incompatíveis em operação '{op}': {left_type} e {right_type}")
            parser.success = False
            p[0] = ([], None)
            return
        result_type = 'boolean'

    p[0] = (left_code + right_code + [ops[op]], result_type)

def p_expression_group(p):
    "Expression : '(' Expression ')'"
    p[0] = p[2]

def p_expression_identifier(p):
    "Expression : identifier"
    var = p[1]
    if var not in parser.regists:
        print(f"Erro: variável '{var}' não declarada.")
        parser.success = False
        p[0] = ([], None)
    else:
        tipo = parser.var_types[var]
        p[0] = ([f"PUSHG {parser.regists[var]}"], tipo)

def p_expression_index_access(p):
    "Expression : identifier '[' Expression ']'"
    var_name = p[1]
    index_code, index_type = p[3]

    if var_name not in parser.regists:
        print(f"Erro: variável '{var_name}' não declarada.")
        parser.success = False
        p[0] = ([], None)
        return

    var_type = parser.var_types[var_name]

    if isinstance(var_type, tuple) and var_type[0] == 'array':
        base_address = parser.regists[var_name]
        start = var_type[1]
        elem_type = var_type[3]
        code = ["PUSHGP"] + index_code + [f"PUSHI {start - base_address}", "SUB", "LOADN"]
        p[0] = (code, elem_type)

    elif var_type == 'string':
        base_address = parser.regists[var_name]
        code = [f"PUSHG {base_address}"] + index_code + ["PUSHI 1", "SUB", "CHARAT"]
        p[0] = (code, 'integer') 

    else:
        print(f"Erro: acesso por índice só é permitido para arrays ou strings. Tipo encontrado: {var_type}")
        parser.success = False
        p[0] = ([], None)

def p_expression_int(p):
    "Expression : number"
    p[0] = ([f"PUSHI {p[1]}"], 'integer')

def p_expression_string(p):
    "Expression : argument"
    p[0] = ([f'PUSHS "{p[1]}"'], 'string')

def p_expression_true(p):
    "Expression : TRUE"
    p[0] = (["PUSHI 1"], 'boolean')

def p_expression_false(p):
    "Expression : FALSE"
    p[0] = (["PUSHI 0"], 'boolean')

def p_expression_not(p):
    "Expression : NOT Expression"
    expr_code, expr_type = p[2]
    if expr_type != 'boolean':
        print("Erro: operador NOT só pode ser aplicado a booleanos.")
        parser.success = False
        p[0] = ([], None)
    else:
        p[0] = (expr_code + ["NOT"], 'boolean')

def p_expression_length(p):
    "Expression : LENGTH '(' identifier ')'"
    var_name = p[3]
    if var_name not in parser.regists:
        print(f"Erro: variável '{var_name}' não declarada.")
        parser.success = False
        p[0] = ([], None)
        return

    var_type = parser.var_types[var_name]
    if var_type != 'string' and (not isinstance(var_type, tuple) or var_type[0] != 'array'):
        print(f"Erro: LENGTH só pode ser usado com strings ou arrays. Tipo encontrado: {var_type}")
        parser.success = False
        p[0] = ([], None)
        return

    p[0] = ([f"PUSHG {parser.regists[var_name]}", "STRLEN"], 'integer')

#################################################################

## ASSIGNEMENT ##################################################

def p_assignment(p):
    """
    Assignment : identifier assign Expression
    """
    var = p[1]
    expr_code, expr_type = p[3]

    if var not in parser.regists:
        print(f"Erro: variável '{var}' não declarada.")
        parser.success = False
        p[0] = []
        return

    var_type = parser.var_types[var]
    if var_type != expr_type:
        print(f"Erro: atribuição incompatível. Variável '{var}' é '{var_type}' mas expressão é '{expr_type}'.")
        parser.success = False

    p[0] = expr_code + [f"STOREG {parser.regists[var]}"]


#################################################################

## BLOCKS #######################################################

def p_block(p):
    """
    Block : BEGIN Lines_Of_Code END
    """
    p[0] = p[2]

#################################################################

## IF ELSE BLOCKS ###############################################

def p_if_statement(p):
    """
    If_Statement : If_Statement_Complete
                 | If_Statement_Incomplete
    """
    p[0] = p[1]

def p_if_statement_complete(p):
    """
    If_Statement_Complete : IF Expression THEN Program_Line_No_Semi_Colon ELSE Program_Line_No_Semi_Colon
    """
    expr_code, expr_type = p[2]
    if expr_type != 'boolean':
        print("Erro: expressão condicional do IF deve ser do tipo boolean.")
        parser.success = False

    then_code = p[4]
    else_code = p[6]
    label_else = f"L{len(parser.labels)}"
    label_end = f"L{len(parser.labels) + 1}"
    parser.labels += [label_else, label_end]

    p[0] = (
        expr_code +
        [f"JZ {label_else}"] +
        then_code +
        [f"JUMP {label_end}", f"{label_else}:"] +
        else_code +
        [f"{label_end}:"]
    )

def p_if_statement_incomplete(p):
    """
    If_Statement_Incomplete : IF Expression THEN Program_Line_No_Semi_Colon
    """
    expr_code, expr_type = p[2]
    if expr_type != 'boolean':
        print("Erro: expressão condicional do IF deve ser do tipo boolean.")
        parser.success = False

    then_code = p[4]
    label_end = f"L{len(parser.labels)}"
    parser.labels.append(label_end)

    p[0] = expr_code + [f"JZ {label_end}"] + then_code + [f"{label_end}:"]

#################################################################

## FOR STATEMENT ################################################

def p_for_statement(p):
    """
    For_Statement : FOR identifier assign Expression TO Expression DO Program_Line_No_Semi_Colon
                  | FOR identifier assign Expression DOWNTO Expression DO Program_Line_No_Semi_Colon
    """
    var_name = p[2]
    start_expr_code, start_type = p[4]
    end_expr_code, end_type = p[6]
    body_code = p[8]

    if var_name not in parser.regists:
        print(f"Erro: variável '{var_name}' não declarada.")
        parser.success = False
        p[0] = []
        return

    if start_type != 'integer' or end_type != 'integer':
        print("Erro: expressão de início e fim do FOR devem ser do tipo integer.")
        parser.success = False

    var_index = parser.regists[var_name]
    label_start = f"L{len(parser.labels)}"
    label_end = f"L{len(parser.labels)+1}"
    parser.labels += [label_start, label_end]

    code = []
    code += start_expr_code
    code.append(f"STOREG {var_index}")
    code.append(f"{label_start}:")
    code.append(f"PUSHG {var_index}")
    code += end_expr_code

    if p[5].lower() == "to":
        code.append("INFEQ")
    elif p[5].lower() == "downto":
        code.append("SUPEQ")

    code.append(f"JZ {label_end}")
    code += body_code
    code.append(f"PUSHG {var_index}")
    if p[5].lower() == "to":
        code.append("PUSHI 1")
        code.append("ADD")
    elif p[5].lower() == "downto":
        code.append("PUSHI 1")
        code.append("SUB")
    code.append(f"STOREG {var_index}")
    code.append(f"JUMP {label_start}")
    code.append(f"{label_end}:")

    p[0] = code

#################################################################

## WHILE STATEMENT ##############################################

def p_statement_while(p):
    "While_Statement : WHILE Expression DO Program_Line_No_Semi_Colon"
    expr_code, expr_type = p[2]
    if expr_type != 'boolean':
        print("Erro: condição do WHILE deve ser do tipo boolean.")
        parser.success = False

    label_start = f"L{len(parser.labels)}"
    label_end = f"L{len(parser.labels) + 1}"
    parser.labels += [label_start, label_end]

    code = []
    code.append(f"{label_start}:")
    code += expr_code
    code.append(f"JZ {label_end}")
    code += p[4]
    code.append(f"JUMP {label_start}")
    code.append(f"{label_end}:")

    p[0] = code

#################################################################

def p_error(p):
    if p:
        print(f"Erro de sintaxe próximo ao token '{p.value}' na linha {p.lineno}.")
    else:
        print("Erro de sintaxe: entrada inesperada.")
    parser.success = False

parser = yacc.yacc(debug=True)

parser.index = 0
parser.regists = {}
parser.var_types = {}
parser.labels = []

import sys
try:
    texto = sys.stdin.read()
    parser.success = True
    parser.parse(texto)
    if parser.success:
        print("\nFrase válida: ", texto)
    else:
        print("Frase inválida... Corrija e tente novamente!")
except Exception as e:
    print(f"Erro ao processar entrada: {e}")
    parser.success = False
