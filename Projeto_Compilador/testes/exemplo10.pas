program Soma2;
var
    num1, num2, soma: Integer;
begin
    { Ler 2 números }
    Write('Introduza o primeiro número: ');
    ReadLn(num1);

    Write('Introduza o segundo número: ');
    ReadLn(num2);

    { Calcular a soma }
    soma := num1 + num2;

    { Escrever o resultado }
    WriteLn('A soma é: ', soma);
end.