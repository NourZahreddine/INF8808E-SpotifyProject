import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from .utils import df, get_modern_layout

def create_danceability_engagement():
    df['danceability_range'] = pd.cut(df['danceability'], 
                                     bins=[0, 0.3, 0.5, 0.9, 1.0], 
                                     labels=['Low Dance (0-0.3)', 'Medium Dance (0.3-0.5)', 'High Dance (0.5-0.9)', 'Very High Dance (0.9-1.0)'])
    
    engagement_stats = df.groupby('danceability_range').agg({
        'popularity': ['mean', 'std', 'count'],
        'energy': 'mean',
        'valence': 'mean'
    }).round(2)
    
    engagement_stats.columns = ['avg_popularity', 'popularity_std', 'track_count', 'avg_energy', 'avg_valence']
    engagement_stats = engagement_stats.reset_index()
    
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=['Danceability vs Popularity Distribution', 'Average Metrics by Danceability Range'],
        specs=[[{"type": "xy"}, {"type": "xy"}]],
        horizontal_spacing=0.15
    )
    
    sample_df = df.sample(n=min(8000, len(df)), random_state=42)
    colors = ['#1DB954', '#f39c12', '#e94560', '#9b59b6']
    
    for i, dance_range in enumerate(engagement_stats['danceability_range']):
        range_data = sample_df[sample_df['danceability_range'] == dance_range]
        fig.add_trace(
            go.Scatter(
                x=range_data['danceability'],
                y=range_data['popularity'],
                mode='markers',
                name=dance_range,
                marker=dict(
                    color=colors[i],
                    size=4,
                    opacity=0.6,
                    line=dict(width=0.3, color='#FFFFFF')
                ),
                hovertemplate=
                "<b>%{y}</b>" +
                "<extra></extra>",
                customdata=range_data[['track_name']].values
            ),
            row=1, col=1
        )
    
    fig.add_trace(
        go.Bar(
            x=engagement_stats['danceability_range'],
            y=engagement_stats['avg_popularity'],
            marker=dict(
                color=colors,
                line=dict(color='#FFFFFF', width=1)
            ),
            text=engagement_stats['avg_popularity'].round(1),
            textposition='outside',
            textfont=dict(color='#FFFFFF', size=11),
            hovertemplate=
            "<b>%{x}</b><br>" +
            "Avg Popularity: <b>%{y:.1f}</b><br>" +
            "Track Count: <b>%{customdata:,}</b>" +
            "<extra></extra>",
            customdata=engagement_stats['track_count'],
            showlegend=False
        ),
        row=1, col=2
    )
    
    layout_update = get_modern_layout()
    layout_update.update(dict(
        height=400,
        title_text="",
        legend=dict(
            orientation="v",
            yanchor="top",
            y=1,
            xanchor="left",
            x=1.02,
            bgcolor="rgba(25, 25, 25, 0.9)",
            bordercolor="rgba(29, 185, 84, 0.3)",
            borderwidth=1,
            font=dict(color='#FFFFFF', size=11)
        )
    ))
    
    fig.update_xaxes(title_text="Danceability Level", row=1, col=1)
    fig.update_yaxes(title_text="Popularity Score", row=1, col=1)
    fig.update_xaxes(title_text="Danceability Range", row=1, col=2)
    fig.update_yaxes(title_text="Average Popularity", row=1, col=2)
    
    fig.update_layout(**layout_update)
    return fig 