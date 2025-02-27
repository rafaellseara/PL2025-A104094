# TPC1: Somador on/off

2025-02-10

## Autor:
- Rafael Lopes Seara
- A104094

### Problema
1. Pretende-se um programa que some todas as sequências de dígitos que encontre num texto;
2. Sempre que encontrar a string “Off” em qualquer combinação de maiúsculas e minúsculas, esse comportamento é desligado;
3. Sempre que encontrar a string “On” em qualquer combinação de maiúsculas e minúsculas, esse comportamento é novamente ligado;
4. Sempre que encontrar o caráter “=”, o resultado da soma é colocado na saída.

### Funcionamento
O somador on/off vai percorrendo o texto inserido somando todas as sequencias de digitos que encontre no texto. Caso encontre a string "off" este processo é desligado. Caso encontre a string "on" este processo volta a ser ligado utilizado assim um sistema boleano para identificar se deve somar os digitos ou ignorados. Sempre que encontra o caracter "=" o resultado é colocado na saida.

## Instrução de utilização

 ```sh
    $ python3 main.py <file_path>
```
