from flask import render_template, request, session, redirect, url_for, jsonify
from application import application, db, bcrypt
from models import User, Habits, CompletionLog, CoachingGroups, HabitCompletion
from services.UserService import UserService
from services.HabitService import HabitService
from services.CompletionLogService import CompletionLogService
from services.HabitCompletionService import HabitCompletionService
from services.TimeService import TimeService
from services.CoachingService import CoachingService
from services.GraphService import GraphService
from datetime import date, datetime
import pandas as pd
import plotly.graph_objects as go

#route for login, it gets the username and password to verify the user
#sets up all session id's and directs the user to the correct dashboard
@application.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        existingUser = User.query.filter_by(username=username).first()
        #if the username and password match up, load the user's dashboard for the current date
        if existingUser and bcrypt.check_password_hash(existingUser.password, password):
            session['username'] = existingUser.username
            session['userid'] = existingUser.id 
            session['role'] = existingUser.role
            session['current_date'] = date.today()
 
            if existingUser.role == 'LifeCoach':
                #return redirect(url_for('lifecoach_dashboard'))  
                return jsonify({'user': False})
            else:
                #return redirect(url_for('user_dashboard'))
                return jsonify({'user': True})
        #if the username and password do not match up
        else:
            return jsonify({'failure': True})

    return render_template('LoginPage.html')

#when clicking the back button in ManageHabits.html, loads the user/lifecoach dashboard
@application.route('/go_home', methods=['GET', 'POST'])
def go_home():
    role = session.get('role')
    #if the logged-in user is a life coach, go back to the page of their client. If not, load the User's page
    if role == 'LifeCoach':
        user_id = request.args.get('user_id')
        return redirect(url_for('view_user', user_id=user_id))
    elif role == 'User':
        return redirect(url_for('user_dashboard'))
    
@application.route('/load_graphs_page')
def load_graphs_page():
    user_id = request.args.get('user_id')
    weight_graph = GraphService.generate_weight_over_time_graph(user_id)
    completions_graph = GraphService.generate_completions_over_time_graph(user_id)
    calories_graph = GraphService.generate_calories_over_time_graph(user_id)
    protein_graph = GraphService.generate_protein_over_time_graph(user_id)
    carbs_graph = GraphService.generate_carbs_over_time_graph(user_id)
    fats_graph = GraphService.generate_fats_over_time_graph(user_id)
    macros_graph = GraphService.generate_macros_over_time_graph(user_id)
    role = session.get('role')
    return render_template('Graphs.html', userid=user_id, weight_graph=weight_graph, completions_graph=completions_graph, 
                           macros_graph=macros_graph, calories_graph=calories_graph, protein_graph=protein_graph,
                           carbs_graph=carbs_graph, fats_graph=fats_graph, role=role)

@application.route('/load_charts_page')
def load_charts_page():
    user_id = request.args.get('user_id')
    habits_barchart = GraphService.generate_habit_progress_barchart(user_id)
    habits_piechart = GraphService.generate_habit_progress_piechart(user_id)
    weekly_completions_bar = GraphService.generate_weekly_completion_summary_bar(user_id)
    weekly_completions_pie = GraphService.generate_weekly_completion_summary_pie(user_id)
    role = session.get('role')
    return render_template('Charts.html', userid=user_id, habits_barchart=habits_barchart, habits_piechart=habits_piechart, 
                           weekly_completions_bar=weekly_completions_bar, weekly_completions_pie=weekly_completions_pie, role=role)

#route to log out of current account
@application.route('/signout', methods=['POST','GET'])
def logout():
    session.clear()  #remove all items from a session
    return redirect(url_for('login'))  #redirect to home page

#Route to render registration page
@application.route('/gotoregister', methods=['POST','GET'])
def goToRegister():
    return render_template('RegisterPage.html')

#this route obtains the information to build a user, calls UserService to create a user
@application.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')
    role = request.form.get('role')

    #if the user with the entered username exists, do not add to datbase
    existingUser = UserService.get_user(username=username)
    if existingUser:
        return jsonify({'success': False})
    else:
    #else, create the user and add to db
        UserService.create_user(username, password, role)
        return jsonify({'success': True})

# ---------------------------- USER ROUTES ----------------------------------------------

