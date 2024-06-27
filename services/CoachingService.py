from models import User, CoachingGroups
from app import db, bcrypt

class CoachingService:
    #Query the database to get the list of users paired with the coach
    @staticmethod
    def get_paired_users(coach_id):
        #join where the user_id in CoachingGroups matches the id in the User table
        paired_users = db.session.query(User).join(CoachingGroups, CoachingGroups.user_id == User.id).filter(CoachingGroups.coach_id == coach_id, CoachingGroups.rel_status == 'friends').all()
        return paired_users
    
    @staticmethod
    def get_requested_users(coach_id):
        #join where the user_id in CoachingGroups matches the id in the User table
        requested_users = db.session.query(User).join(CoachingGroups, CoachingGroups.user_id == User.id).filter(CoachingGroups.coach_id == coach_id, CoachingGroups.rel_status == 'pending').all()
        return requested_users

    @staticmethod
    def get_requested_pair(user_id):
        return CoachingGroups.query.filter_by(user_id=user_id).first()
    
    @staticmethod
    def create_link(user_id, coach_id):
        # Check if the user is already linked to a coach
        existing_link = CoachingGroups.query.filter_by(user_id=user_id, coach_id=coach_id).first()
        #if the link exists, make them friends
        if existing_link:
            existing_link.rel_status = 'friends'
        else:
            # If no link exists, create a new entry in the CoachingGroups table with a 'pending' status
            new_link = CoachingGroups(user_id=user_id, coach_id=coach_id, rel_status='pending')
            db.session.add(new_link)
        db.session.commit()
        return True
    
    @staticmethod
    def delete_link(user_id, coach_id):
        link = CoachingGroups.query.filter_by(user_id=user_id, coach_id=coach_id).first()
        if link:
            db.session.delete(link)
            db.session.commit()
            return True
        else:
            return False