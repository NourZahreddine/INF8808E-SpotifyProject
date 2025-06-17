import plotly.graph_objects as go
from .utils import df, get_modern_layout

def create_consistent_artists():
    solo_artists_df = df[~df['artists'].str.contains(';', na=False)]
    
    artist_stats = solo_artists_df.groupby('artists').agg({
        'popularity': ['mean', 'std', 'count'],
        'track_name': 'count'
    }).round(2)
    
    artist_stats.columns = ['avg_popularity', 'popularity_std', 'track_count', 'total_tracks']
    artist_stats = artist_stats.reset_index()
    
    consistent_artists = artist_stats[artist_stats['track_count'] >= 8].copy()
    
    top_artists = consistent_artists.nlargest(10, 'avg_popularity')
    
    fig = go.Figure()
    
    n_bars = len(top_artists)
    colors = []
    for i in range(n_bars):
        ratio = i / (n_bars - 1) if n_bars > 1 else 0
        r = int(67 + (26 - 67) * ratio)      
        g = int(233 + (120 - 233) * ratio)   
        b = int(123 + (84 - 123) * ratio)   
        colors.append(f'rgb({r},{g},{b})')
    
    fig.add_trace(go.Bar(
        y=top_artists['artists'],
        x=top_artists['avg_popularity'],
        orientation='h',
        marker=dict(
            color=colors,
            line=dict(color='#FFFFFF', width=0.5)
        ),
        text=top_artists['avg_popularity'].round(1),
        textposition='outside',
        textfont=dict(color='#FFFFFF', size=10),
        hovertemplate=
        "<b>%{y}</b><br>" +
        "Avg Popularity: <b>%{x:.1f}</b><br>" +
        "Track Count: <b>%{customdata[0]}</b><br>" +
        "Consistency : <b>%{customdata[1]:.1f}</b>" +
        "<extra></extra>",
        customdata=list(zip(
            top_artists['track_count'], 
            top_artists['popularity_std']
        ))
    ))
    
    layout_update = get_modern_layout()
    layout_update.update(dict(
        height=450,
        title_text="",
        xaxis_title="Average Popularity Score",
        yaxis_title="",
        showlegend=False,
        margin=dict(l=200, r=60, t=40, b=40),
        yaxis=dict(
            gridcolor="rgba(29, 185, 84, 0.1)",
            color='#B8B8B8',
            zerolinecolor="rgba(29, 185, 84, 0.2)",
            tickfont=dict(size=10),
            side='left'
        ),
        xaxis=dict(
            gridcolor="rgba(29, 185, 84, 0.1)",
            color='#B8B8B8',
            zerolinecolor="rgba(29, 185, 84, 0.2)",
            tickfont=dict(size=10)
        ),
        hoverlabel=dict(
            bgcolor="rgba(25, 25, 25, 0.9)",
            bordercolor="rgba(29, 185, 84, 0.5)",
            font_color="white"
        )
    ))
    
    fig.update_layout(**layout_update)
    return fig 