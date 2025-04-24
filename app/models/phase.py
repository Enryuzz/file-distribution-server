from app import db

class Phase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    is_active = db.Column(db.Boolean, default=False)
    
    @classmethod
    def is_attack_active(cls):
        phase = cls.query.filter_by(name='attack').first()
        return phase.is_active if phase else False
    
    @classmethod
    def is_defense_active(cls):
        phase = cls.query.filter_by(name='defense').first()
        return phase.is_active if phase else False 