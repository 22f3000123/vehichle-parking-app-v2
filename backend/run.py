
from app import create_app
from app.extensions import db
from app.models import User, Role
from flask_security import hash_password

def setup_database(app):
    with app.app_context():
        db.create_all()
        if not Role.query.filter_by(name='admin').first():
            admin_role = Role(name='admin', description='Administrator')
            db.session.add(admin_role)
            db.session.commit()

        if not User.query.filter_by(email='admin@test.com').first():
            admin_user = User(
                first_name='Admin',
                last_name='User',
                email='admin@test.com',
                username='admin',
                password=hash_password('admin'),
                active=True,
                fs_uniquifier='admin',
            )
            admin_role = Role.query.filter_by(name='admin').first()
            admin_user.roles.append(admin_role)
            db.session.add(admin_user)
            db.session.commit()

app = create_app()
setup_database(app)

if __name__ == '__main__':
    app.run(debug=True)
