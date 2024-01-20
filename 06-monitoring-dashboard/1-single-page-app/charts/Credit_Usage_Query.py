import plotly.express as px

def getChart(df):
    # Ensure the dataframe is sorted by START_TIME before plotting
    df = df.sort_values(by='START_TIME')
    
    # Create a line chart with Plotly Express
    fig = px.line(
        df,
        x='START_TIME',
        y='CREDITS_USED',
        color='WAREHOUSE_NAME',
        labels={'START_TIME': 'Start Time', 'CREDITS_USED': 'Credits Used', 'WAREHOUSE_NAME': 'Warehouse'},
        title='Credit Usage by Virtual Warehouses Over Time'
    )
    
    # Customize the layout
    fig.update_layout(
        xaxis_title='Time',
        yaxis_title='Credits Consumed',
        legend_title='Virtual Warehouse'
    )
    
    # Show the figure
    #fig.show()

    # Return the figure object in case further manipulation is required
    return fig