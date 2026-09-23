import numpy as np
import plotly.graph_objects as go

def build_color_strip(rgb01):
    strip = np.repeat(rgb01[np.newaxis, :, :], 24, axis=0)
    fig = go.Figure()
    fig.add_trace(go.Heatmap(z=np.zeros_like(strip), coloraxis="coloraxis"))
    fig.update_layout(
        coloraxis=dict(colorscale=[[i, f"rgb({int(c*255)},{int(d*255)},{int(e*255)})"] for i, (c, d, e) in enumerate(rgb01)]),
        height=60,
        margin=dict(l=0, r=0, t=0, b=0),
        xaxis=dict(showticklabels=False),
        yaxis=dict(showticklabels=False),
    )
    return fig

def build_rgb_plot(distance, rgb, config):
    fig = go.Figure()
    colors = config["plots"]["rgb_colors"]
    labels = ["Red", "Green", "Blue"]
    for i, (color, label) in enumerate(zip(colors, labels)):
        fig.add_trace(go.Scatter(x=distance, y=rgb[:, i], mode="lines", name=label, line=dict(color=color)))
    fig.update_layout(title="RGB Channels", xaxis_title="Distance", yaxis_title="Intensity")
    return fig

def build_hsv_plot(distance, hue, saturation, reference, config):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=distance, y=hue, mode="lines", name="Measured Hue", line=dict(color=config["plots"]["hue_color"])))
    fig.add_trace(go.Scatter(x=distance, y=reference["hue"], mode="lines", name="Reference Hue", line=dict(dash="dash")))
    fig.add_trace(go.Scatter(x=distance, y=saturation, mode="lines", name="Saturation", line=dict(color=config["plots"]["sat_color"])))
    fig.update_layout(title="Hue & Saturation", xaxis_title="Distance", yaxis_title="Value")
    return fig