program Produto3;
var
    num1, num2, num3, produto: Integer;
begin
    { Ler 3 números }
    Write('Introduza o primeiro número: ');
    ReadLn(num1);

    Write('Introduza o segundo número: ');
    ReadLn(num2);

    Write('Introduza o terceiro número: ');
    ReadLn(num3);

    { Calcular o produto }
    produto := num1 * num2 * num3;
        
    { Escrever o resultado }
    WriteLn('O produto é: ', produto);
end.