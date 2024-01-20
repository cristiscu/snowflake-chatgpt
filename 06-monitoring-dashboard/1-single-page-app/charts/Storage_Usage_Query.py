import plotly.express as px

def getChart(df):
    # Aggregate the storage usage by database, schema (optional)
    df_aggregated = df.groupby(['USAGE_DATE']).agg({'STORAGE_BYTES': 'sum'}).reset_index()
    
    # Convert bytes to gigabytes for better readability
    df_aggregated['GB_USED'] = df_aggregated['STORAGE_BYTES'] / (1024 ** 3)

    # Create a bar chart with Plotly Express
    fig = px.bar(
        df_aggregated,
        x='USAGE_DATE',
        y='GB_USED',
        barmode='group',
        labels={'USAGE_DATE': 'Usage Date', 'GB_USED': 'Gigabytes Used'},
        title='Storage Usage (Past 30 Days)'
    )

    # Customize the layout
    fig.update_layout(
        xaxis_title='Time',
        yaxis_title='Storage Used (GB)'
        #legend_title='Database'
    )
    
    # Show the figure
    #fig.show()

    # Return the figure object in case further manipulation is required
    return fig