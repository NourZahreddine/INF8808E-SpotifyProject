import plotly.graph_objects as go
from plotly.subplots import make_subplots
from .utils import df, get_modern_layout

def create_explicit_content_analysis():
    explicit_stats = df.groupby('explicit').agg({
        'popularity': ['mean', 'std', 'count']
    }).round(2)
    
    explicit_stats.columns = ['avg_popularity', 'popularity_std', 'track_count']
    explicit_stats = explicit_stats.reset_index()
    explicit_stats['label'] = explicit_stats['explicit'].map({True: 'Explicit', False: 'Clean'})
    
    genre_explicit = df.groupby(['track_genre', 'explicit'])['popularity'].mean().unstack(fill_value=0)
    top_genres_explicit = genre_explicit.head(10)
    
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=['Overall: Explicit vs Clean', 'By Genre: Explicit vs Clean'],
        specs=[[{"type": "xy"}, {"type": "xy"}]],
        horizontal_spacing=0.15
    )
    
    colors = ['#1DB954', '#0A5D1F']  
    fig.add_trace(
        go.Bar(
            x=explicit_stats['label'],
            y=explicit_stats['avg_popularity'],
            marker=dict(
                color=colors,
                line=dict(color='#FFFFFF', width=1)
            ),
            text=explicit_stats['avg_popularity'].round(1),
            textposition='outside',
            textfont=dict(color='#FFFFFF', size=12),
            hovertemplate=
            "<b>%{x} Tracks</b><br>" +
            "Avg Popularity: <b>%{y:.1f}</b><br>" +
            "Track Count: <b>%{customdata:,}</b>" +
            "<extra></extra>",
            customdata=explicit_stats['track_count']
        ),
        row=1, col=1
    )
    
    fig.add_trace(
        go.Bar(
            x=top_genres_explicit.index,
            y=top_genres_explicit[True],
            name='Explicit',
            marker_color='#0A5D1F' 
        ),
        row=1, col=2
    )
    
    fig.add_trace(
        go.Bar(
            x=top_genres_explicit.index,
            y=top_genres_explicit[False],
            name='Clean',
            marker_color='#1DB954'  
        ),
        row=1, col=2
    )
    
    layout_update = get_modern_layout()
    layout_update.update(dict(
        height=500,
        title_text="",
        barmode='group'
    ))
    
    fig.update_xaxes(title_text="Content Type", row=1, col=1)
    fig.update_yaxes(title_text="Average Popularity", row=1, col=1)
    fig.update_xaxes(title_text="Genre", row=1, col=2, tickangle=45)
    fig.update_yaxes(title_text="Average Popularity", row=1, col=2)
    
    fig.update_layout(**layout_update)
    return fig 