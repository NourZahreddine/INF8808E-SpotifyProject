import plotly.graph_objects as go
from plotly.subplots import make_subplots
from .utils import get_modern_layout

def create_energy_time_analysis(data=None):
    if data is None:
        import pandas as pd
        data = pd.read_csv('data/dataset.csv')
    
    sample_df = data.sample(n=min(12000, len(data)), random_state=42)
    
    sample_df['energy_category'] = sample_df['energy'].apply(lambda x: 'High Energy (0.7+)' if x >= 0.7 else 'Medium Energy (0.4-0.7)' if x >= 0.4 else 'Low Energy (0-0.4)')
    
    fig = make_subplots(
        rows=2, cols=1,
        subplot_titles=[
            '<b>Energy vs Popularity Correlation</b>',
            '<b>Energy Category Comparison</b>'
        ],
        specs=[[{"type": "xy"}],
               [{"type": "xy"}]],
        vertical_spacing=0.45,
        row_heights=[0.6, 0.4]
    )
    
    ordered_categories = ['Low Energy (0-0.4)', 'Medium Energy (0.4-0.7)', 'High Energy (0.7+)']
    colors = {
        'Low Energy (0-0.4)': '#43E97B',    
        'Medium Energy (0.4-0.7)': '#1DB954', 
        'High Energy (0.7+)': '#0D7D2C'     
    }
    
    for category in ordered_categories:
        if category in sample_df['energy_category'].unique():
            category_data = sample_df[sample_df['energy_category'] == category]
            fig.add_trace(
                go.Scatter(
                    x=category_data['energy'],
                    y=category_data['popularity'],
                    mode='markers',
                    name=category,
                    marker=dict(
                        color=colors[category],
                        size=5,
                        opacity=0.7,
                        line=dict(width=0.5, color='#FFFFFF')
                    ),
                    hovertemplate=
                    "<b>Track Information</b><br>" +
                    "Track: <b>%{customdata[0]}</b><br>" +
                    "Artist: <b>%{customdata[1]}</b><br>" +
                    "Energy: <b>%{x:.3f}</b><br>" +
                    "Popularity: <b>%{y}</b><br>" +
                    "Category: <b>" + category + "</b>" +
                    "<extra></extra>",
                    customdata=category_data[['track_name', 'artists']].values
                ),
                row=1, col=1
            )
    
    energy_stats = data.groupby(data['energy'].apply(lambda x: 'High Energy (0.7+)' if x >= 0.7 else 'Medium Energy (0.4-0.7)' if x >= 0.4 else 'Low Energy (0-0.4)'))['popularity'].agg(['mean', 'count', 'std']).reset_index()
    energy_stats.columns = ['energy_category', 'avg_popularity', 'track_count', 'std_popularity']
    
    energy_stats['order'] = energy_stats['energy_category'].map({'Low Energy (0-0.4)': 0, 'Medium Energy (0.4-0.7)': 1, 'High Energy (0.7+)': 2})
    energy_stats = energy_stats.sort_values('order')
    
    fig.add_trace(
        go.Bar(
            x=energy_stats['energy_category'],
            y=energy_stats['avg_popularity'],
            marker=dict(
                color=[colors[cat] for cat in energy_stats['energy_category']],
                line=dict(color='#FFFFFF', width=1)
            ),
            text=[f'{val:.1f}' for val in energy_stats['avg_popularity']],
            textposition='outside',
            textfont=dict(color='#FFFFFF', size=12, family='Inter'),
            hovertemplate=
            "<b>%{x}</b><br>" +
            "Average Popularity: <b>%{y:.1f}</b><br>" +
            "Total Tracks: <b>%{customdata[0]:,}</b><br>" +
            "Std Deviation: <b>%{customdata[1]:.1f}</b>" +
            "<extra></extra>",
            customdata=energy_stats[['track_count', 'std_popularity']].values,
            showlegend=False
        ),
        row=2, col=1
    )
    
    layout_update = get_modern_layout()
    layout_update.update(dict(
        height=650,
        title_text="",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.08,
            xanchor="center",
            x=0.5,
            bgcolor="rgba(25, 25, 25, 0.9)",
            bordercolor="rgba(29, 185, 84, 0.3)",
            borderwidth=1,
            font=dict(color='#FFFFFF', size=11)
        ),
        margin=dict(l=70, r=70, t=180, b=100)
    ))
    
    fig.update_xaxes(
        title_text="<b>Energy Level (0.0 - 1.0)</b>", 
        row=1, col=1,
        gridcolor="rgba(29, 185, 84, 0.2)",
        color='#B8B8B8',
        tickfont=dict(size=11),
        titlefont=dict(size=12)
    )
    fig.update_yaxes(
        title_text="<b>Popularity Score</b>", 
        row=1, col=1,
        gridcolor="rgba(29, 185, 84, 0.2)",
        color='#B8B8B8',
        tickfont=dict(size=11),
        titlefont=dict(size=12)
    )
    fig.update_xaxes(
        title_text="<b>Energy Category</b>", 
        row=2, col=1,
        gridcolor="rgba(29, 185, 84, 0.2)",
        color='#B8B8B8',
        tickfont=dict(size=11),
        titlefont=dict(size=12)
    )
    fig.update_yaxes(
        title_text="<b>Average Popularity</b>", 
        row=2, col=1,
        gridcolor="rgba(29, 185, 84, 0.2)",
        color='#B8B8B8',
        tickfont=dict(size=11),
        titlefont=dict(size=12),
        range=[energy_stats['avg_popularity'].min() * 0.95, energy_stats['avg_popularity'].max() * 1.1]
    )
    
    fig.update_annotations(font=dict(size=14, color='#FFFFFF'))
    
    fig.update_layout(**layout_update)
    return fig 