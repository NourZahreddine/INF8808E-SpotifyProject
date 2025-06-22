import streamlit as st
from visualizations import (
    create_genre_popularity_chart, 
    create_audio_features_correlation, 
    create_energy_time_analysis,
    create_danceability_engagement,
    create_consistent_artists,
    create_track_length_viral,
    create_energy_by_genre,
    create_tempo_loudness_analysis,
    create_explicit_content_analysis
)
import pandas as pd

st.set_page_config(
    page_title="Analyzing the Beat",
    page_icon=" ",
    layout="wide",
    initial_sidebar_state="collapsed"
)

@st.cache_data
def load_data():
    return pd.read_csv('data/dataset.csv')

df = load_data()

@st.cache_data
def filter_data_by_genre(df, selected_genres):
    if 'All Genres' in selected_genres or not selected_genres:
        return df
    return df[df['track_genre'].isin(selected_genres)]

@st.cache_data
def filter_data(df, selected_genres, explicit_filter):
    """Filter data by both genre and explicit content"""
    filtered_df = df.copy()
    
    # Filter by genre
    if selected_genres and 'All Genres' not in selected_genres:
        filtered_df = filtered_df[filtered_df['track_genre'].isin(selected_genres)]
    
    # Filter by explicit content
    if explicit_filter == "Explicit Only":
        filtered_df = filtered_df[filtered_df['explicit'] == True]
    elif explicit_filter == "Non-Explicit Only":
        filtered_df = filtered_df[filtered_df['explicit'] == False]
    # "All" means no filtering by explicit content
    
    return filtered_df

def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

load_css('style.css')


if 'active_tab' not in st.session_state:
    st.session_state.active_tab = "Track's Popularity"

if 'graph_indices' not in st.session_state:
    st.session_state.graph_indices = {
        "Track's Popularity": 0,
        "Audience Analysis": 0,
        "Track Analysis": 0
    }

if 'show_onboarding' not in st.session_state:
    st.session_state.show_onboarding = True


st.markdown("""
<div class="header-container">
    <div>
        <h1 class="main-header">Analyzing the Beat</h1>
        <p class="subtitle">Insights from Spotify's Music Dataset | 114,000 Tracks Analyzed</p>
    </div>
</div>
""", unsafe_allow_html=True)

if 'filter_panel_open' not in st.session_state:
    st.session_state.filter_panel_open = False

all_genres = sorted(df['track_genre'].unique())
genre_options = ['All Genres'] + all_genres


if 'show_filter' not in st.session_state:
    st.session_state.show_filter = False


# Get current filter selection and apply filtering
selected_genres = st.session_state.get('genre_filter', ['All Genres'])
filtered_df = filter_data_by_genre(df, selected_genres)

# Update filtered_df whenever genre_filter changes
if 'genre_filter' in st.session_state:
    filtered_df = filter_data_by_genre(df, st.session_state['genre_filter'])

tab_descriptions = {
    "Track's Popularity": {
        "description": "Explore what makes tracks popular on Spotify",
        "insights": "Discover genre trends, audio feature combinations, and energy patterns"
    },
    "Audience Analysis": {
        "description": "Understand how listeners engage with different track characteristics", 
        "insights": "Analyze danceability impact, artist consistency, and viral track patterns"
    },
    "Track Analysis": {
        "description": "Deep dive into track characteristics and their effects",
        "insights": "Examine energy by genre, tempo-loudness relationships, and explicit content impact"
    }
}

