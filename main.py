from flask import Blueprint, request, Response, send_file
from flask_login import login_required, current_user
import pandas as pd
import base64
from rdkit.Chem import Draw
from io import BytesIO
import naclo

from db import db


main = Blueprint('main', __name__)

def package_mol(smiles:str) -> str:
    '''Packages a smiles string to html data for Mol drawing'''
    
    # mol = naclo.smiles_2_mols([smiles])[0]
    from rdkit import Chem
    mol = Chem.MolFromSmiles(smiles)
    print(smiles)
    print(mol)
    pil_img = Draw.MolToImage(mol, size=(300, 100))
    
    output = BytesIO()
    pil_img.save(output, format='PNG')
    output.seek(0)
    output_s = output.read()
    b64 = base64.b64encode(output_s)
    
    return '<img src="data:image/png;base64,{0}"/>'.format(b64.decode('utf-8'))

@main.route('/get_table', methods=['POST'])
@login_required
def get_table() -> Response:
    data = pd.read_sql_query(f'select * from data where username = \'{current_user.username}\'', db.engine)
    return '', 204

@main.route('/get_saved_tables', methods=['GET'])
@login_required
def get_saved_tables() -> Response:
    df = pd.read_sql_query(f'select * from data where username = \'{current_user.username}\'', db.engine)
    return df['dataname'].unique().tolist()

@main.route('/table_by_name', methods=['POST'])
@login_required
def table_by_name() -> list:
    data = request.get_json()
    dataname = data['table_name']
    print(current_user.username)
    df = pd.read_sql_query(f'select * from data where username = \'{current_user.username}\' \
        and dataname = \'{dataname}\'', db.engine)
    return [package_mol(x) for x in df['smiles'].to_list()]

# @main.route('/new_table', methods=['POST'])
# @login_required
# def new_table():
#     data = request.get_json()
#     table_name = data['table_name']

def is_smiles_in_table(table_name:str, smiles:str):
    data = pd.read_sql_query(f'select * from data where username = \'{current_user.username}\' \
        and dataname = \'{table_name}\'', db.engine)
    return smiles in data['smiles'].to_list()
    

@main.route('/add_mol_to_table', methods=['POST'])
@login_required
def add_mol_to_table() -> list:
    data = request.get_json()
    smi = data['smi']
    table_name = data['table_name']
    
    if is_smiles_in_table(table_name, smi):
        return 'Molecule already in table', 400
    else:
        db.add_data(current_user.username, smi, table_name)
        data = pd.read_sql_query(f'select * from data where username = \'{current_user.username}\' \
            and dataname = \'{table_name}\'', db.engine)
        print(data)
        
    return [package_mol(x) for x in data['smiles'].to_list()]

@main.route('/download_sdf', methods=['POST'])
@login_required
def download_sdf() -> Response:
    data = request.get_json()
    table_name = data['table_name']
    df = pd.read_sql_query(f'select * from data where username = \'{current_user.username}\' \
        and dataname = \'{table_name}\'', db.engine)
    
    mols = naclo.smiles_2_mols(df['smiles'])
    df = pd.DataFrame(mols, columns=['ROMol'])
    
    buf = BytesIO()
    writer = naclo.dataframes.Writer(df)
    buf = writer.write(out=buf, ext='sdf')
    return send_file(buf, as_attachment=True, download_name=f'{table_name}.sdf')
    


    
# @login_manager.request_loader
# def load_user_from_request(request):

#     # first, try to login using the api_key url arg
#     api_key = request.args.get('api_key')
#     if api_key:
#         user = User.query.filter_by(username=api_key).first()
#         if user:
#             return user

#     # next, try to login using Basic Auth
#     api_key = request.headers.get('Authorization')
#     if api_key:
#         api_key = api_key.replace('Basic ', '', 1)
#         try:
#             api_key = base64.b64decode(api_key)
#         except TypeError:
#             pass
#         user = User.query.filter_by(username=api_key).first()
#         if user:
#             return user

#     # finally, return None if both methods did not login the user
#     return None

# blueprint for auth routes in our app
# from .auth import auth as auth_blueprint

# blueprint for non-auth parts of app
# from .main import main as main_blueprint
# app.register_blueprint(main_blueprint)

# return app
