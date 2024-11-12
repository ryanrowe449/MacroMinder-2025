from models import CompletionLog
from models import User
from application import db

class CompletionLogService:
    @staticmethod
    def get_logs(user_id, date=None):
        if date:
            logs = CompletionLog.query.filter_by(user_id=user_id, date=date).all()
        else:
            logs = CompletionLog.query.filter_by(user_id=user_id).all()
        return logs
    
    @staticmethod
    def delete_all_user_completion_logs(user_id):
        logs = CompletionLog.query.filter_by(user_id=user_id).all()
        for log in logs:
            db.session.delete(log)
        db.session.commit()

    # Instead of having an edit button, we 'limit' the user to one log per day by checking against 
    # the date stored in the db, serves as 'edit' functionality as well.
    @staticmethod
    def add_completion_log(user_id, date, protein=0, calories=0, weightlbs=150, carbs=0, fats=0):
        # Check if there is already a log for the given user and date
        existing_log = CompletionLog.query.filter_by(user_id=user_id, date=date).first()

        if existing_log:
            # Update the existing log
            existing_log.protein = protein
            existing_log.calories = calories
            existing_log.carbs = carbs
            existing_log.fats = fats
            existing_log.weightlbs = weightlbs
        else:
            # Create a new log
            new_log = CompletionLog(
                user_id=user_id,
                date=date,
                protein=protein,
                calories=calories,
                weightlbs=weightlbs,
                carbs = carbs,
                fats = fats
            )
            db.session.add(new_log)

        db.session.commit()
        return existing_log.tracking_id if existing_log else new_log.tracking_id

    @staticmethod
    def delete_completion_log(log_id):
        log = CompletionLog.query.get(log_id)
        if log:
            db.session.delete(log)
            db.session.commit()
            return True
        else:
            return False
        
    @staticmethod
    def get_macros_for_current_user(user_id):
        macros = CompletionLog.query.filter_by(user_id=user_id).all()
        return macros
    
    @staticmethod
    def get_weight_data(user_id):
        #Fetch weight and date data from CompletionLog table for the given user_id
        logs = CompletionLog.query.filter_by(user_id=user_id).all()
        data = {}
        #extract dates and weights from the logs, store in data dictionary
        for log in logs:
            data[log.date] = log.weightlbs

        #split data into two lists, one containing dates (sorted), the other weights
        dates = sorted(data.keys())
        weights = [data[date] for date in dates]

        return dates, weights
    
    @staticmethod
    def get_calories_data(user_id):
        logs = CompletionLog.query.filter_by(user_id=user_id).all()
        data = {}
        for log in logs:
            data[log.date] = log.calories
        dates = sorted(data.keys())
        calories = [data[date] for date in dates]
        return dates, calories
    
    @staticmethod
    def get_protein_data(user_id):
        logs = CompletionLog.query.filter_by(user_id=user_id).all()
        data = {}
        for log in logs:
            data[log.date] = log.protein
        dates = sorted(data.keys())
        protein = [data[date] for date in dates]
        return dates, protein
    
    @staticmethod
    def get_carbs_data(user_id):
        logs = CompletionLog.query.filter_by(user_id=user_id).all()
        data = {}
        for log in logs:
            data[log.date] = log.carbs
        dates = sorted(data.keys())
        carbs = [data[date] for date in dates]
        return dates, carbs
    
    @staticmethod
    def get_fats_data(user_id):
        logs = CompletionLog.query.filter_by(user_id=user_id).all()
        data = {}
        for log in logs:
            data[log.date] = log.fats
        dates = sorted(data.keys())
        fats = [data[date] for date in dates]
        return dates, fats