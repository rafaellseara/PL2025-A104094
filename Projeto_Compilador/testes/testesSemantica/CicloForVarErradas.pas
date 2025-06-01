program CicloForErro;
var
  i: integer;
begin
  for i := 'a' to 5 do   { ERRO: limite inicial não é inteiro }
    writeln(i);
end.
