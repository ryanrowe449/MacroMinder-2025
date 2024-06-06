from models import HabitCompletion, User
from app import db

class HabitCompletionService:
    #checks to see if a specific habit was completed on a specific date
    @staticmethod
    def check_for_habit_completion(habit_id, date):
        completion = HabitCompletion.query.filter_by(habit_id=habit_id, date=date)
        return completion
    
    @staticmethod
    def get_completions(user_id, date):
        completions = HabitCompletion.query.filter_by(user_id=user_id, date=date).all()
        return completions