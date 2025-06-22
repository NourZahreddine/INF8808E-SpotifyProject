import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from .utils import get_modern_layout

def create_track_length_viral(data=None):
    if data is None:
        data = pd.read_csv('data/dataset.csv')
    

    if data.empty:
        fig = go.Figure()
        fig.add_annotation(
            text="No data available for the selected filters",
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            showarrow=False,
            font=dict(size=16, color='#B8B8B8')
        )
        layout_update = get_modern_layout()
        fig.update_layout(**layout_update)
        return fig

    df_copy = data.copy()
    df_copy['duration_min'] = df_copy['duration_ms'] / 60000
    

    try:
        df_copy['length_category'] = pd.cut(df_copy['duration_min'], 
                                      bins=[0, 2.5, 3.5, 4.5, 10], 
                                      labels=['Short (0-2.5min)', 'Medium (2.5-3.5min)', 'Long (3.5-4.5min)', 'Very Long (4.5min+)'])
    except Exception as e:
        fig = go.Figure()
        fig.add_annotation(
            text=f"Error processing track length data: {str(e)}",
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            showarrow=False,
            font=dict(size=16, color='#B8B8B8')
        )
        layout_update = get_modern_layout()
        fig.update_layout(**layout_update)
        return fig
    
    fig = go.Figure()
    
    colors = ['#43E97B', '#1DB954', '#0D7D2C', '#0A5D1F']
    
    for i, category in enumerate(['Short (0-2.5min)', 'Medium (2.5-3.5min)', 'Long (3.5-4.5min)', 'Very Long (4.5min+)']):
        category_data = df_copy[df_copy['length_category'] == category]['popularity']
        

        if not category_data.empty:
            fig.add_trace(go.Box(
                y=category_data,
                name=category,
                marker_color=colors[i],
                line=dict(color='#FFFFFF', width=2),
                fillcolor=colors[i],
                opacity=0.7,
                boxpoints='outliers',  
                hoverinfo='y',  
                hovertemplate=None  
            ))
    
    layout_update = get_modern_layout()
    layout_update.update(dict(
        height=450,
        title_text="",
        xaxis_title="Track Length Category",
        yaxis_title="Popularity Score", 
        showlegend=False,
        margin=dict(l=60, r=60, t=40, b=80) 
    ))
    
    fig.update_layout(**layout_update)
    return fig 