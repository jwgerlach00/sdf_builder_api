from . import Data


def add_entry(db:Data, username:str, smiles:str, dataname:str='test') -> None:
    db.session.add(Data(username=username, dataname=dataname, smiles=smiles))
    db.session.commit()
