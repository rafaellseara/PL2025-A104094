program NumeroArmstrong;
var
    num, temp, digito, soma: integer;
begin
    writeln('Introduza um número inteiro positivo:');
    readln(num);
    soma := 0;
    temp := num;
    while temp > 0 do
        begin
            digito := temp mod 10;
            soma := soma + (digito * digito * digito);
            temp := temp div 10;
        end;
    if soma = num then
        writeln(num, ' é um número de Armstrong')
    else
        writeln(num, ' não é um número de Armstrong');
end.