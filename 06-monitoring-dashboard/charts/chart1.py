import plotly.graph_objs as go
import pandas as pd

# Below code assumes that 'df' is a Pandas DataFrame with the results from your Snowflake query.
# The DataFrame should have two columns: 'hour_window' and 'avg_execution_time_ms'.

def getChart(df):
    # Creating the line chart
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df['HOUR_WINDOW'], 
        y=df['AVG_EXECUTION_TIME_MS'],
        mode='lines+markers',  # This will create both lines and markers on each data point
        name='Average Execution Time'
    ))

    # Updating layout of the plot
    fig.update_layout(
        title='Average Query Execution Time in the Last Day',
        xaxis_title='Hour Window (Last 24 Hours)',
        yaxis_title='Average Execution Time (ms)',
        xaxis=dict(showline=True, showgrid=False, linecolor='rgb(204, 204, 204)'),
        yaxis=dict(showline=True, showgrid=False, linecolor='rgb(204, 204, 204)'),
        plot_bgcolor='white'
    )

    # Display the plot
    #fig.show()
    return fig