import ply.lex as lex
import sys
import json
from datetime import date

tokens = (
    "LISTAR",
    "SELECIONAR",
    "MOEDA",
    "NOTA",
    "SAIR"
)

stock = {}
coins = {}
notes = {}

t_ignore = ' \t\n'

def t_LISTAR(t): r'LISTAR'; return t
def t_SAIR(t): r'SAIR'; return t
def t_SELECIONAR(t): r'SELECIONAR[ ]+[a-zA-Z0-9]+'; return t
def t_MOEDA(t): r'MOEDA\s+((1e|2e|50c|20c|10c|5c|2c|1c),?\s*)+'; return t
def t_NOTA(t): r'NOTA\s+([5e|10e|20e|50e|100e|200e|500e],?\s*)+'; return t
def t_error(t): print(f"Caracter Ilegal {t.value[0]}"); t.lexer.skip(1)

def LISTAR():
    print('     Number        |                Name                |       Stock       |    Price    ')
    print('--------------------------------------------------------------------------------------------------------')
    for product in stock.values():
        print(f"        {product['cod']}        |     {product['nome']: <30} |         {product['quant']: <5}     |      {product['preco']: <5}")
        
def TROCO(saldo):
    valores = [50, 20, 10, 5, 2, 1, 0.50, 0.20, 0.10, 0.05, 0.02, 0.01]
    troco = []

    for valor in valores:
        quant = int(saldo // valor)  
        if quant > 0:
            troco.append(f"{quant}x {int(valor) if valor >= 1 else int(valor * 100)}{'e' if valor >= 1 else 'c'}")
            saldo = round(saldo - quant * valor, 2)

    return ", ".join(troco)

     
def save_to_json(file_path: str):
    data = {
        "stock": list(stock.values()),
        "moedas": list(coins.values()),
        "notas": list(notes.values())
    }
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)
     
def vending_machine(file_path: str):
    print(f"maq: {date.today()} Stock carregado, Estado atualizado.")
    print("maq: Bom dia. Estou disponível para atender o seu pedido")
    lexer = lex.lex()
    saldo = 0

    for line in sys.stdin:
        lexer.input(line)

        for token in lexer:
            if token.type == "LISTAR":
                LISTAR()
                
            elif token.type == "SELECIONAR":
                cod = token.value.split()[1]
                product = stock.get(cod)
                if not product:
                    print(f"Produto não encontrado.")
                    continue
                if saldo == 0:
                    print(f"O Preço do produto é: {product['preco']:.2f}€")
                    continue
                if saldo < product["preco"]:
                    print(f"maq: Saldo insuficiente para satisfazer o seu pedido.")
                    print(f"maq: Saldo = {saldo:.2f}€ Pedido = {product['preco']:.2f}€")
                    continue
                if product["quant"] == 0:
                    print(f"Produto esgotado.")
                    continue
                product["quant"] -= 1
                saldo -= product["preco"]
                print(f"Produto: {product['nome']} - {product['preco']:.2f}€")
                print(f"Saldo restante: {saldo:.2f}€")
                
            elif token.type == "MOEDA":
                moedas_str = " ".join(token.value.split()[1:])
                moedas = moedas_str.split(",")
                for moeda in moedas:
                    moeda = moeda.strip()
                    if moeda:
                        if moeda.endswith('e'):
                            valor = int(moeda[:-1])
                            coin = next((c for c in coins.values() if c["valor"] == valor), None)
                            if coin:
                                coin["quant"] += 1
                            saldo += valor
                        elif moeda.endswith('c'):
                            cents = int(moeda[:-1])
                            valor = cents / 100.0
                            coin = next((c for c in coins.values() if c["valor"] == valor), None)
                            if coin:
                                coin["quant"] += 1
                            saldo += valor
                print(f"Saldo: {saldo:.2f}€")
                
            elif token.type == "NOTA":
                notas_str = " ".join(token.value.split()[1:])
                notas = notas_str.split(",")
                for nota in notas:
                    nota = nota.strip()
                    if nota:
                        if nota.endswith('e'):
                            valor_str = nota[:-1]
                            valor = int(valor_str)
                            if valor not in [5, 10, 20]:
                                print(f"Nota inválida. Adicione notas de 5, 10 ou 20.")
                                continue
                            note = next((n for n in notes.values() if n["valor"] == valor), None)
                            if note:
                                note["quant"] += 1
                            saldo += valor
                print(f"Saldo: {saldo:.2f}€")
                
            elif token.type == "SAIR":
                if saldo > 0:
                    troco = TROCO(saldo)
                    print(f"maq: Pode retirar o troco: {troco}")
                print("maq: Até à próxima!")
                save_to_json(file_path)
                exit(0)
            

     
def storage(data):
    for product in data["stock"]:
        stock[product["cod"]] = product
    for coin in data["moedas"]:
        coins[coin["valor"]] = coin
    for note in data["notas"]:
        notes[note["valor"]] = note   

def main(argv):
    file_path = argv[1]
    with open(file_path, "r") as file:
        data = json.load(file)
        
    storage(data)
    vending_machine(file_path)

if __name__ == "__main__":
    main(sys.argv)