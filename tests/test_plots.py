import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
from src.ui.plots import plot_color_profiles
from src.domain.models import AnalysisResult, ColorProfile
import numpy as np
import streamlit as st

def test_plot_creation():
    """Test that plot function creates a figure without crashing."""
    # Mock data
    positions = np.linspace(0, 1, 50)
    measured_rgb = np.random.rand(50, 3)
    measured_hsv = np.random.rand(50, 3)
    ref_rgb = np.random.rand(50, 3)
    ref_hsv = np.random.rand(50, 3)
    
    measured = ColorProfile(positions=positions, rgb=measured_rgb, hsv=measured_hsv)
    reference = ColorProfile(positions=positions, rgb=ref_rgb, hsv=ref_hsv)
    
    result = AnalysisResult(
        measured=measured,
        reference=reference,
        score=0.85,
        error_metric=0.05
    )
    
    # Mock st.pyplot to avoid actual Streamlit context issues in unit test
    original_pyplot = st.pyplot
    st.pyplot = lambda fig: None
    
    try:
        plot_color_profiles(result)
        # If we get here without exception, the plotting logic worked
        assert True
    finally:
        st.pyplot = original_pyplot
        plt.close('all')