import plotly.graph_objects as go
from plotly.subplots import make_subplots
from .utils import df, get_modern_layout

def create_energy_time_analysis():
    sample_df = df.sample(n=min(12000, len(df)), random_state=42)
    
    sample_df['energy_category'] = sample_df['energy'].apply(lambda x: 'High Energy (0.7+)' if x >= 0.7 else 'Medium Energy (0.4-0.7)' if x >= 0.4 else 'Low Energy (0-0.4)')
    
    fig = make_subplots(
        rows=2, cols=1,
        subplot_titles=[
            'Energy vs Popularity Correlation',
            'Energy Category Comparison'
        ],
        specs=[[{"type": "xy"}],
               [{"type": "xy"}]],
        vertical_spacing=0.25,
        row_heights=[0.55, 0.45]
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
                        size=4,
                        opacity=0.6,
                        line=dict(width=0.3, color='#FFFFFF')
                    ),
                    hovertemplate=
                    "<b>%{customdata[0]}</b><br>" +
                    "Energy: <b>%{x:.2f}</b><br>" +
                    "Popularity: <b>%{y}</b><br>" +
                    "Category: <b>" + category + "</b>" +
                    "<extra></extra>",
                    customdata=category_data[['track_name']].values
                ),
                row=1, col=1
            )
    
    energy_stats = df.groupby(df['energy'].apply(lambda x: 'High Energy (0.7+)' if x >= 0.7 else 'Medium Energy (0.4-0.7)' if x >= 0.4 else 'Low Energy (0-0.4)'))['popularity'].agg(['mean', 'count']).reset_index()
    energy_stats.columns = ['energy_category', 'avg_popularity', 'track_count']
    
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
            text=energy_stats['avg_popularity'].round(1),
            textposition='outside',
            textfont=dict(color='#FFFFFF', size=12),
            hovertemplate=
            "<b>%{x}</b><br>" +
            "Avg Popularity: <b>%{y:.1f}</b><br>" +
            "Track Count: <b>%{customdata:,}</b>" +
            "<extra></extra>",
            customdata=energy_stats['track_count'],
            showlegend=False
        ),
        row=2, col=1
    )
    
    layout_update = get_modern_layout()
    layout_update.update(dict(
        height=400,
        title_text="",
        legend=dict(
            orientation="h",
            yanchor="top",
            y=1.05,
            xanchor="center",
            x=0.5,
            bgcolor="rgba(25, 25, 25, 0.9)",
            bordercolor="rgba(29, 185, 84, 0.3)",
            borderwidth=1,
            font=dict(color='#FFFFFF', size=11)
        ),
        margin=dict(l=60, r=60, t=100, b=60)
    ))
    
    fig.update_xaxes(
        title_text="Energy Level", 
        row=1, col=1,
        gridcolor="rgba(29, 185, 84, 0.2)",
        color='#B8B8B8',
        tickfont=dict(size=11)
    )
    fig.update_yaxes(
        title_text="Popularity Score", 
        row=1, col=1,
        gridcolor="rgba(29, 185, 84, 0.2)",
        color='#B8B8B8',
        tickfont=dict(size=11)
    )
    fig.update_xaxes(
        title_text="Energy Category", 
        row=2, col=1,
        gridcolor="rgba(29, 185, 84, 0.2)",
        color='#B8B8B8',
        tickfont=dict(size=11)
    )
    fig.update_yaxes(
        title_text="Average Popularity", 
        row=2, col=1,
        gridcolor="rgba(29, 185, 84, 0.2)",
        color='#B8B8B8',
        tickfont=dict(size=11),
        range=[30, 37] 
    )
    
    fig.update_layout(**layout_update)
    return fig 