#the main user dashboard, calls various service layer functions to obtain all required information
#HabitService prints the habits for the session date, GraphService prints the graph corresponding
#UserService prints the lifecoach and Coaching groups checks for any paired groups.
@application.route('/user/dashboard')
def user_dashboard():
    userid = session.get('userid')
    username = session.get('username')
    session_date = session.get('current_date')
    #we have to use this to get the session date in a format the db can read
    current_date = TimeService.parse_session_date(session_date)
    connected_coach = UserService.get_connected_coach(userid)
    request = CoachingService.get_requested_pair(userid)
    requested_coach = None
    if request:
        requested_coach = UserService.get_user(request.coach_id)
    habits = HabitService.list_habits(userid, current_date) #add date parameter
    completions = HabitCompletionService.get_completions(userid, current_date)
    completions_dict = {completion.habit_id: True for completion in completions}
    
    return render_template('UserDashboard.html', userid=userid, habits=habits, current_date=current_date,
                           username=username, connected_coach=connected_coach, request=request,
                           requested_coach=requested_coach, completions=completions_dict)


@application.route('/managehabits', methods=['POST'])
def manage_habits():
    #send the user's habits to managehabits.html
    userid = request.form.get('user_id')
    habits = HabitService.list_habits(userid)
    return render_template('ManageHabits.html', userid=userid, habits=habits, getattr=getattr) #have to add getattr=getattr to the template context so it can be used

#just used for the managehabits page; this handles the event of a user changing the description/days of a habit
@application.route('/updatehabits', methods=['POST'])
def update_habits():
    if request.method == 'POST':
        data = request.json
        habits = data.get('habits', []) #put the data into a list
        user_id = data.get('user_id')

        if user_id:
            for habit_data in habits:
                habit_id = habit_data['habit_id'] #habit_id is the key
                habit_description = habit_data.get('habit_description')
                habit = Habits.query.filter_by(habit_id=habit_id, user_id=user_id).first()
                
                if habit:
                    habit.habit_description = habit_description
                    habit.sun = habit_data.get('sun', False) #defaults to False if a key is missing
                    habit.mon = habit_data.get('mon', False)
                    habit.tues = habit_data.get('tues', False)
                    habit.wed = habit_data.get('wed', False)
                    habit.thurs = habit_data.get('thurs', False)
                    habit.fri = habit_data.get('fri', False)
                    habit.sat = habit_data.get('sat', False)

                    db.session.commit()

            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'message': 'You must be logged in to update habits.'})

    return jsonify({'success': False, 'message': 'Invalid request method.'})

#route to render the addhabit page or add a habit
#called when a user clicks 'add' for a habit, takes the habit description and uses it to create a new habit for that date
@application.route('/addhabit', methods=['POST','GET'])
def addHabit():
    if request.method == 'POST':
        description = request.form.get('habitdesc')
        userid = request.form.get('user_id') 
        current_date = session.get('current_date')
        current_date = TimeService.parse_session_date(current_date)

        if userid:
            success, response = HabitService.add_habit(userid, description, current_date) #response is the habit id
            if success:
                return jsonify({'success': True, 'habit_id': response, 'desc': description})
            else:
                return jsonify({'success': False, 'message': response})
        else:
            return jsonify({'success': False, 'message': 'You must be logged in to add a habit.'})

#called when a checkbox is clicked, stores/deletes a completion in habitcompletion
@application.route('/checkbox', methods=['POST'])
def checkBox():
    user_id = request.form.get('user_id')
    habit_id = request.form.get('habit_id')
    current_date = session.get('current_date')
    current_date = TimeService.parse_session_date(current_date)
    completed = request.form.get('completed')=='True'
    habit = HabitService.get_habit(habit_id)
    if habit:
        habit_completion = HabitCompletion.query.filter_by(habit_id=habit_id, user_id=user_id, date=current_date).first()

        if completed:
            if not habit_completion:
                HabitCompletionService.add_completion(habit_id, user_id, current_date)
        else:
            if habit_completion:
                db.session.delete(habit_completion)

        db.session.commit()
        return jsonify({'success': True})
    else:
        return jsonify({'success': False})

#called when a user clicks edit habit, queries for the new description and edits the desired habit with HabitService
@application.route('/edithabit', methods=['POST'])
def editHabit():
    habit_id = request.form.get('habit_id')
    new_description = request.form.get('new_description')

    success = HabitService.edit_habit(habit_id, new_description)
    
    if success:
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'message': 'Habit not found'})

