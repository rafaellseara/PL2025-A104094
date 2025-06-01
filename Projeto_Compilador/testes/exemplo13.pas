program NumeroPerfeito;
var
    num, i, soma: integer;
begin
    writeln('Introduza um número inteiro positivo:');
    readln(num);
    soma := 0;
    i := 1;
    while i <= (num div 2) do
        begin
            if (num mod i) = 0 then
                soma := soma + i;
            i := i + 1;
        end;
    if soma = num then
        writeln(num, ' é um número perfeito')
    else
        writeln(num, ' não é um número perfeito');
end.