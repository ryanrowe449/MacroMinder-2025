from models import HabitCompletion, User, Habits
from app import db

class HabitCompletionService:
    #checks to see if a specific habit was completed on a specific date
    @staticmethod
    def check_for_habit_completion(habit_id, date):
        completion = HabitCompletion.query.filter_by(habit_id=habit_id, date=date)
        return completion
    
    #gets a user's completions for the day
    @staticmethod
    def get_completions(user_id, date):
        completions = HabitCompletion.query.filter_by(user_id=user_id, date=date).all()
        return completions
    
    @staticmethod
    def add_completion(habit_id, user_id, date):
        habit_completion = HabitCompletion(habit_id=habit_id, user_id=user_id, date=date)
        db.session.add(habit_completion)
        db.session.commit()

    #delete all completions associated with a specific habit
    @staticmethod
    def delete_habit_completions(habit_id):
        habit = Habits.query.get(habit_id)
        if habit:
            completions = habit.completions #this is possible because of the relationship defined in models.py
            #one by one, delete the completions
            for completion in completions:
                db.session.delete(completion)
            db.session.commit()

    #fetch the number of habits completed for each day and the dates associated
    @staticmethod
    def get_completion_data(user_id):
        user = User.query.get(user_id)
        data = {} #data is a dictionary that will have key-value pairs of date:habits completed on that date
        if user:
            completions = user.habit_completions
            #loop through completions; if a completion is stored, increase the count; if not, create a new entry
            for completion in completions:
                date = completion.date
                if date in data:
                    data[date] += 1
                else:
                    data[date] = 1
            #split data into two lists, one containing dates (sorted), the other num of completions
            dates = sorted(data.keys())
            count = [data[date] for date in dates]
            return dates, count
        return [], [] #return nothing if the user doesn't exist