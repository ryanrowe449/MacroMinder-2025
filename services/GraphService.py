import plotly.graph_objects as go
from services.HabitService import HabitService
from services.CompletionLogService import CompletionLogService
from services.HabitCompletionService import HabitCompletionService

class GraphService:
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
            title='Habit Progress',
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
            title='Habit Progress',
        )
        chart_html = fig.to_html(full_html=False)
        return chart_html

    @staticmethod
    def generate_weight_over_time_graph(user_id):
        dates, weights = CompletionLogService.get_weight_data(user_id)

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=dates, y=weights, mode='lines', name='Weight'))

        fig.update_layout(
            title='Weight Over Time',
            xaxis=dict(title='Date'),
            yaxis=dict(title='Weight (lbs)'),
            height=300,
            width=450,
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
            height=300,
            width=450,
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