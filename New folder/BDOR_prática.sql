-- 1) definir os seguintes TADs e tabelas:

create type TEnd as (
  ruaNro text,
  cidade text,
  cep numeric(8)
);

create type TProfessor as (
 cpf numeric(11),
 nome text,
 DN date,
 endereco TEnd,
 matricula int,
 areas text ARRAY
);

create type TAluno as (
  cpf numeric(11),
  nome text, 
  DN date, 
  endereco TEnd,
  matricula int,
  orientador int
);

create table professores OF TProfessor
(primary key(matricula));
 
create TABLE alunos of TAluno
(Primary key(matricula), FOREIGN KEY(orientador) REFERENCES professores);

-- 2) Inserir os seguintes professores (CPF, nome, DN, endereco,matricula, areas):

INSERT INTO professores 
values (1112233344, 'Ronaldo Mello', '1/1/1981', ROW('Rua A, 11', 'Florianopolis', 88000005), 116780, '{"NoSQL", "JSON", "BD"}');
        
INSERT INTO professores 
values (22233344455, 'Carina Dorneles', '2/2/1982', ROW('Rua B, 22', 'Florianopolis', 88111005), 122540, '{"Web", "BD"}');
        
INSERT INTO professores 
values (33344455566, 'Renato Fileto', '1/1/1981', ROW('Rua C, 33', 'Lages', 88222005), 133872, '{"Web", "Semantica", "BD"}');

-- 3) Inserir os seguintes alunos (CPF, nome, DN, endereco,matricula, orientador):

INSERT INTO alunos
VALUES (44455566677, 'Alexandre Heckert Lentz', '3/3/2003', ROW('Rua D, 44', 'Florianopolis',88001105), 0201111, 116780);

INSERT INTO alunos
VALUES (55566677788, 'Bruno Duarte de Borja', '4/4/2003', ROW('Rua E, 55', 'Florianopolis',88001105), 0202222, 122540);
        
INSERT INTO alunos
VALUES (66677788899, 'Julia Fernanda Werlang', '5/5/2003', ROW('Rua F, 66', 'Palhoca', 88220005), 0203333, 116780);

INSERT INTO alunos
VALUES (7778889900, 'Petterson Pereira da Rosa', '6/6/2003', ROW('Rua G, 77', 'Biguacu', 88020005), 0204444, 133872);

-- 4) Realizar as seguintes consultas:

SELECT * FROM alunos
WHERE (endereco).cep = 88001105;

-- b) buscar as 2 primeiras áreas de atuação dos professores;
SELECT nome, ARRAY(SELECT unnest(areas) LIMIT 2) AS duas_primeiras_areas
FROM professores;

-- c) buscar o nome da cidade dos orientandos do professor Ronaldo Mello;
SELECT (endereco).cidade
FROM alunos
WHERE orientador = (SELECT matricula FROM professores WHERE nome = 'Ronaldo Mello');

-- d) buscar o nome dos professores que atuam na área Web. 
SELECT nome
FROM professores
WHERE 'Web' = ANY(areas);


