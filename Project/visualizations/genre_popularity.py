import plotly.express as px
from .utils import df, get_modern_layout

def create_genre_popularity_chart():

    genre_stats = df.groupby('track_genre').agg({
        'popularity': ['mean', 'std', 'count'],
        'duration_ms': 'mean',
        'energy': 'mean',
        'danceability': 'mean'
    }).round(2)
    
    genre_stats.columns = ['avg_popularity', 'popularity_std', 'track_count', 'avg_duration', 'avg_energy', 'avg_danceability']
    

    most_popular_tracks = df.loc[df.groupby('track_genre')['popularity'].idxmax()][['track_genre', 'track_name', 'artists', 'popularity']]
    genre_stats = genre_stats.merge(most_popular_tracks.set_index('track_genre'), left_index=True, right_index=True)
    genre_stats.rename(columns={'track_name': 'most_popular_track', 'artists': 'top_artist', 'popularity': 'max_popularity'}, inplace=True)
    
    top_genres = genre_stats.nlargest(20, 'avg_popularity')
    
    # Format duration properly
    top_genres['duration_formatted'] = top_genres['avg_duration'].apply(
        lambda x: f"{int(x//60000)}:{int((x%60000)//1000):02d}"
    )
    
    fig = px.bar(
        x=top_genres['avg_popularity'],
        y=top_genres.index,
        orientation='h',
        title=" ",
        labels={'x': '<b>Average Popularity Score</b>', 'y': ''},
        custom_data=[
            top_genres['duration_formatted'], 
            top_genres['most_popular_track'],
            top_genres['top_artist'],
            top_genres['track_count'],
            top_genres['popularity_std'],
            top_genres['avg_energy'],
            top_genres['avg_danceability'],
            top_genres['max_popularity']
        ]
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
        marker_line_color='#FFFFFF',
        marker_line_width=1,
        textposition='outside',
        texttemplate='%{x:.1f}',
        textfont=dict(color='#FFFFFF', size=10, family='Inter'),
        hovertemplate=
        "<b style='color:#43E97B; font-size:14px;'>%{y}</b><br>" +
        "<span style='color:#FFFFFF'>Average Popularity: <b>%{x:.1f}</b></span><br>" +
        "<span style='color:#FFFFFF'>Total Tracks: <b>%{customdata[3]:,}</b></span><br>" +
        "<span style='color:#FFFFFF'>Std Deviation: <b>%{customdata[4]:.1f}</b></span><br>" +
        "<span style='color:#FFFFFF'>Average Duration: <b>%{customdata[0]}</b></span><br>" +
        "<span style='color:#FFFFFF'>Average Energy: <b>%{customdata[5]:.3f}</b></span><br>" +
        "<span style='color:#FFFFFF'>Average Danceability: <b>%{customdata[6]:.3f}</b></span><br>" +
        "<br><span style='color:#43E97B'>🏆 Top Track:</span><br>" +
        "<span style='color:#FFFFFF'><b>%{customdata[1]}</b></span><br>" +
        "<span style='color:#FFFFFF'>by %{customdata[2]}</span><br>" +
        "<span style='color:#FFFFFF'>Popularity: <b>%{customdata[7]}</b></span>" +
        "<extra></extra>"
    )
    
    layout_update = get_modern_layout()
    layout_update.update(dict(
        height=500,  
        showlegend=False,
        yaxis_title='<b>Music Genre</b>',
        xaxis_title='<b>Average Popularity Score</b>',
        margin=dict(l=150, r=60, t=50, b=60),  
        yaxis=dict(
            gridcolor="rgba(67, 233, 123, 0.2)",
            color='#B8B8B8',
            zerolinecolor="rgba(67, 233, 123, 0.3)",
            tickfont=dict(size=11, family='Inter'),
            side='left',
            categoryorder='total ascending'  
        ),
        xaxis=dict(
            gridcolor="rgba(67, 233, 123, 0.2)",
            color='#B8B8B8',
            zerolinecolor="rgba(67, 233, 123, 0.3)",
            tickfont=dict(size=11, family='Inter'),
            range=[0, top_genres['avg_popularity'].max() * 1.1]  
        ),
        hoverlabel=dict(
            bgcolor="rgba(25, 25, 25, 0.95)",
            bordercolor="rgba(29, 185, 84, 0.8)",
            font=dict(color="white", size=12, family='Inter')
        )
    ))
    

    fig.add_annotation(
        text="<i>Hover over bars for detailed genre statistics and top tracks</i>",
        xref="paper", yref="paper",
        x=0.5, y=-0.12,
        showarrow=False,
        font=dict(size=10, color='#B8B8B8'),
        align="center"
    )
    
    fig.update_layout(**layout_update)
    return fig 