 # ANALYZING THE BEAT

**INF8808E - Data Visualization**  
**Summer 2025**  
**June 22, 2025**

## Team 15

### Team Composition
- **Mohammad Darandeh** - 2352903
- **Nour Zahreddine** - 2167661  
- **Ismail Sebbahi** - 2012128
- **Fatemeh Nikkhah** - 2266659
- **Bourennani Juba** - 1934122
- **Maha Mubarak** - 2402357

---

## About the Project

An interactive Streamlit dashboard analyzing 114,000 Spotify tracks to see music trends and patterns. This comprehensive visualization tool explores the relationships between various audio features and track popularity across different genres.

## Live Application

**Access the deployed application:** [https://inf8808e-spotifyproject-9rpmq7dgjrmipocpumttlj.streamlit.app](https://inf8808e-spotifyproject-9rpmq7dgjrmipocpumttlj.streamlit.app)

## Running Locally

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/NourZahreddine/INF8808E-SpotifyProject.git
   cd INF8808E-SpotifyProject
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   streamlit run app.py
   ```

4. **Access the app:**
   Open your web browser and navigate to `http://localhost:8501`


## Project Structure

```
├── app.py                 # Main Streamlit application
├── style.css             # Custom CSS styling
├── requirements.txt      # Python dependencies
├── README.md            # Project documentation
├── data/
│   └── dataset.csv      # Spotify tracks dataset (114,000+ tracks)
└── visualizations/
    ├── __init__.py
    ├── utils.py
    ├── genre_popularity.py
    ├── audio_features_correlation.py
    ├── energy_time_analysis.py
    ├── danceability_engagement.py
    ├── consistent_artists.py
    ├── track_length_viral.py
    ├── energy_by_genre.py
    ├── tempo_loudness_analysis.py
    └── explicit_content_analysis.py
```

## Technology Stack

- **Frontend**: Streamlit
- **Data Processing**: Pandas, NumPy
- **Visualizations**: Plotly
- **Statistical Analysis**: SciPy
- **Styling**: Custom CSS with Spotify theme

## Dataset

The application analyzes a comprehensive Spotify dataset containing:
- **114,000+** tracks
- **20+** audio features per track
- **114** unique genres
- Track metadata including popularity scores, energy levels, danceability, and more

---

*This project was developed as part of the INF8808E Data Visualization course at École Polytechnique de Montréal.*