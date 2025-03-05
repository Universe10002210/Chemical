
from flask import Flask, request, jsonify
from rdkit import Chem
from rdkit.Chem import AllChem, rdMolDescriptors
import tempfile
import os
import shutil
from models import db, Compound
from flask_cors import CORS

app = Flask(__name__)
# 请根据实际情况修改数据库连接信息
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://your_username:your_password@localhost/chemical_db'
db.init_app(app)
CORS(app)


@app.route('/upload', methods=['POST'])
def upload_compound():
    file = request.files.get('file')
    if not file:
        return jsonify({"error": "No file provided"}), 400

    temp_path = os.path.join(tempfile.gettempdir(), file.filename)
    try:
        file.save(temp_path)
        mol = Chem.MolFromMolFile(temp_path)
        if not mol:
            return jsonify({"error": "Invalid file format"}), 400

        inchi = Chem.MolToInchi(mol)
        smiles = Chem.MolToSmiles(mol)
        fingerprint = AllChem.GetMorganFingerprintAsBitVect(mol, 2, nBits=1024).ToBitString()
        skeleton = Chem.MolToSmiles(rdMolDescriptors.GetMoleculeScaffold(mol))

        new_compound = Compound(
            name=request.form.get('name'),
            inchi=inchi,
            smiles=smiles,
            fingerprint=fingerprint,
            skeleton_smiles=skeleton
        )
        db.session.add(new_compound)
        db.session.commit()
        return jsonify({"status": "success", "inchi": inchi})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        if os.path.exists(temp_path):
            if os.path.isdir(temp_path):
                shutil.rmtree(temp_path)
            else:
                os.remove(temp_path)


@app.route('/search', methods=['POST'])
def search_similar():
    data = request.json
    query_smiles = data.get('smiles')
    if not query_smiles:
        return jsonify({"error": "Missing 'smiles' in request data"}), 400

    threshold = data.get('threshold', 0.8)
    method = data.get('method', 'tanimoto')
    query_mol = Chem.MolFromSmiles(query_smiles)
    if not query_mol:
        return jsonify({"error": "Invalid SMILES string"}), 400

    query_fp = AllChem.GetMorganFingerprintAsBitVect(query_mol, 2, nBits=1024)
    compounds = Compound.query.all()
    results = []
    for compound in compounds:
        db_fp = Chem.DataStructs.CreateFromBitString(compound.fingerprint)
        if method == 'tanimoto':
            similarity = Chem.DataStructs.TanimotoSimilarity(query_fp, db_fp)
        else:
            similarity = 0

        query_skeleton = rdMolDescriptors.GetMoleculeScaffold(query_mol)
        db_skeleton = Chem.MolFromSmiles(compound.skeleton_smiles)
        if query_skeleton and db_skeleton:
            skeleton_fp_query = AllChem.GetMorganFingerprintAsBitVect(query_skeleton, 2, nBits=1024)
            skeleton_fp_db = AllChem.GetMorganFingerprintAsBitVect(db_skeleton, 2, nBits=1024)
            skeleton_similarity = Chem.DataStructs.TanimotoSimilarity(skeleton_fp_query, skeleton_fp_db)
        else:
            skeleton_similarity = 0

        if similarity >= threshold:
            results.append({
                "name": compound.name,
                "smiles": compound.smiles,
                "similarity": round(similarity, 3),
                "skeleton_similarity": round(skeleton_similarity, 3)
            })

    return jsonify({"results": sorted(results, key=lambda x: x['similarity'], reverse=True)})


@app.route('/')
def home():
    return "Flask 后端服务已启动！"


if __name__ == '__main__':
    app.run(debug=True)
