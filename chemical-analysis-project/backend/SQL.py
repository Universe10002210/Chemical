from app import app, db
from models import Compound

# 推送应用上下文
with app.app_context():
    # 创建所有表
    db.create_all()