from app import db


class Assessment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    module_code = db.Column(db.String(10), nullable=False)
    deadline = db.Column(db.Date, nullable=False)
    description = db.Column(db.Text, nullable=True)
    is_completed = db.Column(db.Boolean, default=False)
    is_deleted = db.Column(db.Boolean, default=False)

    # Unique constraint for title and module_code combination
    __table_args__ = (
        db.UniqueConstraint(
            'title', 'module_code', name='title_module_uc'
        ),
    )

    def __repr__(self):
        return f'<Assessment {self.title}>'
