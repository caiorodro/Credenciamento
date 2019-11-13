
from sqlalchemy import create_engine
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import MetaData
from sqlalchemy import String, Table, Integer, Numeric, DateTime, BLOB
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import mapper
import json
from app.base.mapTable import mapUser, mapLogger, mapEmpresaContratante, mapEvento, mapConvidado, mapCredenciamento
import datetime
from decimal import Decimal
from venv.config import DevelopmentConfig as config

strConn = ''.join((config.DB_USERNAME, ':', config.DB_PASSWORD, '@', config.DB_SERVER_NAME, '/', config.DB_NAME))

engine = create_engine('mysql+pymysql://' + strConn, isolation_level="READ UNCOMMITTED")

metadata = MetaData()
Session = sessionmaker(bind=engine)
session = Session()

tables = []

user = Table('tb_user', metadata,
    Column('ID_USER', Integer, primary_key=True, autoincrement='auto'),
    Column('NAME_USER', String(60), nullable=False),
    Column('PASSWORD1', String(150), nullable=True),
    Column('EMAIL', String(100), nullable=True),
    Column('USER_ENABLED', Integer, nullable=True),
    Column('KIND_OF_USER', Integer, nullable=True))

tb_logger = Table('tb_logger', metadata,
    Column('ID_LOG', Integer, primary_key=True, autoincrement='auto'),
    Column('ID_USER', Integer, nullable=True),
    Column('DATE_OF', DateTime, nullable=True),
    Column('MESSAGE1', String(3000), nullable=False),
    Column('LEVEL1', String(10), nullable=False),
    Column('TRACE', String(3000), nullable=False))

tb_empresa_contratante = Table('tb_empresa_contratante', metadata,
    Column('ID_EMPRESA', Integer, primary_key=True, autoincrement='auto'),
    Column('RAZAO_SOCIAL', String(100), nullable=True),
    Column('NOME_FANTASIA', String(35), nullable=True),
    Column('CNPJ', String(20), nullable=False),
    Column('IE', String(15), nullable=False),
    Column('ENDERECO', String(100), nullable=False),
    Column('NUMERO', String(15), nullable=False),
    Column('COMPLEMENTO', String(20), nullable=False),
    Column('CEP', String(10), nullable=False),
    Column('MUNICIPIO', String(80), nullable=False),
    Column('UF', String(2), nullable=False),
    Column('EMAIL', String(70), nullable=False),
    Column('TELEFONE', String(30), nullable=False),
    Column('CONTATO', String(50), nullable=False))

tb_evento = Table('tb_evento', metadata,
    Column('ID_EVENTO', Integer, primary_key=True, autoincrement='auto'),
    Column('ID_EMPRESA', Integer, ForeignKey('tb_empresa_contratante.ID_EMPRESA')),
    Column('DATA_EVENTO', DateTime, nullable=True),
    Column('TITULO_EVENTO', String(150), nullable=True),
    Column('OBSERVACAO', String(2000), nullable=True)
)

tb_convidado = Table('tb_convidado', metadata,
    Column('ID_CONVIDADO', Integer, primary_key=True, autoincrement='auto'),
    Column('ID_EVENTO', Integer, ForeignKey('tb_evento.ID_EVENTO')),
    Column('NOME_CONVIDADO', String(80), nullable=True),
    Column('CELULAR_CONVIDADO', String(20), nullable=True)
)

tb_credenciamento = Table('tb_credenciamento', metadata,
    Column('ID_CREDENCIAMENTO', Integer, primary_key=True, autoincrement='auto'),
    Column('ID_EVENTO', Integer, ForeignKey('tb_evento.ID_EVENTO')),
    Column('ID_CONVIDADO', Integer, ForeignKey('tb_convidado.ID_CONVIDADO')),
    Column('DATA_HORA', DateTime, nullable=True),
    Column('PRESENTE', Integer, nullable=True)
)

tables.append([mapUser, user])
tables.append([mapLogger, tb_logger])
tables.append([mapEmpresaContratante, tb_empresa_contratante])
tables.append([mapEvento, tb_evento])
tables.append([mapConvidado, tb_convidado])
tables.append([mapCredenciamento, tb_credenciamento])

def mapAllTables():
    [mapper(table[0], table[1]) for table in tables]

def connect():
    try:
        return engine.connect()
    except Exception:
        raise Exception('Cannot connect on database')

def close():
    try:
        engine.close()
    except Exception:
        pass

conn = connect()
mapAllTables()
