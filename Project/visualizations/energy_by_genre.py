import plotly.graph_objects as go
import plotly.express as px
from .utils import get_modern_layout

def create_energy_by_genre(data=None):
    if data is None:
        import pandas as pd
        data = pd.read_csv('data/dataset.csv')

    top_genres = data['track_genre'].value_counts().head(10).index
    filtered_df = data[data['track_genre'].isin(top_genres)]
    

    genre_stats = filtered_df.groupby('track_genre')['energy'].agg(['mean', 'median', 'std', 'count']).round(3)
    genre_stats = genre_stats.reindex(top_genres)  
    
    fig = go.Figure()
    
    colors = ['#43E97B', '#3AE571', '#32E168', '#29DD5E', '#20D955', '#18D54B', '#0FD142', '#1DB954', '#15B54A', '#0CB240']
    
    for i, genre in enumerate(top_genres):
        genre_data = filtered_df[filtered_df['track_genre'] == genre]['energy']
        genre_info = genre_stats.loc[genre]
        
        fig.add_trace(go.Box(
            y=genre_data,
            name=genre.title(), 
            marker=dict(
                color=colors[i],
                line=dict(color='#FFFFFF', width=1)
            ),
            line=dict(color='#FFFFFF', width=2),
            fillcolor=colors[i],
            opacity=0.8,
            boxpoints='outliers',  
            pointpos=0,
            hovertemplate=
            "<b>%{fullData.name}</b><br>" +
            f"Sample Count: <b>{genre_info['count']:,}</b><br>" +
            f"Mean Energy: <b>{genre_info['mean']:.3f}</b><br>" +
            f"Median Energy: <b>{genre_info['median']:.3f}</b><br>" +
            f"Std Deviation: <b>{genre_info['std']:.3f}</b><br>" +
            "Energy Range: %{y:.3f}<br>" +
            "<extra></extra>",
            customdata=[genre_info['count'], genre_info['mean'], genre_info['median'], genre_info['std']]
        ))
    
    layout_update = get_modern_layout()
    layout_update.update(dict(
        height=500,  
        title_text="",
        xaxis_title="<b>Music Genre</b>",
        yaxis_title="<b>Energy Level (0.0 - 1.0)</b>",
        showlegend=False,
        margin=dict(l=70, r=60, t=50, b=100),  
        xaxis=dict(
            tickangle=45, 
            tickfont=dict(size=11),
            gridcolor="rgba(29, 185, 84, 0.2)",
            color='#B8B8B8',
            zerolinecolor="rgba(29, 185, 84, 0.3)"
        ),
        yaxis=dict(
            gridcolor="rgba(29, 185, 84, 0.2)",
            color='#B8B8B8',
            zerolinecolor="rgba(29, 185, 84, 0.3)",
            tickfont=dict(size=11),
            range=[0, 1] 
        )
    ))
    
    fig.update_layout(**layout_update)
    return fig 