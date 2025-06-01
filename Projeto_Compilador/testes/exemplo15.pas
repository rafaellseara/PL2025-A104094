program MaiorArray;
var
    numeros: array[1..5] of integer;
    i, maior: integer;
begin
    writeln('Introduza 5 números inteiros:');
    for i := 1 to 5 do
    begin
        readln(numeros[i]);
        if (i = 1) or (numeros[i] > maior) then
            maior := numeros[i];
    end;

    writeln('O maior número é: ', maior);
end.