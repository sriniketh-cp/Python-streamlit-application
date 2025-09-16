"""
Lab 9: Advanced Statistical Analysis Streamlit Application
Comprehensive CSV Data Analysis with NumPy and Modern UI
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from io import StringIO
import base64
from typing import Dict, List, Any, Optional, Tuple
import json
import time

# Import custom modules
from utils.stats import StatisticalAnalyzer, generate_sample_data, quick_stats, compare_groups
from utils.visualizations import DataVisualizer, quick_histogram, quick_scatter, quick_correlation_heatmap

# Page configuration
st.set_page_config(
    page_title="Lab 9: Statistical Analysis Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/your-repo/statistical-analysis',
        'Report a bug': 'https://github.com/your-repo/statistical-analysis/issues',
        'About': "Advanced Statistical Analysis Dashboard with NumPy and Modern UI"
    }
)

# Load custom CSS
def load_css():
    """Load custom CSS styling"""
    try:
        with open('/home/runner/work/Python-streamlit-application/Python-streamlit-application/styles/main.css') as f:
            css = f.read()
        st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("Custom CSS file not found. Using default styling.")

# Initialize the app
load_css()

# Custom HTML components
def create_header():
    """Create custom header with modern styling"""
    st.markdown("""
    <div class="custom-header fade-in">
        <h1>📊 Statistical Analysis Dashboard</h1>
        <p>Advanced CSV Data Analysis with NumPy • Lab 9</p>
    </div>
    """, unsafe_allow_html=True)

def create_metric_card(title: str, value: str, icon: str = "📈") -> str:
    """Create a metric card HTML"""
    return f"""
    <div class="stats-card slide-in-right">
        <h3>{icon} {title}</h3>
        <div class="metric-value">{value}</div>
    </div>
    """

def create_info_card(title: str, content: str, type: str = "info") -> str:
    """Create an info card with different types"""
    colors = {
        "info": "var(--primary-color)",
        "success": "var(--success-color)",
        "warning": "var(--warning-color)",
        "danger": "var(--danger-color)"
    }
    
    return f"""
    <div class="stats-card" style="border-left: 4px solid {colors.get(type, colors['info'])}">
        <h4 style="color: {colors.get(type, colors['info'])}; margin-bottom: 0.5rem;">{title}</h4>
        <p style="margin: 0; color: var(--text-secondary);">{content}</p>
    </div>
    """

# Session state initialization
def initialize_session_state():
    """Initialize session state variables"""
    if 'data' not in st.session_state:
        st.session_state.data = None
    if 'analyzer' not in st.session_state:
        st.session_state.analyzer = None
    if 'visualizer' not in st.session_state:
        st.session_state.visualizer = None
    if 'filtered_data' not in st.session_state:
        st.session_state.filtered_data = None
    if 'analysis_results' not in st.session_state:
        st.session_state.analysis_results = {}

initialize_session_state()

# Utility functions
def load_data(file_content: str, file_type: str = 'csv') -> pd.DataFrame:
    """Load data from uploaded file"""
    try:
        if file_type == 'csv':
            df = pd.read_csv(StringIO(file_content))
        else:
            raise ValueError("Unsupported file type")
        return df
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None

def download_data(data: pd.DataFrame, filename: str = "processed_data.csv") -> str:
    """Create download link for processed data"""
    csv = data.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">Download Processed Data</a>'
    return href

def create_sample_dataset() -> pd.DataFrame:
    """Create sample dataset for demonstration"""
    with st.spinner("Generating sample dataset..."):
        time.sleep(1)  # Simulate loading
        return generate_sample_data(n_samples=1000, n_features=6, random_state=42)

# Main application pages
def show_data_upload_page():
    """Data upload and preview page"""
    st.markdown("## 📁 Data Upload & Preview")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### Upload Your CSV File")
        uploaded_file = st.file_uploader(
            "Choose a CSV file",
            type=['csv'],
            help="Upload a CSV file with numerical data for analysis"
        )
        
        if uploaded_file is not None:
            try:
                # Read the uploaded file
                stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
                data = pd.read_csv(stringio)
                
                st.session_state.data = data
                st.session_state.analyzer = StatisticalAnalyzer(data)
                st.session_state.visualizer = DataVisualizer(data)
                
                st.success(f"✅ File uploaded successfully! Shape: {data.shape}")
                
            except Exception as e:
                st.error(f"Error reading file: {str(e)}")
                return
    
    with col2:
        st.markdown("### 🧪 Or Use Sample Data")
        if st.button("Generate Sample Dataset", type="primary", use_container_width=True):
            sample_data = create_sample_dataset()
            st.session_state.data = sample_data
            st.session_state.analyzer = StatisticalAnalyzer(sample_data)
            st.session_state.visualizer = DataVisualizer(sample_data)
            st.success("✅ Sample dataset generated!")
    
    # Data preview
    if st.session_state.data is not None:
        st.markdown("---")
        st.markdown("### 👀 Data Preview")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Rows", st.session_state.data.shape[0])
        with col2:
            st.metric("Columns", st.session_state.data.shape[1])
        with col3:
            numeric_cols = len(st.session_state.data.select_dtypes(include=[np.number]).columns)
            st.metric("Numeric Columns", numeric_cols)
        with col4:
            missing_values = st.session_state.data.isnull().sum().sum()
            st.metric("Missing Values", missing_values)
        
        # Data type information
        with st.expander("📋 Column Information", expanded=False):
            col_info = pd.DataFrame({
                'Column': st.session_state.data.columns,
                'Data Type': st.session_state.data.dtypes,
                'Non-Null Count': st.session_state.data.count(),
                'Null Count': st.session_state.data.isnull().sum(),
                'Unique Values': st.session_state.data.nunique()
            })
            st.dataframe(col_info, use_container_width=True)
        
        # Data preview table
        st.markdown("#### First 10 Rows")
        st.dataframe(st.session_state.data.head(10), use_container_width=True)

def show_statistical_analysis_page():
    """Statistical analysis page"""
    if st.session_state.data is None:
        st.warning("⚠️ Please upload data first from the Data Upload page.")
        return
    
    st.markdown("## 📊 Statistical Analysis")
    
    # Column selection
    numeric_columns = st.session_state.data.select_dtypes(include=[np.number]).columns.tolist()
    
    if not numeric_columns:
        st.error("❌ No numeric columns found in your data.")
        return
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### 🎯 Analysis Settings")
        
        selected_column = st.selectbox(
            "Select Column for Analysis",
            numeric_columns,
            help="Choose a numeric column for detailed statistical analysis"
        )
        
        analysis_type = st.multiselect(
            "Select Analysis Types",
            ["Basic Statistics", "Distribution Analysis", "Outlier Detection", "Correlation Analysis"],
            default=["Basic Statistics", "Distribution Analysis"],
            help="Choose which types of analysis to perform"
        )
    
    with col2:
        if selected_column:
            # Basic statistics
            if "Basic Statistics" in analysis_type:
                st.markdown("### 📈 Basic Statistics")
                
                stats = st.session_state.analyzer.get_summary_statistics(selected_column)
                
                # Create metrics in columns
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Mean", f"{stats['mean']:.3f}")
                    st.metric("Std Dev", f"{stats['std']:.3f}")
                with col2:
                    st.metric("Median", f"{stats['median']:.3f}")
                    st.metric("Variance", f"{stats['variance']:.3f}")
                with col3:
                    st.metric("Min", f"{stats['min']:.3f}")
                    st.metric("Max", f"{stats['max']:.3f}")
                with col4:
                    st.metric("Range", f"{stats['range']:.3f}")
                    st.metric("IQR", f"{stats['iqr']:.3f}")
                
                # Additional statistics
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Skewness", f"{stats['skewness']:.3f}")
                with col2:
                    st.metric("Kurtosis", f"{stats['kurtosis']:.3f}")
                with col3:
                    st.metric("Count", f"{stats['count']}")
            
            # Distribution analysis
            if "Distribution Analysis" in analysis_type:
                st.markdown("### 📊 Distribution Analysis")
                
                # Histogram
                fig_hist = st.session_state.visualizer.create_histogram(selected_column, bins=30)
                st.plotly_chart(fig_hist, use_container_width=True)
                
                # Percentiles
                st.markdown("#### Percentiles")
                percentiles = [10, 25, 50, 75, 90, 95, 99]
                perc_values = st.session_state.analyzer.calculate_percentiles(percentiles, selected_column)
                
                perc_df = pd.DataFrame({
                    'Percentile': [f"{p}th" for p in percentiles],
                    'Value': [f"{v:.3f}" for v in perc_values]
                })
                st.dataframe(perc_df, use_container_width=True)
            
            # Outlier detection
            if "Outlier Detection" in analysis_type:
                st.markdown("### 🎯 Outlier Detection")
                
                method = st.radio("Detection Method", ["IQR Method", "Z-Score Method"], horizontal=True)
                method_key = 'iqr' if method == "IQR Method" else 'zscore'
                
                outliers, normal_data = st.session_state.analyzer.get_outliers(selected_column, method=method_key)
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Normal Data Points", len(normal_data))
                with col2:
                    st.metric("Outliers Detected", len(outliers))
                
                if len(outliers) > 0:
                    # Box plot for outlier visualization
                    fig_box = st.session_state.visualizer.create_box_plot([selected_column])
                    st.plotly_chart(fig_box, use_container_width=True)
                    
                    # Show outlier values
                    with st.expander("View Outlier Values"):
                        outlier_df = pd.DataFrame({"Outlier Values": outliers})
                        st.dataframe(outlier_df, use_container_width=True)
            
            # Correlation analysis
            if "Correlation Analysis" in analysis_type and len(numeric_columns) > 1:
                st.markdown("### 🔗 Correlation Analysis")
                
                # Correlation heatmap
                fig_corr = st.session_state.visualizer.create_correlation_heatmap()
                st.plotly_chart(fig_corr, use_container_width=True)
                
                # Correlation with selected column
                corr_with_selected = st.session_state.data[numeric_columns].corr()[selected_column].abs().sort_values(ascending=False)
                
                st.markdown(f"#### Correlations with {selected_column}")
                corr_df = pd.DataFrame({
                    'Column': corr_with_selected.index,
                    'Correlation': [f"{v:.3f}" for v in corr_with_selected.values]
                })
                st.dataframe(corr_df, use_container_width=True)

def show_filtering_page():
    """Data filtering and boolean masking page"""
    if st.session_state.data is None:
        st.warning("⚠️ Please upload data first from the Data Upload page.")
        return
    
    st.markdown("## 🔍 Data Filtering & Boolean Masking")
    
    numeric_columns = st.session_state.data.select_dtypes(include=[np.number]).columns.tolist()
    
    if not numeric_columns:
        st.error("❌ No numeric columns found in your data.")
        return
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### ⚙️ Filter Settings")
        
        filter_column = st.selectbox("Select Column to Filter", numeric_columns)
        
        condition = st.selectbox(
            "Condition",
            [">", "<", ">=", "<=", "==", "!="],
            help="Choose the filtering condition"
        )
        
        # Get column statistics for better threshold selection
        col_stats = st.session_state.analyzer.get_summary_statistics(filter_column)
        
        threshold = st.number_input(
            "Threshold Value",
            value=float(col_stats['median']),
            help=f"Column range: {col_stats['min']:.3f} to {col_stats['max']:.3f}"
        )
        
        # Apply filter button
        if st.button("Apply Filter", type="primary", use_container_width=True):
            # Create mask and apply filter
            mask = st.session_state.analyzer.create_mask(filter_column, condition, threshold)
            filtered_data = st.session_state.data[mask]
            st.session_state.filtered_data = filtered_data
            
            st.success(f"✅ Filter applied! {len(filtered_data)} rows remaining out of {len(st.session_state.data)}")
        
        # Clear filter button
        if st.button("Clear Filter", use_container_width=True):
            st.session_state.filtered_data = None
            st.success("✅ Filter cleared!")
    
    with col2:
        st.markdown("### 📊 Filter Results")
        
        if st.session_state.filtered_data is not None:
            # Show comparison statistics
            st.markdown("#### Original vs Filtered Data Comparison")
            
            original_stats = st.session_state.analyzer.get_summary_statistics(filter_column)
            filtered_analyzer = StatisticalAnalyzer(st.session_state.filtered_data)
            filtered_stats = filtered_analyzer.get_summary_statistics(filter_column)
            
            # Comparison table
            comparison_df = pd.DataFrame({
                'Statistic': ['Count', 'Mean', 'Median', 'Std Dev', 'Min', 'Max'],
                'Original': [
                    original_stats['count'],
                    f"{original_stats['mean']:.3f}",
                    f"{original_stats['median']:.3f}",
                    f"{original_stats['std']:.3f}",
                    f"{original_stats['min']:.3f}",
                    f"{original_stats['max']:.3f}"
                ],
                'Filtered': [
                    filtered_stats['count'],
                    f"{filtered_stats['mean']:.3f}",
                    f"{filtered_stats['median']:.3f}",
                    f"{filtered_stats['std']:.3f}",
                    f"{filtered_stats['min']:.3f}",
                    f"{filtered_stats['max']:.3f}"
                ]
            })
            st.dataframe(comparison_df, use_container_width=True)
            
            # Distribution comparison visualization
            st.markdown("#### Distribution Comparison")
            filtered_visualizer = DataVisualizer(st.session_state.filtered_data)
            
            # Create comparison histogram
            fig_comparison = go.Figure()
            
            # Original data
            fig_comparison.add_trace(go.Histogram(
                x=st.session_state.data[filter_column].dropna(),
                name="Original Data",
                opacity=0.7,
                nbinsx=30
            ))
            
            # Filtered data
            fig_comparison.add_trace(go.Histogram(
                x=st.session_state.filtered_data[filter_column].dropna(),
                name="Filtered Data",
                opacity=0.7,
                nbinsx=30
            ))
            
            fig_comparison.update_layout(
                title=f"Distribution Comparison: {filter_column}",
                xaxis_title=filter_column,
                yaxis_title="Frequency",
                barmode='overlay',
                template="plotly_white",
                height=500
            )
            
            st.plotly_chart(fig_comparison, use_container_width=True)
            
            # Download filtered data
            st.markdown("#### 💾 Export Filtered Data")
            st.markdown(download_data(st.session_state.filtered_data, "filtered_data.csv"), unsafe_allow_html=True)
        
        else:
            st.info("👆 Configure and apply a filter to see results here.")
            
            # Show current filter preview
            if filter_column:
                st.markdown("#### 👀 Filter Preview")
                st.info(f"Filter: {filter_column} {condition} {threshold}")
                
                # Show how many rows would be affected
                temp_mask = st.session_state.analyzer.create_mask(filter_column, condition, threshold)
                temp_filtered = st.session_state.data[temp_mask]
                
                st.write(f"This filter would result in **{len(temp_filtered)}** rows out of **{len(st.session_state.data)}** total rows.")

def show_visualization_page():
    """Advanced data visualization page"""
    if st.session_state.data is None:
        st.warning("⚠️ Please upload data first from the Data Upload page.")
        return
    
    st.markdown("## 📈 Advanced Data Visualizations")
    
    numeric_columns = st.session_state.data.select_dtypes(include=[np.number]).columns.tolist()
    categorical_columns = st.session_state.data.select_dtypes(include=['object', 'category']).columns.tolist()
    
    if not numeric_columns:
        st.error("❌ No numeric columns found in your data.")
        return
    
    # Visualization type selection
    viz_type = st.selectbox(
        "Choose Visualization Type",
        ["Histogram", "Box Plot", "Scatter Plot", "Correlation Heatmap", "Bar Chart", 
         "Line Plot", "Violin Plot", "Statistical Summary", "Pair Plot"],
        help="Select the type of visualization to create"
    )
    
    if viz_type == "Histogram":
        col1, col2 = st.columns([1, 3])
        with col1:
            column = st.selectbox("Select Column", numeric_columns)
            bins = st.slider("Number of Bins", 10, 100, 30)
        with col2:
            if column:
                fig = st.session_state.visualizer.create_histogram(column, bins)
                st.plotly_chart(fig, use_container_width=True)
    
    elif viz_type == "Box Plot":
        col1, col2 = st.columns([1, 3])
        with col1:
            columns = st.multiselect("Select Columns", numeric_columns, default=numeric_columns[:3])
        with col2:
            if columns:
                fig = st.session_state.visualizer.create_box_plot(columns)
                st.plotly_chart(fig, use_container_width=True)
    
    elif viz_type == "Scatter Plot":
        col1, col2 = st.columns([1, 3])
        with col1:
            x_col = st.selectbox("X-axis", numeric_columns)
            y_col = st.selectbox("Y-axis", numeric_columns, index=1 if len(numeric_columns) > 1 else 0)
            color_col = st.selectbox("Color by (optional)", [None] + numeric_columns + categorical_columns)
            size_col = st.selectbox("Size by (optional)", [None] + numeric_columns)
        with col2:
            if x_col and y_col:
                fig = st.session_state.visualizer.create_scatter_plot(x_col, y_col, color_col, size_col)
                st.plotly_chart(fig, use_container_width=True)
    
    elif viz_type == "Correlation Heatmap":
        if len(numeric_columns) > 1:
            fig = st.session_state.visualizer.create_correlation_heatmap()
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Need at least 2 numeric columns for correlation analysis.")
    
    elif viz_type == "Bar Chart":
        if categorical_columns:
            col1, col2 = st.columns([1, 3])
            with col1:
                column = st.selectbox("Select Column", categorical_columns + numeric_columns)
                top_n = st.slider("Show Top N", 5, 50, 20)
            with col2:
                if column:
                    fig = st.session_state.visualizer.create_bar_chart(column, top_n=top_n)
                    st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No categorical columns available for bar chart.")
    
    elif viz_type == "Line Plot":
        col1, col2 = st.columns([1, 3])
        with col1:
            x_col = st.selectbox("X-axis", numeric_columns)
            y_col = st.selectbox("Y-axis", numeric_columns, index=1 if len(numeric_columns) > 1 else 0)
            group_col = st.selectbox("Group by (optional)", [None] + categorical_columns)
        with col2:
            if x_col and y_col:
                fig = st.session_state.visualizer.create_line_plot(x_col, y_col, group_col)
                st.plotly_chart(fig, use_container_width=True)
    
    elif viz_type == "Violin Plot":
        col1, col2 = st.columns([1, 3])
        with col1:
            columns = st.multiselect("Select Columns", numeric_columns, default=numeric_columns[:3])
        with col2:
            if columns:
                fig = st.session_state.visualizer.create_violin_plot(columns)
                st.plotly_chart(fig, use_container_width=True)
    
    elif viz_type == "Statistical Summary":
        col1, col2 = st.columns([1, 3])
        with col1:
            column = st.selectbox("Select Column", numeric_columns)
        with col2:
            if column:
                fig = st.session_state.visualizer.create_statistical_summary_plot(column)
                st.plotly_chart(fig, use_container_width=True)
    
    elif viz_type == "Pair Plot":
        st.markdown("### 🔗 Pair Plot Analysis")
        st.info("Note: Pair plots are computationally intensive. Limited to first 4 numeric columns and 1000 samples for performance.")
        
        if len(numeric_columns) >= 2:
            with st.spinner("Creating pair plot..."):
                fig = st.session_state.visualizer.create_pair_plot()
                if fig:
                    st.pyplot(fig, use_container_width=True)
        else:
            st.warning("Need at least 2 numeric columns for pair plot.")

def show_dashboard_page():
    """Main dashboard overview page"""
    if st.session_state.data is None:
        st.warning("⚠️ Please upload data first from the Data Upload page.")
        return
    
    st.markdown("## 🏠 Dashboard Overview")
    
    # Quick stats overview
    data = st.session_state.data
    numeric_columns = data.select_dtypes(include=[np.number]).columns.tolist()
    
    # Top metrics
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("Total Rows", f"{len(data):,}")
    with col2:
        st.metric("Total Columns", len(data.columns))
    with col3:
        st.metric("Numeric Columns", len(numeric_columns))
    with col4:
        missing_pct = (data.isnull().sum().sum() / (len(data) * len(data.columns))) * 100
        st.metric("Missing Data", f"{missing_pct:.1f}%")
    with col5:
        memory_usage = data.memory_usage(deep=True).sum() / 1024**2
        st.metric("Memory Usage", f"{memory_usage:.1f} MB")
    
    if numeric_columns:
        st.markdown("---")
        
        # Quick visualizations
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📊 Data Distribution")
            # First numeric column histogram
            first_col = numeric_columns[0]
            fig_hist = quick_histogram(data, first_col)
            st.plotly_chart(fig_hist, use_container_width=True)
        
        with col2:
            st.markdown("### 🔗 Correlation Overview")
            if len(numeric_columns) > 1:
                fig_corr = quick_correlation_heatmap(data)
                st.plotly_chart(fig_corr, use_container_width=True)
            else:
                st.info("Need at least 2 numeric columns for correlation analysis.")
        
        # Statistical summary table
        st.markdown("### 📈 Statistical Summary")
        
        summary_stats = []
        for col in numeric_columns[:10]:  # Limit to first 10 columns for display
            stats = st.session_state.analyzer.get_summary_statistics(col)
            summary_stats.append({
                'Column': col,
                'Count': stats['count'],
                'Mean': f"{stats['mean']:.3f}",
                'Std': f"{stats['std']:.3f}",
                'Min': f"{stats['min']:.3f}",
                'Max': f"{stats['max']:.3f}",
                'Skewness': f"{stats['skewness']:.3f}"
            })
        
        summary_df = pd.DataFrame(summary_stats)
        st.dataframe(summary_df, use_container_width=True)
        
        # Data quality indicators
        st.markdown("### 🎯 Data Quality Indicators")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Missing data by column
            missing_by_col = data.isnull().sum()
            missing_by_col = missing_by_col[missing_by_col > 0].sort_values(ascending=False)
            
            if len(missing_by_col) > 0:
                st.markdown("#### Missing Data by Column")
                fig_missing = px.bar(
                    x=missing_by_col.values,
                    y=missing_by_col.index,
                    orientation='h',
                    title="Missing Values Count",
                    labels={'x': 'Missing Count', 'y': 'Column'}
                )
                fig_missing.update_layout(height=300, template="plotly_white")
                st.plotly_chart(fig_missing, use_container_width=True)
            else:
                st.success("✅ No missing data found!")
        
        with col2:
            # Data types distribution
            dtype_counts = data.dtypes.value_counts()
            st.markdown("#### Data Types Distribution")
            fig_dtypes = px.pie(
                values=dtype_counts.values,
                names=dtype_counts.index,
                title="Column Data Types"
            )
            fig_dtypes.update_layout(height=300, template="plotly_white")
            st.plotly_chart(fig_dtypes, use_container_width=True)
        
        with col3:
            # Unique values distribution
            unique_counts = data.nunique().sort_values(ascending=False)[:10]
            st.markdown("#### Unique Values (Top 10)")
            fig_unique = px.bar(
                x=unique_counts.index,
                y=unique_counts.values,
                title="Unique Values Count",
                labels={'x': 'Column', 'y': 'Unique Count'}
            )
            fig_unique.update_layout(height=300, template="plotly_white", xaxis_tickangle=-45)
            st.plotly_chart(fig_unique, use_container_width=True)

# Sidebar navigation
def create_sidebar():
    """Create sidebar navigation"""
    st.sidebar.markdown("# 🧭 Navigation")
    
    pages = {
        "🏠 Dashboard": show_dashboard_page,
        "📁 Data Upload": show_data_upload_page,
        "📊 Statistical Analysis": show_statistical_analysis_page,
        "🔍 Data Filtering": show_filtering_page,
        "📈 Visualizations": show_visualization_page
    }
    
    selected_page = st.sidebar.selectbox("Choose Page", list(pages.keys()))
    
    # Add data info in sidebar
    if st.session_state.data is not None:
        st.sidebar.markdown("---")
        st.sidebar.markdown("### 📋 Data Info")
        st.sidebar.info(f"""
        **Rows:** {len(st.session_state.data):,}  
        **Columns:** {len(st.session_state.data.columns)}  
        **Numeric:** {len(st.session_state.data.select_dtypes(include=[np.number]).columns)}
        """)
        
        # Quick actions
        st.sidebar.markdown("### ⚡ Quick Actions")
        if st.sidebar.button("🔄 Refresh Analysis", use_container_width=True):
            st.session_state.analyzer = StatisticalAnalyzer(st.session_state.data)
            st.session_state.visualizer = DataVisualizer(st.session_state.data)
            st.success("✅ Analysis refreshed!")
        
        if st.sidebar.button("💾 Download Current Data", use_container_width=True):
            current_data = st.session_state.filtered_data if st.session_state.filtered_data is not None else st.session_state.data
            st.sidebar.markdown(download_data(current_data), unsafe_allow_html=True)
    
    # Footer
    st.sidebar.markdown("---")
    st.sidebar.markdown("""
    <div style='text-align: center; color: #666; font-size: 0.8rem;'>
        <p>📊 Lab 9: Statistical Analysis</p>
        <p>Built with Streamlit & NumPy</p>
        <p>© 2024</p>
    </div>
    """, unsafe_allow_html=True)
    
    return pages[selected_page]

# Main application
def main():
    """Main application function"""
    create_header()
    
    # Create sidebar and get selected page
    selected_page_func = create_sidebar()
    
    # Add some spacing
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Run selected page
    try:
        selected_page_func()
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.exception(e)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; margin-top: 2rem;'>
        <p>🚀 Advanced Statistical Analysis Dashboard | Powered by NumPy, Streamlit & Modern UI</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()