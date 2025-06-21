import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from .utils import get_modern_layout

def create_audio_features_correlation(data=None):

    if data is None:
        data = pd.read_csv('data/dataset.csv')
    

    df_work = data.copy()
   
    df_work['energy_bins'] = pd.cut(df_work['energy'], bins=4, labels=['Low Energy', 'Med Energy', 'High Energy', 'Very High Energy'])
    df_work['danceability_bins'] = pd.cut(df_work['danceability'], bins=4, labels=['Low Dance', 'Med Dance', 'High Dance', 'Very High Dance'])
    df_work['valence_bins'] = pd.cut(df_work['valence'], bins=4, labels=['Low Valence', 'Med Valence', 'High Valence', 'Very High Valence'])
    df_work['instrumentalness_bins'] = pd.cut(df_work['instrumentalness'], bins=4, labels=['Vocal', 'Mostly Vocal', 'Mostly Instrumental', 'Instrumental'])
    

    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=[
            'Energy and Danceability', 
            'Energy and Valence',
            'Danceability and Valence',
            'Energy and Vocal/Instrumental'
        ],
        specs=[[{"type": "xy"}, {"type": "xy"}],
               [{"type": "xy"}, {"type": "xy"}]],
        horizontal_spacing=0.12,
        vertical_spacing=0.15
    )
    
    colorscale = [
        [0, '#1a1a2e'],     
        [0.25, '#16213e'],   
        [0.5, '#0f3460'],   
        [0.75, '#e94560'],   
        [1, '#f1c40f']      
    ]
    
    # Energy vs Danceability
    heatmap1_data = df_work.groupby(['energy_bins', 'danceability_bins'])['popularity'].mean().reset_index()
    pivot1 = heatmap1_data.pivot(index='energy_bins', columns='danceability_bins', values='popularity')
    best1 = heatmap1_data.loc[heatmap1_data['popularity'].idxmax()]
    
    fig.add_trace(
        go.Heatmap(
            z=pivot1.values,
            x=pivot1.columns,
            y=pivot1.index,
            colorscale=colorscale,
            showscale=False,
            hovertemplate="<b>%{y} + %{x}</b><br>Avg Popularity: <b>%{z:.1f}</b><extra></extra>"
        ),
        row=1, col=1
    )
    
    # Energy vs Valence  
    heatmap2_data = df_work.groupby(['energy_bins', 'valence_bins'])['popularity'].mean().reset_index()
    pivot2 = heatmap2_data.pivot(index='energy_bins', columns='valence_bins', values='popularity')
    best2 = heatmap2_data.loc[heatmap2_data['popularity'].idxmax()]
    
    fig.add_trace(
        go.Heatmap(
            z=pivot2.values,
            x=pivot2.columns,
            y=pivot2.index,
            colorscale=colorscale,
            showscale=False,
            hovertemplate="<b>%{y} + %{x}</b><br>Avg Popularity: <b>%{z:.1f}</b><extra></extra>"
        ),
        row=1, col=2
    )
    
    # Danceability vs Valence
    heatmap3_data = df_work.groupby(['danceability_bins', 'valence_bins'])['popularity'].mean().reset_index()
    pivot3 = heatmap3_data.pivot(index='danceability_bins', columns='valence_bins', values='popularity')
    best3 = heatmap3_data.loc[heatmap3_data['popularity'].idxmax()]
    
    fig.add_trace(
        go.Heatmap(
            z=pivot3.values,
            x=pivot3.columns,
            y=pivot3.index,
            colorscale=colorscale,
            showscale=False,
            hovertemplate="<b>%{y} + %{x}</b><br>Avg Popularity: <b>%{z:.1f}</b><extra></extra>"
        ),
        row=2, col=1
    )
    
    # Energy vs Instrumentalness
    heatmap4_data = df_work.groupby(['energy_bins', 'instrumentalness_bins'])['popularity'].mean().reset_index()
    pivot4 = heatmap4_data.pivot(index='energy_bins', columns='instrumentalness_bins', values='popularity')
    best4 = heatmap4_data.loc[heatmap4_data['popularity'].idxmax()]
    
    fig.add_trace(
        go.Heatmap(
            z=pivot4.values,
            x=pivot4.columns,
            y=pivot4.index,
            colorscale=colorscale,
            showscale=True,
            hovertemplate="<b>%{y} + %{x}</b><br>Avg Popularity: <b>%{z:.1f}</b><extra></extra>",
            colorbar=dict(
                title="Popularity",
                titlefont=dict(color='#FFFFFF', size=12),
                tickfont=dict(color='#FFFFFF', size=10),
                len=0.5,
                y=0.25
            )
        ),
        row=2, col=2
    )
    
    layout_update = get_modern_layout()
    layout_update.update(dict(
        height=700,
        title_text="",
        margin=dict(l=80, r=120, t=120, b=80),
        hoverlabel=dict(
            bgcolor="rgba(25, 25, 25, 0.9)",
            bordercolor="rgba(29, 185, 84, 0.5)",
            font_color="white"
        )
    ))
    
    fig.update_layout(**layout_update)
    return fig 