#called when a user clicks delete habit, passes info to HabitService
@application.route('/deletehabit', methods=['POST'])
def deleteHabit():
    #before deleting the habit, delete the completions related to the habit
    #have to delete completions before deleting habit, as delete_habit_completions requires that the habit exists
    habit_id = request.form.get('habit_id')
    HabitCompletionService.delete_habit_completions(habit_id)
    success = HabitService.delete_habit(habit_id)
    if success:
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'message': 'Habit not found'})
    
@application.route('/deletecoachinggroup', methods=['POST'])
def delete_coaching_group():
    user_id = request.form.get('user_id')
    #user_id = session.get('userid')
    success = CoachingService.delete_link(user_id)
    if success:
        return jsonify({'success': True})
    else:
        return jsonify({'success': False})
    
@application.route('/searchcoach', methods=['POST'])
def search_coach():
    username = request.form.get('coach_name')
    coach = UserService.get_user(username=username, role='LifeCoach')
    if coach:
        coach_data = {
            'id': coach.id,
            'username': coach.username
        }
        return jsonify({'success': True, 'coach_data': coach_data})
    else:
        return jsonify({'success': False, 'message': 'Coach not found'})
    
@application.route('/sendrequest', methods=['POST'])
def send_request():
    user_id = session.get('userid')
    coach_id = request.form.get('coach_id')
    coach = UserService.get_user(coach_id)
    if user_id and coach_id and coach:
        CoachingService.create_link(user_id, coach_id)
        coach_data = {
            'id': coach.id,
            'username': coach.username
        }
        return jsonify({'success': True, 'coach_data': coach_data, 'user_id': user_id})
    else:
        return jsonify({'success': False})
    
#called when a user submits macro information, passes information to CompletionLogService
@application.route('/addmacros', methods=['POST'])
def add_macros():
    # Add macro to the database
    #user_id = session.get('userid')
    data = request.get_json()
    user_id = data['user_id']
    protein = data['protein']
    carbs = data['carbs']
    fats = data['fats']
    calories = data['calories']
    weightlbs = data['weightlbs']
    current_date = session.get('current_date')
    current_date = TimeService.parse_session_date(current_date)

    CompletionLogService.add_completion_log(user_id, current_date, protein, calories, weightlbs, carbs, fats)
  
    return jsonify({"success": True})
# ----------------------- LIFECOACH ROUTES ---------------------------------------

#the main lifecoach dashbaors, uses Coachingservice to print out all paired users
@application.route('/lifecoach/dashboard')
def lifecoach_dashboard():
    username = session.get('username')
    # Check lifecoach role
    if session.get('role') != 'LifeCoach':
        return redirect(url_for('login'))

    # Get the lifecoach's ID from the session
    lifecoach_id = session.get('userid')

    # Fetch paired/requested users for the lifecoach
    paired_users = CoachingService.get_paired_users(lifecoach_id)
    requested_users = CoachingService.get_requested_users(lifecoach_id)

    # Render the lifecoach dashboard template with paired users
    return render_template('LifecoachDashboard.html', paired_users=paired_users, requested_users=requested_users, username=username)

#the view of the users dashboard from a lifecoach view, prints everything a user might see from userdashboard
#everything there applies here.
@application.route('/viewuser/<int:user_id>', methods=['GET'])
def view_user(user_id):
    user = User.query.get(user_id)
    user_username = user.username
    session_date = session.get('current_date')
    current_date = TimeService.parse_session_date(session_date)
    
    if not user:
        return redirect(url_for('lifecoach_dashboard'))
    
    habits = HabitService.list_habits(user_id, current_date)
    completions = HabitCompletionService.get_completions(user_id, current_date)
    completions_dict = {completion.habit_id: True for completion in completions}

    # Render the UserView.html template with the user's information
    return render_template('UserView.html', user_id=user_id, habits=habits, current_date=current_date, user_username=user_username, completions=completions_dict)

@application.route('/setcoachinggroup', methods=['POST'])
def set_coach():
    coach_id = session.get('userid')
    user_id = request.form.get('user_id')
    success = CoachingService.create_link(user_id, coach_id)
    if success:
        user = UserService.get_user(user_id=user_id)
        return jsonify({'success': True, 'username': user.username})
    else:
        return jsonify({'success': False})
        
#sets the session id to the next date, using TimeService
@application.route('/nextday', methods=['POST'])
def next_day():
    TimeService.set_next_date()
    return jsonify({'success': True})

#sets the session ID to the previous date, using TimeService
@application.route('/prevday', methods=['POST'])
def prev_day():
    TimeService.set_previous_date()
    return jsonify({'success': True})