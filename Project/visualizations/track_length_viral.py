import pandas as pd
import plotly.graph_objects as go
from .utils import df, get_modern_layout

def create_track_length_viral():
    df_copy = df.copy()
    df_copy['duration_min'] = df_copy['duration_ms'] / 60000
    
    df_copy['length_category'] = pd.cut(df_copy['duration_min'], 
                                  bins=[0, 2.5, 3.5, 4.5, 10], 
                                  labels=['Short (0-2.5min)', 'Medium (2.5-3.5min)', 'Long (3.5-4.5min)', 'Very Long (4.5min+)'])
    
    fig = go.Figure()
    
    colors = ['#43E97B', '#1DB954', '#0D7D2C', '#0A5D1F']
    
    for i, category in enumerate(['Short (0-2.5min)', 'Medium (2.5-3.5min)', 'Long (3.5-4.5min)', 'Very Long (4.5min+)']):
        category_data = df_copy[df_copy['length_category'] == category]['popularity']
        
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
        yaxis_title="Viral Score",
        showlegend=False,
        margin=dict(l=60, r=60, t=40, b=60)
    ))
    
    fig.update_layout(**layout_update)
    return fig 