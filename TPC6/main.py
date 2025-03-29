from ana_sin import tokenize, parse_expression
from calculation import calc

def main():
    expr = input("Expr: ")
    try:
        tokens = tokenize(expr)
        print("Tokens:", tokens)
        ast, resto = parse_expression(tokens)
        if resto:
            print("Erro: tokens não consumidos:", resto)
        else:
            print("AST:", ast)
            print("Resultado:", calc(ast))
    except Exception as e:
        print("Erro:", e)

if __name__ == "__main__":
    main()