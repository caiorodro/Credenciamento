
use credenciamento;

CREATE TABLE tb_user (ID_USER int(11) NOT NULL AUTO_INCREMENT,
   EMAIL varchar(120) DEFAULT NULL,
   PASSWORD1 varchar(250) DEFAULT NULL,
   NAME_USER varchar(80) DEFAULT NULL,
   USER_ENABLED int(11) DEFAULT NULL,
   KIND_OF_USER int(11) DEFAULT NULL,
   PRIMARY KEY (ID_USER),
   KEY IDX_EMAIL (EMAIL)
 );
 
 CREATE TABLE tb_empresa_contratante (
   ID_EMPRESA bigint NOT NULL AUTO_INCREMENT,
   RAZAO_SOCIAL varchar(100) DEFAULT NULL,
   NOME_FANTASIA varchar(35) DEFAULT NULL,
   CNPJ varchar(20) DEFAULT NULL,
   IE varchar(15) DEFAULT NULL,
   ENDERECO varchar(100) DEFAULT NULL,
   NUMERO varchar(15) DEFAULT NULL,
   COMPLEMENTO varchar(20) DEFAULT NULL,
   CEP varchar(10) DEFAULT NULL,
   MUNICIPIO varchar(80) DEFAULT NULL,
   UF varchar(2) DEFAULT NULL,
   EMAIL varchar(70) DEFAULT NULL,
   TELEFONE varchar(30) DEFAULT NULL,
   CONTATO varchar(50) DEFAULT NULL,
   PRIMARY KEY (ID_EMPRESA)
 );

 CREATE TABLE tb_logger (
   ID_LOG bigint NOT NULL AUTO_INCREMENT,
   ID_USER int(11) DEFAULT NULL,
   DATE_OF datetime DEFAULT NULL,
   MESSAGE1 varchar(3000) DEFAULT NULL,
   LEVEL1 varchar(10) DEFAULT NULL,
   TRACE varchar(3000) DEFAULT NULL,
   PRIMARY KEY (ID_LOG)
 );

CREATE TABLE tb_evento (
   ID_EVENTO bigint NOT NULL AUTO_INCREMENT,
   ID_EMPRESA bigint DEFAULT NULL,
   DATA_EVENTO datetime DEFAULT NULL,
   TITULO_EVENTO varchar(150) DEFAULT NULL,
   OBSERVACAO varchar(2000) DEFAULT NULL,
   PRIMARY KEY (ID_EVENTO)
 );

CREATE TABLE tb_convidado (
	ID_CONVIDADO bigint NOT NULL AUTO_INCREMENT,
	ID_EVENTO bigint DEFAULT NULL,
    NOME_CONVIDADO varchar(80),
    CELULAR_CONVIDADO varchar(20),
    PRIMARY KEY (ID_CONVIDADO)
);

ALTER TABLE tb_convidado add foreign key (ID_EVENTO) references tb_evento(ID_EVENTO);

insert into tb_user (EMAIL, PASSWORD1, NAME_USER, USER_ENABLED, KIND_OF_USER)
values('caiorodro@gmail.com', 'pbkdf2:sha256:50000$HcLsOBq3$fe148f7ec479aab99efe43a5f468e5a03504244ef3cb81771cdd83808e6cff12',
'Caio Rodrigues', 1, 1);

insert into tb_empresa_contratante (RAZAO_SOCIAL, NOME_FANTASIA, CNPJ, IE, ENDERECO, NUMERO, COMPLEMENTO,
CEP, MUNICIPIO, UF, EMAIL, TELEFONE, CONTATO)
VALUES('DORAN SOFTWARE ME', 'DORAN', '02.967.782/0001-68', 'ISENTO', 'RUA DO ORFANATO', '882', '', '03131-010', 'SAO PAULO', 'SP', 'caiorodro@gmail.com', '11 992640322', '');

CREATE TABLE tb_credenciamento (
	ID_CREDENCIAMENTO bigint NOT NULL AUTO_INCREMENT,
	ID_EVENTO bigint DEFAULT NULL,
    ID_CONVIDADO bigint,
    DATA_HORA datetime,
    PRESENTE int,
    PRIMARY KEY (ID_CREDENCIAMENTO)
);

ALTER TABLE tb_credenciamento add foreign key (ID_EVENTO) references tb_evento(ID_EVENTO);
ALTER TABLE tb_credenciamento add foreign key (ID_CONVIDADO) references tb_convidado(ID_CONVIDADO);
