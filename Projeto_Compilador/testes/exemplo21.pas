program RepetirNome;

procedure EscreverVariasVezes(nome: string; vezes: integer);
var
    i: integer;
begin
    for i := 1 to vezes do
        writeln(nome);
end;

var
    meuNome: string;
    repeticoes: integer;

begin
    writeln('Introduza o seu nome:');
    readln(meuNome);
    writeln('Quantas vezes quer escrever o nome?');
    readln(repeticoes);

    EscreverVariasVezes(meuNome, repeticoes);
end.
