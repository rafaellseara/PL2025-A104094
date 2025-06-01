program CondicaoComposta;
var
  x: integer;
  b: boolean;
begin
  x := 10;
  b := (x > 5) and (x < 20);
  if b then
    writeln('x está entre 5 e 20');
end.
