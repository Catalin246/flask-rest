from .. import db
from datetime import datetime

class Todo(db.Model):
    """ Todo Model for storing todo related details """
    __tablename__ = "todo"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    user = db.relationship('User', backref=db.backref('todo', lazy=True))

    def __repr__(self):
        return "<Todo '{}'>".format(self.description)
