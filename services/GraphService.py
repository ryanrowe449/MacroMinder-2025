import plotly.graph_objects as go
from services.HabitService import HabitService
from services.CompletionLogService import CompletionLogService
from services.HabitCompletionService import HabitCompletionService

class GraphService:
    #------------------charts--------------------
    #bar chart: x-axis = each habit, y-axis = number of completions for that habit
    @staticmethod
    def generate_habit_progress_barchart(user_id):
        #gets a user's completions
        descriptions, count = HabitCompletionService.get_completion_data(user_id)
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=descriptions,
            y=count,
            name='Habit Progress',
            marker_color='blue'
        ))

        fig.update_layout(
            title='Habit Completions Breakdown',
            xaxis=dict(title='Habits'),
            yaxis=dict(title='Total Completions'),
        )

        chart_html = fig.to_html(full_html=False)
        return chart_html
    #same data as bar chart, but a pie chart
    @staticmethod
    def generate_habit_progress_piechart(user_id):
        descriptions, count = HabitCompletionService.get_completion_data(user_id)
        fig = go.Figure()
        fig.add_trace(go.Pie(
            labels=descriptions,
            values=count,
            name='Habit Progress',
        ))
        fig.update_layout(
            title='Habit Completions Breakdown',
        )
        chart_html = fig.to_html(full_html=False)
        return chart_html

    def generate_weekly_completion_summary_bar(user_id):
        logs = HabitCompletionService.get_completions(user_id)

        #keep track of habits completed per day
        completion_data = {'Sunday': 0, 'Monday': 0, 'Tuesday': 0, 'Wednesday': 0, 'Thursday': 0, 'Friday': 0, 'Saturday': 0}
        for log in logs:
            day_of_week = log.date.strftime('%A')
            completion_data[day_of_week] += 1

        # Create the figure
        fig = go.Figure()
        fig.add_trace(go.Bar(x=list(completion_data.keys()), y=list(completion_data.values()), name='Completions'))

        fig.update_layout(
            title='Weekly Habit Completion Summary',
            xaxis=dict(title='Day of the Week'),
            yaxis=dict(title='Total Completions'),
        )

        graph_html = fig.to_html(full_html=False)
        return graph_html
    
    def generate_weekly_completion_summary_pie(user_id):
        logs = HabitCompletionService.get_completions(user_id)

        #keep track of habits completed per day
        completion_data = {'Sunday': 0, 'Monday': 0, 'Tuesday': 0, 'Wednesday': 0, 'Thursday': 0, 'Friday': 0, 'Saturday': 0}
        for log in logs:
            day_of_week = log.date.strftime('%A')
            completion_data[day_of_week] += 1

        # Create the figure
        fig = go.Figure()
        fig.add_trace(go.Pie(
            labels=list(completion_data.keys()),
            values=list(completion_data.values()),
            name='Completions')
        )

        fig.update_layout(
            title='Weekly Habit Completion Summary'
        )

        graph_html = fig.to_html(full_html=False)
        return graph_html

    #------------------graphs--------------------
    @staticmethod
    def generate_weight_over_time_graph(user_id):
        dates, weights = CompletionLogService.get_weight_data(user_id)

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=dates, y=weights, mode='lines', name='Weight'))

        fig.update_layout(
            title='Weight Over Time',
            xaxis=dict(title='Date'),
            yaxis=dict(title='Weight (lbs)'),
            height=500,
            width=1060,
        )

        graph_html = fig.to_html(full_html=False)
        return graph_html
    
    @staticmethod
    def generate_completions_over_time_graph(user_id):
        dates, count = HabitCompletionService.get_completion_date_data(user_id)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=dates, y=count, mode='lines', name='Habit Completion Count'))

        fig.update_layout(
            title='Habit Completions Over Time',
            xaxis=dict(title='Date'),
            yaxis=dict(title='Habit Completions'),
            height=500,
            width=1060,
        )

        graph_html = fig.to_html(full_html=False)
        return graph_html
    
    #get a graph of the macros (protein, carbs, fats)
    @staticmethod
    def generate_macros_over_time_graph(user_id):
        #dates doesn't really matter since they are all the same
        dates, protein = CompletionLogService.get_protein_data(user_id)
        dates, carbs = CompletionLogService.get_carbs_data(user_id)
        dates, fats = CompletionLogService.get_fats_data(user_id)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=dates, y=protein, mode='lines', name='Protein (g)'))
        fig.add_trace(go.Scatter(x=dates, y=carbs, mode='lines', name='Carbs (g)'))
        fig.add_trace(go.Scatter(x=dates, y=fats, mode='lines', name='Fats (g)'))

        fig.update_layout(
            title='Macros Consumed Over Time',
            xaxis=dict(title='Date'),
            yaxis=dict(title='Macros'),
            height=500,
            width=1060,
        )

        graph_html = fig.to_html(full_html=False)
        return graph_html

    @staticmethod
    def generate_calories_over_time_graph(user_id):
        dates, cals = CompletionLogService.get_calories_data(user_id)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=dates, y=cals, mode='lines', name='Calories'))

        fig.update_layout(
            title='Calories Consumed Over Time',
            xaxis=dict(title='Date'),
            yaxis=dict(title='Calories'),
            height=300,
            width=450,
        )

        graph_html = fig.to_html(full_html=False)
        return graph_html
    
    @staticmethod
    def generate_protein_over_time_graph(user_id):
        dates, protein = CompletionLogService.get_protein_data(user_id)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=dates, y=protein, mode='lines', name='Protein'))

        fig.update_layout(
            title='Protein Consumed Over Time',
            xaxis=dict(title='Date'),
            yaxis=dict(title='Protein (g)'),
            height=300,
            width=450,
        )

        graph_html = fig.to_html(full_html=False)
        return graph_html
    
    @staticmethod
    def generate_carbs_over_time_graph(user_id):
        dates, carbs = CompletionLogService.get_carbs_data(user_id)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=dates, y=carbs, mode='lines', name='Protein'))

        fig.update_layout(
            title='Carbs Consumed Over Time',
            xaxis=dict(title='Date'),
            yaxis=dict(title='Carbs (g)'),
            height=300,
            width=450,
        )

        graph_html = fig.to_html(full_html=False)
        return graph_html
    
    @staticmethod
    def generate_fats_over_time_graph(user_id):
        dates, fats = CompletionLogService.get_fats_data(user_id)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=dates, y=fats, mode='lines', name='Protein'))

        fig.update_layout(
            title='Fats Consumed Over Time',
            xaxis=dict(title='Date'),
            yaxis=dict(title='Fats (g)'),
            height=300,
            width=450,
        )

        graph_html = fig.to_html(full_html=False)
        return graph_html