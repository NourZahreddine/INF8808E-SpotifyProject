import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from scipy import stats

df = pd.read_csv('data/dataset.csv')

PRIMARY_BLUE = '#667EEA'
SECONDARY_PURPLE = '#764BA2'
ACCENT_PINK = '#F093FB'
ACCENT_ORANGE = '#F9844A'
ACCENT_TEAL = '#4FACFE'
ACCENT_GREEN = '#43E97B'

modern_colors = ['#667EEA', '#764BA2', '#F093FB', '#F9844A', '#4FACFE', '#43E97B', '#A855F7', '#06B6D4']

def get_modern_layout():
    return dict(
        plot_bgcolor='#191919',
        paper_bgcolor='#191919',
        font=dict(color='#FFFFFF', family="Inter, Arial, sans-serif", size=12),
        title_font=dict(size=24, color='#FFFFFF', family="Inter, Arial, sans-serif"),
        legend=dict(
            bgcolor="rgba(25, 25, 25, 0.9)",
            bordercolor="rgba(29, 185, 84, 0.3)",
            borderwidth=1,
            font=dict(color='#FFFFFF', size=11),
            title=dict(font=dict(color='#FFFFFF', size=12))
        ),
        xaxis=dict(
            gridcolor="rgba(29, 185, 84, 0.2)",
            color='#B8B8B8',
            zerolinecolor="rgba(29, 185, 84, 0.3)",
            tickfont=dict(size=11)
        ),
        yaxis=dict(
            gridcolor="rgba(29, 185, 84, 0.2)",
            color='#B8B8B8',
            zerolinecolor="rgba(29, 185, 84, 0.3)",
            tickfont=dict(size=11)
        ),
        margin=dict(l=60, r=40, t=80, b=60)
    ) 