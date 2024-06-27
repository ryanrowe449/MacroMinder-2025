from app import db
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy import ForeignKey, Column, Integer, String, Boolean, Date
#from sqlalchemy.ext.declarative import declarative_base
#from sqlalchemy.schema import PrimaryKeyConstraint
from sqlalchemy.orm import relationship

#Base = declarative_base

class User(db.Model):
    # Replace 'User' with the name of your database table containing these exact things - Ori
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    role = db.Column(db.String(80), nullable=False)

#table linked to user to define their habits
class Habits(db.Model):
    __tablename__ = 'Habits'
    habit_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
    habit_description = db.Column(db.String(255), nullable=False)
    date = db.Column(db.Date, nullable = False)
    sun = db.Column(db.Boolean, default=True, nullable=False)
    mon = db.Column(db.Boolean, default=True, nullable=False)
    tues = db.Column(db.Boolean, default=True, nullable=False)
    wed = db.Column(db.Boolean, default=True, nullable=False)
    thurs = db.Column(db.Boolean, default=True, nullable=False)
    fri = db.Column(db.Boolean, default=True, nullable=False)
    sat = db.Column(db.Boolean, default=True, nullable=False)
    user = relationship("User", backref="habits") #gets all the habits linked to a user


# Db table for tracking the macro for the day, tasks_completed is for habits
class CompletionLog(db.Model):
    __tablename__ = 'CompletionLog'
    tracking_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    protein = db.Column(db.Integer, default=0)
    carbs = db.Column(db.Integer, default=0)
    fats = db.Column(db.Integer, default=0)
    calories = db.Column(db.Integer, default=0)
    weightlbs = db.Column(db.DECIMAL(4, 2), default=150)
    user = relationship("User", backref="completionlogs") #gets all the logs linked to a user

class HabitCompletion(db.Model):
    __tablename__ = 'HabitCompletion'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    habit_id = db.Column(db.Integer, db.ForeignKey('Habits.habit_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    habit = relationship("Habits", backref="completions") #gets all completions linked to a habit
    user = relationship("User", backref="habit_completions") #gets all completions linked to a user

# Db table for keeping life coaches linked with their standard users
class CoachingGroups(db.Model):
    __tablename__ = 'CoachingGroups'
    coach_id = db.Column(db.Integer, db.ForeignKey('User.id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), primary_key=True)
    rel_status = db.Column(db.String(80), nullable=False)
    life_coach = relationship("User", foreign_keys=[coach_id])
    user = relationship("User", foreign_keys=[user_id])
