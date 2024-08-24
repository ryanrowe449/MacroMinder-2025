from models import User, CoachingGroups
from application import db, bcrypt
from services.HabitService import HabitService
from services.CompletionLogService import CompletionLogService

class UserService:
    @staticmethod
    def create_user(username, password, role):
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(username=username, password=hashed_password, role=role)
        db.session.add(new_user)
        db.session.commit()
    
    def get_user(user_id=None, username=None, role=None):
        if role:
            if username:
                return User.query.filter_by(username=username, role=role).first()
            else:
                return User.query.filter_by(id=user_id, role=role).first()
        else:
            if username:
                return User.query.filter_by(username=username).first()
            else:
                return User.query.filter_by(id=user_id).first()
    
    @staticmethod
    def update_user(user_id, username=None, password=None, role=None):
        user = User.query.get(user_id)
        if not user:
            return None
        
        if username:
            user.username = username
        if password:
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            user.password = hashed_password
        if role:
            user.role = role
        
        db.session.commit()
        return user
    
    @staticmethod
    def delete_user(user_id):
        user = User.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return True
        else:
            return False
    
    @staticmethod
    def list_users():
        users = User.query.all()
        return users
    
    @staticmethod
    def get_life_coaches():
        return User.query.filter_by(role='LifeCoach').all()
    
    @staticmethod
    def get_connected_coach(user_id):
        group = CoachingGroups.query.filter_by(user_id=user_id).first()
        coach = None
        if group:
            if group.rel_status == 'friends':
                coach_id = group.coach_id
                coach = UserService.get_user(user_id=coach_id, role='LifeCoach')
        return coach