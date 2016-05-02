Primeiro trabalho de busca da recuperação e informação
Aluno: Jorge Rama Krsna Mandoju

Como foi pedido no problema , foi calculada a distancia no modulo do buscador (o qual é o complemento da similaridade).
Ou seja, quanto menor a distância dos cossenos, mais similares são,melhor resultado.
Formula : Distancia dos cossenos = 1 - similaridade dos cossenos.
(Apesar de normalmente utilizar similaridade nas consultas e até em sala de aula foi usado isso,
optei por utilizar distância pois está escrito no problema "O terceiro elemento é a distância do elemento para a consulta")

Foi utilizado o python 3.5 anaconda que já possui várias bibliotecas instaladas.



Módulos não padrão do python 3.5 utilizadas:
 - Numpy
 - scipy
 - lxml
 - unidecode

Para facilitar a leitura do python , foi utilizado a biblioteca configparser ( que é nativa do python) para ler os arquivos cfg.
Porém é nescessário colocar a cláusula [DEFAULT] no início de cada arquivo .CFG para ler corretamente.

Cada arquivo .py corresponde a um modulo do exercício, e são respectivamente:
 - gerador_lista_invertida.py   -> gerador lista invertida
 - indexador.py -> indexador
 - processador_de_consulta.py -> processador de consulta
 - buscador.py -> buscador

os arquivos .cfg para rodar o mesmo estão na raiz.
Existem três pastas no projeto com vários arquivos, elas tem basicamente as funções:
 - db -> onde se localiza todos os arquivos da base de teste CysticFibrosis2
 - log -> onde ficam todos os logs gerados pelos módulos
 - out -> onde ficam os arquivos de saída que são gerados pelos módulos

Apesar dos arquivos de saída ficarem no out não é nescessario que fiquem no out, apenas foi configurado os cfg para ficarem na pasta usando "out\arquivo.csv"