graph_config = {
    "Track's Popularity": {
        "graphs": [
            {
                "title": "Top 20 Genres by Average Popularity", 
                "func": create_genre_popularity_chart,
                "description": "Which music genres consistently achieve higher popularity scores on Spotify? This analysis reveals the most successful genres.",
                "insights": ["Electronic and pop genres dominate popularity rankings", "Traditional genres show varying success patterns", "Emerging genres demonstrate growth potential"]
            },
            {
                "title": "Audio Feature Combinations + Vocal vs Instrumental", 
                "func": create_audio_features_correlation,
                "description": "How do different audio characteristics work together to create popular tracks? Explore the relationships between features like energy, danceability, and vocal content.",
                "insights": ["High-energy tracks often correlate with high danceability", "Vocal tracks generally outperform instrumental ones", "Sweet spots exist for feature combinations"]
            },
            {
                "title": "Energy Correlation + Energy Trends Over Time", 
                "func": create_energy_time_analysis,
                "description": "Track the evolution of energy levels in popular music and understand how energy correlates with other musical features.",
                "insights": ["Music energy levels have evolved over decades", "Energy strongly correlates with listener engagement", "Genre-specific energy patterns exist"]
            }
        ]
    },
    "Audience Analysis": {
        "graphs": [
            {
                "title": "How Does Danceability Affect Listener Engagement?", 
                "func": create_danceability_engagement,
                "description": "Explore the relationship between a track's danceability score and its popularity. Do more danceable tracks perform better?",
                "insights": ["Moderate danceability often performs best", "Different genres have optimal danceability ranges", "Danceability correlates with energy and valence"]
            },
            {
                "title": "Which Artists Consistently Produce Popular Tracks?", 
                "func": create_consistent_artists,
                "description": "Identify artists who regularly create popular content and understand what makes them successful.",
                "insights": ["Top artists maintain consistent quality", "Genre specialization leads to reliability", "Popular artists adapt to trends while maintaining style"]
            },
            {
                "title": "Are Longer or Shorter Tracks More Likely to Go Viral?", 
                "func": create_track_length_viral,
                "description": "Analyze the relationship between track duration and popularity to understand optimal song lengths.",
                "insights": ["Optimal track length varies by genre", "Streaming platforms influence length preferences", "Attention span considerations affect virality"]
            }
        ]
    },
    "Track Analysis": {
        "graphs": [
            {
                "title": "How Does Energy Level Vary by Genre?", 
                "func": create_energy_by_genre,
                "description": "Compare energy distributions across different music genres to understand genre-specific characteristics.",
                "insights": ["Each genre has distinct energy signatures", "High-energy genres dominate certain contexts", "Energy variance differs significantly by genre"]
            },
            {
                "title": "Tempo & Loudness vs Popularity", 
                "func": create_tempo_loudness_analysis,
                "description": "Examine how tempo and loudness interact to influence track success and listener preference.",
                "insights": ["Optimal tempo-loudness combinations exist", "Genre influences ideal tempo ranges", "Loudness wars impact modern music"]
            },
            {
                "title": "How Does Explicit Content Affect Track Popularity?", 
                "func": create_explicit_content_analysis,
                "description": "Understand the impact of explicit content on track performance across different contexts and demographics.",
                "insights": ["Explicit content effects vary by genre", "Platform policies influence explicit track success", "Audience preferences differ by demographic"]
            }
        ]
    }
}

if st.session_state.show_onboarding:
    st.info("""
    👋 **Welcome to Analyzing the Beat!** 
    
    This dashboard analyzes 114,000 Spotify tracks to uncover music trends and patterns. 
    
    **How to navigate:**
    - Use the tabs below to explore different aspects of music data
    - Click "Next →" and "← Back" to browse through visualizations
    - Hover over charts for detailed information
    - Each section provides insights to guide your analysis
    
    Click the close button to dismiss this message.
    """)
    
    if st.button("CLOSE BUTTON", key="dismiss_onboarding"):
        st.session_state.show_onboarding = False
        st.rerun()


st.markdown('<div class="main-content-area">', unsafe_allow_html=True)

st.markdown("---")

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("Track's Popularity", key="tab1", use_container_width=True, 
                type="primary" if st.session_state.active_tab == "Track's Popularity" else "secondary"):
        st.session_state.active_tab = "Track's Popularity"
        st.rerun()
