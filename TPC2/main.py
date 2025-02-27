import sys
import re

def parse_csv(content):
    compositores = set()
    distribuicao_periodos = {}
    obras_por_periodo = {}
    
    lined_content = re.sub(r'\n\s+', ' ', content, flags=re.DOTALL)
    split_content = lined_content.split("\n")
    
    for line in split_content:
        splited_line = re.split(r';(?=(?:[^"]*"[^"]*")*[^"]*$)', line)
        
        compositores.add(splited_line[4])
        
        if splited_line[3] in obras_por_periodo:
            obras_por_periodo[splited_line[3]].add(splited_line[0])
        else:
            obras_por_periodo[splited_line[3]] = {splited_line[0]}
            
        if splited_line[3] in distribuicao_periodos:
            distribuicao_periodos[splited_line[3]] += 1
        else:
            distribuicao_periodos[splited_line[3]] = 1
            
    return sorted(compositores), str(distribuicao_periodos), str(obras_por_periodo)
            
        
            
        

def main():
    with open(sys.argv[1], encoding="utf-8") as f:
        next(f)
        content = f.read()

    compositores_ordenados, distribuicao_periodos, obras_por_periodo = parse_csv(content)
    
    print("\nLista ordenada alfabeticamente de compositores:")
    for compositor in compositores_ordenados:
        print(f"Compositor: {compositor}")
        
    print("\nDistribuição de obras por período:")
    for periodo, obras in eval(obras_por_periodo).items():
        print(f"Período: {periodo} - Obras: {obras}")
        
    print("\nNúmero de obras por período:")
    for periodo, num in eval(distribuicao_periodos).items():
        print(f"Período: {periodo} - Numero: {num}")
    

    
if __name__ == "__main__":
    main()