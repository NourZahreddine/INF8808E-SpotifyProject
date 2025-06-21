import plotly.graph_objects as go
import plotly.express as px
from .utils import get_modern_layout

def create_tempo_loudness_analysis(data=None):
    if data is None:
        import pandas as pd
        data = pd.read_csv('data/dataset.csv')

    sample_df = data.sample(n=min(8000, len(data)), random_state=42)
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=sample_df['tempo'],
        y=sample_df['popularity'],
        mode='markers',
        marker=dict(
            color=sample_df['loudness'],
            colorscale=[
                [0, '#0066CC'],      
                [0.25, '#4A90E2'],  
                [0.5, '#FFA500'],   
                [1, '#FF0000']    
            ],
            size=5,
            opacity=0.7,
            colorbar=dict(
                title="Loudness (dB)",
                titlefont=dict(color='#FFFFFF', size=11),
                tickfont=dict(color='#FFFFFF', size=9)
            ),
            line=dict(width=0.3, color='#FFFFFF'),
            cmin=sample_df['loudness'].quantile(0.05), 
            cmax=sample_df['loudness'].quantile(0.95) 
        ),
        hovertemplate=
        "<b>%{customdata[0]}</b><br>" +
        "Tempo: <b>%{x:.0f} BPM</b><br>" +
        "Popularity: <b>%{y}</b><br>" +
        "Loudness: <b>%{marker.color:.1f} dB</b>" +
        "<extra></extra>",
        customdata=sample_df[['track_name']].values
    ))
    
    layout_update = get_modern_layout()
    layout_update.update(dict(
        height=450,
        title_text="",
        xaxis_title="Tempo (BPM)",
        yaxis_title="Popularity Score",
        showlegend=False,
        margin=dict(l=60, r=120, t=40, b=60)
    ))
    
    fig.update_layout(**layout_update)
    return fig 