with col2:
    if st.button("Audience Analysis", key="tab2", use_container_width=True, 
                type="primary" if st.session_state.active_tab == "Audience Analysis" else "secondary"):
        st.session_state.active_tab = "Audience Analysis"
        st.rerun()
with col3:
    if st.button("Track Analysis", key="tab3", use_container_width=True, 
                type="primary" if st.session_state.active_tab == "Track Analysis" else "secondary"):
        st.session_state.active_tab = "Track Analysis"
        st.rerun()

current_tab_info = tab_descriptions[st.session_state.active_tab]
st.markdown(f"""
<div style='background: linear-gradient(135deg, rgba(29, 185, 84, 0.1) 0%, rgba(67, 233, 123, 0.1) 100%); 
           padding: 1rem; border-radius: 10px; border-left: 4px solid #43E97B; margin: 1rem 0;'>
    <h4 style='color: #43E97B; margin: 0;'>{current_tab_info['description']}</h4>
    <p style='color: #B8B8B8; margin: 0.5rem 0 0 0; font-style: italic;'>{current_tab_info['insights']}</p>
</div>
""", unsafe_allow_html=True)


if 'show_filter' not in st.session_state:
    st.session_state.show_filter = False

if st.button("Filters", key="filter_toggle", help="Click to show/hide genre filter"):
    st.session_state.show_filter = not st.session_state.show_filter


if st.session_state.show_filter:
    st.markdown("### Select Filters:")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Genre filter
        st.markdown("**Filter by Genre:**")
        selected_genres = st.multiselect(
            "Choose genres:",
            options=genre_options,
            default=st.session_state.get('genre_filter', ['All Genres']),
            key="genre_filter"
        )
        
        # Explicit content filter
        st.markdown("**Filter by Content:**")
        explicit_options = ["All", "Explicit Only", "Non-Explicit Only"]
        explicit_filter = st.selectbox(
            "Choose content type:",
            options=explicit_options,
            index=0,
            key="explicit_filter"
        )
    
    with col2:
        # Get the current filter selections from session state
        current_genres = st.session_state.get('genre_filter', ['All Genres'])
        current_explicit = st.session_state.get('explicit_filter', 'All')
        current_filtered_df = filter_data(df, current_genres, current_explicit)
        
        # Display filter status
        st.markdown("**Filter Status:**")
        
        # Genre status
        if 'All Genres' not in current_genres and current_genres:
            st.success(f"**{len(current_genres)}** genres selected")
        else:
            st.info("**All genres**")
        
        # Explicit status
        if current_explicit == "Explicit Only":
            st.warning("**Explicit tracks only**")
        elif current_explicit == "Non-Explicit Only":
            st.success("**Clean tracks only**")
        else:
            st.info("**All content types**")
        
        # Total tracks
        st.metric("Filtered Tracks", f"{len(current_filtered_df):,}")
    
    st.markdown("---")

st.markdown('<div class="main-content">', unsafe_allow_html=True)

