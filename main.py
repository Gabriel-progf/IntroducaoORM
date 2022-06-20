from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref
from pprint import pprint
import requests

engine = create_engine('sqlite:///repositorio.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()



class RepoUser(Base):
    __tablename__ = 'repositorios'

    id = Column(Integer, primary_key=True)
    repositorio = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship('UserGit')

    def __repr__(self):
        return  f'RepoUser(repositorio={self.repositorio})'


class UserGit(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    repositorios = relationship(RepoUser, backref='users')

    def __repr__(self):
        return f'UserGit(id={self.id}, name={self.name}, repositorios={self.repositorios})'


Base.metadata.create_all(engine)

resp ='Ss'

while resp in 'Ss':
    name = str(input("User: "))
    usuario = UserGit(name=name)

    r = requests.get(f'https://api.github.com/users/{name}/repos')
    repos = r.json()

    repo_list = list()

    for repo in repos:
        repo_list.append(repo['name'])
        reposit_user = RepoUser(repositorio= repo['name'], user= usuario)
        session.add(reposit_user)

    session.commit()
 
    resp = str(input('Deseja adicionar mais um Usuario e seus repositorios ao banco de dados? (S/N): '))

pprint(session.query(RepoUser).filter(UserGit).all()) 

