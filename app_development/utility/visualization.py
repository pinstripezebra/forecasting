
#import plotly.plotly as py
import plotly.graph_objects as go
import numpy as np
import pandas as pd


df = pd.read_csv('./Data/test.csv')
def generate_run_plot():

    import plotly.graph_objects as go

    r = df['counts'].tolist()
    theta = np.arange(7.5,368,15)
    width = [15]*24

    ticktexts = [f'$\large{i}$' if i % 6 == 0 else '' for i in np.arange(24)]

    fig = go.Figure(go.Barpolar(
        r=r,
        theta=theta,
        width=width,
        marker_color=df['counts'],
        marker_colorscale='Blues',
        marker_line_color="white",
        marker_line_width=2,
        opacity=0.8
    ))

    fig.update_layout(
        template=None,
        polar=dict(
            hole=0.4,
            bgcolor='rgb(223, 223,223)',
            radialaxis=dict(
                showticklabels=False,
                ticks='',
                linewidth=2,
                linecolor='white',
                showgrid=False,
            ),
            angularaxis=dict(
                tickvals=np.arange(0,360,15),
                ticktext=ticktexts,
                showline=True,
                direction='clockwise',
                period=24,
                linecolor='white',
                gridcolor='white',
                showticklabels=True,
                ticks=''
            )
        )
    )
    return fig
