import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from .utils import get_modern_layout

def create_danceability_engagement(data=None):
    if data is None:
        data = pd.read_csv('data/dataset.csv')

    data['danceability_range'] = pd.cut(data['danceability'], 
                                     bins=[0, 0.3, 0.5, 0.9, 1.0], 
                                     labels=['Low Danceability (0-0.3)', 'Medium Danceability (0.3-0.5)', 'High Danceability (0.5-0.9)', 'Very High Danceability (0.9-1.0)'])
    
    engagement_stats = data.groupby('danceability_range').agg({
        'popularity': ['mean', 'std', 'count'],
        'energy': 'mean',
        'valence': 'mean'
    }).round(2)
    
    engagement_stats.columns = ['avg_popularity', 'popularity_std', 'track_count', 'avg_energy', 'avg_valence']
    engagement_stats = engagement_stats.reset_index()
    
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=['<b>Danceability vs Popularity Distribution</b>', '<b>Average Metrics by Danceability Range</b>'],
        specs=[[{"type": "xy"}, {"type": "xy"}]],
        horizontal_spacing=0.15
    )
    
    sample_df = data.sample(n=min(8000, len(data)), random_state=42)
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
                    size=5,
                    opacity=0.7,
                    line=dict(width=0.5, color='#FFFFFF')
                ),
                hovertemplate=
                "<b>Track Information</b><br>" +
                "Track: %{customdata[0]}<br>" +
                "Artist: %{customdata[1]}<br>" +
                "Danceability: %{x:.3f}<br>" +
                "Popularity: <b>%{y}</b><br>" +
                "Energy: %{customdata[2]:.3f}<br>" +
                "Valence: %{customdata[3]:.3f}" +
                "<extra></extra>",
                customdata=range_data[['track_name', 'artists', 'energy', 'valence']].values
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
            text=[f'{val:.1f}' for val in engagement_stats['avg_popularity']],
            textposition='outside',
            textfont=dict(color='#FFFFFF', size=12, family='Inter'),
            hovertemplate=
            "<b>%{x}</b><br>" +
            "Average Popularity: <b>%{y:.1f}</b><br>" +
            "Total Tracks: <b>%{customdata[0]:,}</b><br>" +
            "Std Deviation: %{customdata[1]:.1f}<br>" +
            "Average Energy: %{customdata[2]:.3f}<br>" +
            "Average Valence: %{customdata[3]:.3f}" +
            "<extra></extra>",
            customdata=engagement_stats[['track_count', 'popularity_std', 'avg_energy', 'avg_valence']].values,
            showlegend=False
        ),
        row=1, col=2
    )
    
    layout_update = get_modern_layout()
    layout_update.update(dict(
        height=450,
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
    
    fig.update_xaxes(title_text="<b>Danceability Level</b>", row=1, col=1, titlefont=dict(size=12))
    fig.update_yaxes(title_text="<b>Popularity Score</b>", row=1, col=1, titlefont=dict(size=12))
    fig.update_xaxes(title_text="<b>Danceability Range</b>", row=1, col=2, titlefont=dict(size=12))
    fig.update_yaxes(title_text="<b>Average Popularity</b>", row=1, col=2, titlefont=dict(size=12))
    
    max_pop = engagement_stats['avg_popularity'].max()
    fig.update_yaxes(range=[0, max_pop * 1.15], row=1, col=2)
    
    fig.update_annotations(font=dict(size=14, color='#FFFFFF'))
    
    fig.update_layout(**layout_update)
    return fig 