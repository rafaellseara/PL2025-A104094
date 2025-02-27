# TPC3: Conversor de markdown para html

2025-02-27

## Autor:
- Rafael Lopes Seara
- A104094

### Problema
Criar em Python um pequeno conversor de MarkDown para HTML para os elementos descritos na "Basic Syntax" da Cheat Sheet:

Cabeçalhos: linhas iniciadas por ```# texto```, ou ```## texto``` ou ```### texto```
```
In: # Exemplo
Out: <h1>Exemplo</h1>
```
Bold: pedaços de texto entre ```**```:
```
In: Este é um **exemplo** ...
Out: Este é um <b>exemplo</b> ...
```
Itálico: pedaços de texto entre ```*```:
```
In: Este é um *exemplo* ...
Out: Este é um <i>exemplo</i> ...
```

Lista numerada:
```
In:
1. Primeiro item
2. Segundo item
3. Terceiro item

Out:
<ol>
<li>Primeiro item</li>
<li>Segundo item</li>
<li>Terceiro item</li>
</ol>
```

Link: [texto](endereço URL)
```
In: Como pode ser consultado em [página da UC](http://www.uc.pt)
Out: Como pode ser consultado em <a href="http://www.uc.pt">página da UC</a>
```

Imagem: ![texto alternativo](path para a imagem)
```
In: Como se vê na imagem seguinte: ![imagem dum coelho](http://www.coellho.com) ...
Out: Como se vê na imagem seguinte: <img src="http://www.coellho.com" alt="imagem
dum coelho"/> ...
```

### Funcionamento
O programa tem como objetivo converter um ficheiro de texto em Markdown para HTML. Para isso, lê linha a linha o conteúdo do ficheiro e aplica regras de substituição para transformar os elementos de Markdown nos seus equivalentes em HTML.

Inicialmente, o programa recebe como argumento o caminho para o ficheiro de entrada e o caminho para o ficheiro de saída. A função `markdown_para_html_ficheiro` é responsável por ler o ficheiro Markdown, processar cada linha e guardar o resultado num novo ficheiro HTML.

A função percorre as linhas do ficheiro e converte cabeçalhos, texto em negrito e itálico, imagens, links e listas numeradas. Cada tipo de elemento é tratado com expressões regulares que identificam a sintaxe de Markdown e capturam o conteúdo relevante, como o texto do cabeçalho ou o URL de um link. Essas capturas são usadas diretamente na substituição para criar as tags HTML correspondentes.

Os cabeçalhos são reconhecidos pelas expressões regulares que identificam linhas que começam com `#`, `##` ou `###`, seguidos de texto. Consoante o número de `#`, é gerado um `<h1>`, `<h2>` ou `<h3>`.

Quando é detetada uma lista numerada (linhas que começam com "1.", "2.", etc.), o programa garante que a tag `<ol>` seja aberta antes do primeiro item e fechada corretamente quando a lista termina. Para isso, utiliza a variável `lista_numerada`, que controla se o programa já está dentro de uma lista ordenada.

O programa também aplica substituições a elementos inline, como:

Links do formato `[texto](url)` para `<a href="url">texto</a>`
Imagens do formato `![texto alt](url)` para `<img src="url" alt="texto alt"/>`
Texto em negrito entre `**` para `<b>`
Texto em itálico entre `*` para `<i>`
Finalmente, o conteúdo convertido é guardado no ficheiro de saída indicado pelo utilizador.

## Instrução de utilização

- Indicando o path do ficheiro , o programa irá ler do ficheiro e escrever o output no ficheiro indicado
 ```sh
    $ python3 main.py <file_path> <output_name_file>
```