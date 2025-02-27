import re
import sys

def markdown_para_html_ficheiro(ficheiro_md: str, ficheiro_html: str) -> None:
    with open(ficheiro_md, 'r', encoding='utf-8') as f:
        linhas = f.readlines()

    html = []
    lista_numerada = False

    for linha in linhas:
        linha = linha.strip()
        
        if lista_numerada and not re.match(r'^(\d+)\.\s+(.*)', linha):
            html.append("</ol>")
            lista_numerada = False

        # Cabeçalhos
        match_h3 = re.match(r'^(###)\s+(.*)', linha)
        match_h2 = re.match(r'^(##)\s+(.*)', linha)
        match_h1 = re.match(r'^(#)\s+(.*)', linha)

        if match_h3:
            texto = match_h3.group(2)
            html.append(f"<h3>{texto}</h3>")
        elif match_h2:
            texto = match_h2.group(2)
            html.append(f"<h2>{texto}</h2>")
        elif match_h1:
            texto = match_h1.group(2)
            html.append(f"<h1>{texto}</h1>")

        # Lista numerada
        elif re.match(r'^(\d+)\.\s+(.*)', linha):
            if not lista_numerada:
                html.append("<ol>")
                lista_numerada = True
            match_lista = re.match(r'^(\d+)\.\s+(.*)', linha)
            item = match_lista.group(2)
            html.append(f"<li>{item}</li>")
        else:
            # Links
            linha = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', linha)

            # Imagens
            linha = re.sub(r'!\[(.*?)\]\((.*?)\)', r'<img src="\2" alt="\1"/>', linha)

            # Bold
            linha = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', linha)

            # Itálico
            linha = re.sub(r'\*(.*?)\*', r'<i>\1</i>', linha)

            html.append(linha)

    if lista_numerada:
        html.append("</ol>")

    with open(ficheiro_html, 'w', encoding='utf-8') as f:
        f.write('\n'.join(html))


def main():
    md_file = sys.argv[1]
    html_file = sys.argv[2]
    markdown_para_html_ficheiro(md_file, html_file)

if __name__ == '__main__':
    main()
