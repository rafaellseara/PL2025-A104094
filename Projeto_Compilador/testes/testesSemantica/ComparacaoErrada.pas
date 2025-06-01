program IfNaoBooleano;
var
  x: integer;
begin
  x := 7;
  if x then        { ERRO: condição não é boolean }
    writeln('Isto deve falhar');
end.
