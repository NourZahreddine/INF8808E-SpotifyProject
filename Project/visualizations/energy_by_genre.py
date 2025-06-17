import plotly.graph_objects as go
from .utils import df, get_modern_layout

def create_energy_by_genre():
    top_genres = df['track_genre'].value_counts().head(10).index
    filtered_df = df[df['track_genre'].isin(top_genres)]
    
    fig = go.Figure()
    
    colors = ['#43E97B', '#3AE571', '#32E168', '#29DD5E', '#20D955', '#18D54B', '#0FD142', '#1DB954', '#15B54A', '#0CB240']
    
    for i, genre in enumerate(top_genres):
        genre_data = filtered_df[filtered_df['track_genre'] == genre]['energy']
        
        fig.add_trace(go.Box(
            y=genre_data,
            name=genre,
            marker_color=colors[i],
            line=dict(color='#FFFFFF', width=1),
            opacity=0.7,
            hoverinfo='y'
        ))
    
    layout_update = get_modern_layout()
    layout_update.update(dict(
        height=450,
        title_text="",
        xaxis_title="Genre",
        yaxis_title="Energy Level",
        showlegend=False,
        margin=dict(l=60, r=60, t=40, b=60)
    ))
    
    fig.update_layout(**layout_update)
    return fig 