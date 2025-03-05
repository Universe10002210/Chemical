
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Compound(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    inchi = db.Column(db.String(500), unique=True)
    smiles = db.Column(db.String(500))
    molecular_weight = db.Column(db.Float)
    fingerprint = db.Column(db.String(1024))  # 存储分子指纹（如 Morgan 指纹的二进制编码）
    skeleton_smiles = db.Column(db.String(500))  # 分子骨架的 SMILES
