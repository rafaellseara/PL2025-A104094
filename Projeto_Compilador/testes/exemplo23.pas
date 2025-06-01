program SomaArray;
var
    numeros: array[1..5] of integer;
    i, soma: integer;
begin
    writeln('Introduza 5 números:');
    for i := 1 to 5 do
        readln(numeros[i]);

    soma := 0;
    for i := 1 to 5 do
        soma := soma + numeros[i];

    writeln('A soma é: ', soma);
end.
