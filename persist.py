#!pip install sqlalchemy
import sqlalchemy

sqlalchemy.__version__

# Conexão do banco de dados
engine = sqlalchemy.create_engine('sqlite:///userdata.db',echo=True) # sqlite já vem instalado com python, dispensa instalar drivers ou outros programas
# o echo=True permite ver as operações como sql

# declarando o mapeamento
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String
Base = declarative_base()

class User(Base): # vamos criar a classe para adicionar usuários no banco
    
    __tablename__ = 'users' # criando a tabela users *obrigatório*
    
    id = Column(Integer, primary_key=True) # criando uma coluna chamada id, definindo como inteiro e config. como chave primária
    name = Column(String(50)) # criando uma coluna chamada name do tipo string com 50 caracteres
    fullname = Column(String(50))
    age = Column(Integer)
    
class Medicine(Base): # vamos criar a classe para adicionar usuários no banco
    
    __tablename__ = 'users' # criando a tabela users *obrigatório*
    
    id = Column(Integer, primary_key=True) # criando uma coluna chamada id, definindo como inteiro e config. como chave primária
    name = Column(String(50)) # criando uma coluna chamada name do tipo string com 50 caracteres
    fullname = Column(String(50))
    quantity = Column(Integer)
    times_taken = {
        '07:00':'1 cp',
    }
    
# criar a tabela no banco de dados
Base.metadata.create_all(engine)