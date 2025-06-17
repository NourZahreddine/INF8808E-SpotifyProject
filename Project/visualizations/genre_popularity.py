import plotly.express as px
from .utils import df, get_modern_layout

def create_genre_popularity_chart():
    genre_stats = df.groupby('track_genre').agg({
        'popularity': 'mean',
        'duration_ms': 'mean'
    }).round(2)
    
    genre_stats.columns = ['avg_popularity', 'avg_duration']
    
    most_popular_tracks = df.loc[df.groupby('track_genre')['popularity'].idxmax()][['track_genre', 'track_name']]
    genre_stats = genre_stats.merge(most_popular_tracks.set_index('track_genre'), left_index=True, right_index=True)
    genre_stats.rename(columns={'track_name': 'most_popular_track'}, inplace=True)
    
    top_genres = genre_stats.nlargest(20, 'avg_popularity')
    
    top_genres['duration_formatted'] = top_genres['avg_duration'].apply(
        lambda x: f"{int(x//60000)}:{int((x%60000)//1000):02d}"
    )
    
    fig = px.bar(
        x=top_genres['avg_popularity'],
        y=top_genres.index,
        orientation='h',
        title=" ",
        labels={'x': 'Average Popularity Score', 'y': ''},
        custom_data=[top_genres['duration_formatted'], top_genres['most_popular_track']]
    )
    
    colors = []
    n_bars = len(top_genres)
    for i in range(n_bars):
        ratio = i / (n_bars - 1)
        r = int(67 + (26 - 67) * ratio)
        g = int(233 + (120 - 233) * ratio)   
        b = int(123 + (84 - 123) * ratio)
        colors.append(f'rgb({r},{g},{b})')
    
    fig.update_traces(
        marker_color=colors,
        marker_line_color='#191919',
        marker_line_width=0.5,
        textposition='outside',
        texttemplate='%{x:.1f}',
        textfont=dict(color='#FFFFFF', size=9),
        hovertemplate=
        "<b style='color:#FFFFFF'>%{y}</b><br>" +
        "<span style='color:#FFFFFF'>Average Popularity: <b>%{x:.1f}</b></span><br>" +
        "<span style='color:#FFFFFF'>Average Duration: <b>%{customdata[0]}</b></span><br>" +
        "<span style='color:#FFFFFF'>Most Popular Track: <b>%{customdata[1]}</b></span>" +
        "<extra></extra>"
    )
    
    layout_update = get_modern_layout()
    layout_update.update(dict(
        height=450,
        showlegend=False,
        yaxis_title='',
        xaxis_title='Popularity Score',
        margin=dict(l=140, r=40, t=40, b=40),
        yaxis=dict(
            gridcolor="rgba(67, 233, 123, 0.1)",
            color='#B8B8B8',
            zerolinecolor="rgba(67, 233, 123, 0.2)",
            tickfont=dict(size=10),
            side='left'
        ),
        xaxis=dict(
            gridcolor="rgba(67, 233, 123, 0.1)",
            color='#B8B8B8',
            zerolinecolor="rgba(67, 233, 123, 0.2)",
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