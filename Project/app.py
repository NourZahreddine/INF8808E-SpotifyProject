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
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="collapsed"
)

@st.cache_data
def load_data():
    return pd.read_csv('data/dataset.csv')

df = load_data()

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

st.markdown("""
<div class="header-container">
    <div>
        <h1 class="main-header">Analyzing the Beat</h1>
        <p class="subtitle">Insights from Spotify's Music Dataset</p>
    </div>
</div>

<script>
function setActiveTab(tabName) {
    document.querySelectorAll('.header-tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    
    event.target.classList.add('active');
}
</script>
""", unsafe_allow_html=True)

graph_config = {
    "Track's Popularity": {
        "graphs": [
            {"title": "Top 20 Genres by Average Popularity", "func": create_genre_popularity_chart},
            {"title": "Audio Feature Combinations + Vocal vs Instrumental", "func": create_audio_features_correlation},
            {"title": "Energy Correlation + Energy Trends Over Time", "func": create_energy_time_analysis}
        ]
    },
    "Audience Analysis": {
        "graphs": [
            {"title": "How Does Danceability Affect Listener Engagement?", "func": create_danceability_engagement},
            {"title": "Which Artists Consistently Produce Popular Tracks?", "func": create_consistent_artists},
            {"title": "Are Longer or Shorter Tracks More Likely to Go Viral?", "func": create_track_length_viral}
        ]
    },
    "Track Analysis": {
        "graphs": [
            {"title": "How Does Energy Level Vary by Genre?", "func": create_energy_by_genre},
            {"title": "Tempo & Loudness vs Popularity", "func": create_tempo_loudness_analysis},
            {"title": "How Does Explicit Content Affect Track Popularity?", "func": create_explicit_content_analysis}
        ]
    }
}

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("Track's Popularity", key="tab1", use_container_width=True, type="primary" if st.session_state.active_tab == "Track's Popularity" else "secondary"):
        st.session_state.active_tab = "Track's Popularity"
        st.rerun()
with col2:
    if st.button("Audience Analysis", key="tab2", use_container_width=True, type="primary" if st.session_state.active_tab == "Audience Analysis" else "secondary"):
        st.session_state.active_tab = "Audience Analysis"
        st.rerun()
with col3:
    if st.button("Track Analysis", key="tab3", use_container_width=True, type="primary" if st.session_state.active_tab == "Track Analysis" else "secondary"):
        st.session_state.active_tab = "Track Analysis"
        st.rerun()


st.markdown('<div class="main-content">', unsafe_allow_html=True)

def display_graph_with_navigation(tab_name, tab_key):
    """Display current graph with navigation for a tab"""
    current_index = st.session_state.graph_indices[tab_name]
    graphs = graph_config[tab_name]["graphs"]
    current_graph = graphs[current_index]
    
    st.markdown(f'<p class="graph-counter">Graph {current_index + 1} of {len(graphs)}</p>', unsafe_allow_html=True)
    
    st.markdown(f"### {current_graph['title']}")
    
    with st.spinner("Loading visualization..."):
        fig = current_graph['func']()
        st.plotly_chart(fig, use_container_width=True, key=f"{tab_key}_{current_index}")
    
    col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 1, 2])
    
    with col2:
        if current_index > 0:
            if st.button("← Back", key=f"back_{tab_key}", help="Previous graph"):
                st.session_state.graph_indices[tab_name] -= 1
                st.rerun()
    
    with col4:
        if current_index < len(graphs) - 1:
            if st.button("Next →", key=f"next_{tab_key}", help="Next graph"):
                st.session_state.graph_indices[tab_name] += 1
                st.rerun()

if st.session_state.active_tab == "Track's Popularity":
    display_graph_with_navigation("Track's Popularity", "popularity")
elif st.session_state.active_tab == "Audience Analysis":
    display_graph_with_navigation("Audience Analysis", "audience")
elif st.session_state.active_tab == "Track Analysis":
    display_graph_with_navigation("Track Analysis", "track")

st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #43E97B; font-size: 0.9rem; margin-top: 2rem;'>
    INF8808E | Data from Spotify Dataset
</div>
""", unsafe_allow_html=True) 