def display_graph_with_navigation(tab_name, tab_key):
    """Display current graph with navigation and enhanced information"""

    current_genres = st.session_state.get('genre_filter', ['All Genres'])
    current_explicit = st.session_state.get('explicit_filter', 'All')
    current_filtered_df = filter_data(df, current_genres, current_explicit)
    
    if tab_name not in st.session_state.graph_indices:
        st.session_state.graph_indices[tab_name] = 0
    
    current_index = st.session_state.graph_indices[tab_name]
    graphs = graph_config[tab_name]["graphs"]
    
    if current_index >= len(graphs):
        st.session_state.graph_indices[tab_name] = 0
        current_index = 0
    elif current_index < 0:
        st.session_state.graph_indices[tab_name] = len(graphs) - 1
        current_index = len(graphs) - 1
    
    current_graph = graphs[current_index]
    

    st.markdown(f"""
    <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;'>
        <p class="graph-counter">Graph {current_index + 1} of {len(graphs)}</p>
        <p style='color: #B8B8B8; font-size: 0.9rem;'>Use navigation buttons below to explore all visualizations</p>
    </div>
    """, unsafe_allow_html=True)
    

    st.markdown(f"### {current_graph['title']}")
    st.markdown(f"<p style='color: #B8B8B8; font-style: italic; margin-bottom: 1rem;'>{current_graph['description']}</p>", unsafe_allow_html=True)
    
    # Add helpful subtitle based on the graph type
    if "Genre" in current_graph['title'] and "Popularity" in current_graph['title']:
        st.markdown("<p style='color: #B8B8B8; font-size: 0.9rem; margin-bottom: 1rem;'><i>💡 Hover over bars for detailed genre statistics and top tracks</i></p>", unsafe_allow_html=True)
    elif "Energy" in current_graph['title'] and "Time" in current_graph['title']:
        st.markdown("<p style='color: #B8B8B8; font-size: 0.9rem; margin-bottom: 1rem;'><i>💡 Each point represents a track. Higher energy generally correlates with higher popularity.</i></p>", unsafe_allow_html=True)
    elif "Energy" in current_graph['title'] and "Genre" in current_graph['title']:
        st.markdown("<p style='color: #B8B8B8; font-size: 0.9rem; margin-bottom: 1rem;'><i>💡 Box plots show energy distribution: median (line), quartiles (box), and outliers (points)</i></p>", unsafe_allow_html=True)
    

    try:
        with st.spinner("Loading visualization..."):
            fig = current_graph['func'](current_filtered_df)
            st.plotly_chart(fig, use_container_width=True, key=f"{tab_key}_{current_index}")
    except Exception as e:
        st.error(f"Error loading visualization: {str(e)}")
        st.info("Please try refreshing the page or navigating to a different graph.")
    

    if 'insights' in current_graph:
        with st.expander("Key Insights", expanded=False):
            for insight in current_graph['insights']:
                st.markdown(f"• {insight}")
    

    col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 1, 2])
    
    with col2:
        if current_index > 0:
            if st.button("← Back", key=f"back_{tab_key}", help="Previous graph"):
                st.session_state.graph_indices[tab_name] = max(0, current_index - 1)
                st.rerun()
        else:
            st.markdown("<div style='height: 38px;'></div>", unsafe_allow_html=True)  
    
    with col3:
        st.markdown(f"<div style='text-align: center; color: #43E97B; font-weight: 600; padding: 8px;'>{current_index + 1}/{len(graphs)}</div>", unsafe_allow_html=True)
    
    with col4:
        if current_index < len(graphs) - 1:
            if st.button("Next →", key=f"next_{tab_key}", help="Next graph"):
                st.session_state.graph_indices[tab_name] = min(len(graphs) - 1, current_index + 1)
                st.rerun()
        else:
            st.markdown("<div style='height: 38px;'></div>", unsafe_allow_html=True)  


try:
    if st.session_state.active_tab == "Track's Popularity":
        display_graph_with_navigation("Track's Popularity", "popularity")
    elif st.session_state.active_tab == "Audience Analysis":
        display_graph_with_navigation("Audience Analysis", "audience")
    elif st.session_state.active_tab == "Track Analysis":
        display_graph_with_navigation("Track Analysis", "track")
except Exception as e:
    st.info("Please try refreshing the page.")

st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")

current_genres = st.session_state.get('genre_filter', ['All Genres'])
current_explicit = st.session_state.get('explicit_filter', 'All')
current_filtered_df = filter_data(df, current_genres, current_explicit)

st.markdown(f"""
<div style='text-align: center; color: #FFFFFF; font-size: 0.9rem; margin-top: 2rem;'>
    INF8808E | Data from Spotify Dataset | <strong>{len(current_filtered_df):,} tracks</strong> analyzed across 20+ audio features
</div>
""", unsafe_allow_html=True)
