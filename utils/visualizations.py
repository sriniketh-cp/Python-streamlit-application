"""
Advanced Data Visualization Module
Lab 9 - Comprehensive plotting functions using matplotlib, seaborn, and plotly
"""

import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
from plotly.subplots import make_subplots
import numpy as np
import pandas as pd
from typing import Union, List, Tuple, Dict, Any, Optional
import streamlit as st

# Set plotting style
plt.style.use('default')
sns.set_palette("husl")

class DataVisualizer:
    """
    Comprehensive data visualization class with multiple plotting libraries
    """
    
    def __init__(self, data: pd.DataFrame):
        """Initialize with DataFrame"""
        self.data = data
        self.numeric_columns = data.select_dtypes(include=[np.number]).columns.tolist()
        self.categorical_columns = data.select_dtypes(include=['object', 'category']).columns.tolist()
    
    def create_histogram(self, column: str, bins: int = 30, interactive: bool = True) -> Union[go.Figure, plt.Figure]:
        """Create histogram for distribution analysis"""
        if interactive:
            fig = px.histogram(
                self.data, 
                x=column, 
                nbins=bins,
                title=f'Distribution of {column}',
                marginal="box",  # Add box plot on top
                hover_data=[column]
            )
            fig.update_layout(
                showlegend=False,
                height=500,
                template="plotly_white"
            )
            return fig
        else:
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.hist(self.data[column].dropna(), bins=bins, alpha=0.7, edgecolor='black')
            ax.set_xlabel(column)
            ax.set_ylabel('Frequency')
            ax.set_title(f'Distribution of {column}')
            ax.grid(True, alpha=0.3)
            return fig
    
    def create_box_plot(self, columns: List[str], interactive: bool = True) -> Union[go.Figure, plt.Figure]:
        """Create box plot for outlier detection"""
        if interactive:
            fig = go.Figure()
            for col in columns:
                fig.add_trace(go.Box(
                    y=self.data[col].dropna(),
                    name=col,
                    boxpoints='outliers'
                ))
            
            fig.update_layout(
                title="Box Plot for Outlier Detection",
                yaxis_title="Values",
                template="plotly_white",
                height=500
            )
            return fig
        else:
            fig, ax = plt.subplots(figsize=(12, 6))
            data_to_plot = [self.data[col].dropna() for col in columns]
            ax.boxplot(data_to_plot, labels=columns)
            ax.set_title('Box Plot for Outlier Detection')
            ax.grid(True, alpha=0.3)
            plt.xticks(rotation=45)
            return fig
    
    def create_scatter_plot(self, x_col: str, y_col: str, color_col: str = None, 
                          size_col: str = None, interactive: bool = True) -> Union[go.Figure, plt.Figure]:
        """Create scatter plot for correlation analysis"""
        if interactive:
            fig = px.scatter(
                self.data,
                x=x_col,
                y=y_col,
                color=color_col,
                size=size_col,
                title=f'Scatter Plot: {x_col} vs {y_col}',
                hover_data=self.numeric_columns[:3],  # Show first 3 numeric columns on hover
                template="plotly_white"
            )
            
            # Add trendline
            if color_col is None:
                fig_trend = px.scatter(self.data, x=x_col, y=y_col, trendline="ols")
                fig.add_trace(fig_trend.data[1])  # Add trendline
            
            fig.update_layout(height=500)
            return fig
        else:
            fig, ax = plt.subplots(figsize=(10, 6))
            if color_col:
                scatter = ax.scatter(self.data[x_col], self.data[y_col], 
                                   c=self.data[color_col], alpha=0.6, cmap='viridis')
                plt.colorbar(scatter, ax=ax, label=color_col)
            else:
                ax.scatter(self.data[x_col], self.data[y_col], alpha=0.6)
            
            ax.set_xlabel(x_col)
            ax.set_ylabel(y_col)
            ax.set_title(f'Scatter Plot: {x_col} vs {y_col}')
            ax.grid(True, alpha=0.3)
            return fig
    
    def create_correlation_heatmap(self, interactive: bool = True) -> Union[go.Figure, plt.Figure]:
        """Create correlation heatmap"""
        corr_matrix = self.data[self.numeric_columns].corr()
        
        if interactive:
            fig = px.imshow(
                corr_matrix,
                title="Correlation Heatmap",
                color_continuous_scale="RdBu",
                aspect="auto",
                text_auto=True
            )
            fig.update_layout(height=600, template="plotly_white")
            return fig
        else:
            fig, ax = plt.subplots(figsize=(10, 8))
            sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0,
                       square=True, linewidths=0.5, ax=ax)
            ax.set_title('Correlation Heatmap')
            return fig
    
    def create_bar_chart(self, column: str, interactive: bool = True, top_n: int = 20) -> Union[go.Figure, plt.Figure]:
        """Create bar chart for categorical data"""
        value_counts = self.data[column].value_counts().head(top_n)
        
        if interactive:
            fig = px.bar(
                x=value_counts.index,
                y=value_counts.values,
                title=f'Bar Chart: {column} (Top {min(top_n, len(value_counts))})',
                labels={'x': column, 'y': 'Count'}
            )
            fig.update_layout(
                template="plotly_white",
                height=500,
                xaxis_tickangle=-45
            )
            return fig
        else:
            fig, ax = plt.subplots(figsize=(12, 6))
            value_counts.plot(kind='bar', ax=ax)
            ax.set_title(f'Bar Chart: {column}')
            ax.set_xlabel(column)
            ax.set_ylabel('Count')
            plt.xticks(rotation=45)
            ax.grid(True, alpha=0.3)
            return fig
    
    def create_line_plot(self, x_col: str, y_col: str, group_col: str = None, 
                        interactive: bool = True) -> Union[go.Figure, plt.Figure]:
        """Create line plot for trends"""
        if interactive:
            if group_col:
                fig = px.line(
                    self.data,
                    x=x_col,
                    y=y_col,
                    color=group_col,
                    title=f'Line Plot: {y_col} over {x_col}',
                    markers=True
                )
            else:
                # Sort by x_col for better line plot
                sorted_data = self.data.sort_values(x_col)
                fig = px.line(
                    sorted_data,
                    x=x_col,
                    y=y_col,
                    title=f'Line Plot: {y_col} over {x_col}',
                    markers=True
                )
            
            fig.update_layout(template="plotly_white", height=500)
            return fig
        else:
            fig, ax = plt.subplots(figsize=(12, 6))
            if group_col:
                for group in self.data[group_col].unique():
                    if pd.notna(group):
                        group_data = self.data[self.data[group_col] == group].sort_values(x_col)
                        ax.plot(group_data[x_col], group_data[y_col], 
                               marker='o', label=str(group), alpha=0.7)
                ax.legend()
            else:
                sorted_data = self.data.sort_values(x_col)
                ax.plot(sorted_data[x_col], sorted_data[y_col], marker='o', alpha=0.7)
            
            ax.set_xlabel(x_col)
            ax.set_ylabel(y_col)
            ax.set_title(f'Line Plot: {y_col} over {x_col}')
            ax.grid(True, alpha=0.3)
            return fig
    
    def create_violin_plot(self, columns: List[str], interactive: bool = True) -> Union[go.Figure, plt.Figure]:
        """Create violin plot for distribution comparison"""
        if interactive:
            fig = go.Figure()
            for col in columns:
                fig.add_trace(go.Violin(
                    y=self.data[col].dropna(),
                    name=col,
                    box_visible=True,
                    meanline_visible=True
                ))
            
            fig.update_layout(
                title="Violin Plot - Distribution Comparison",
                yaxis_title="Values",
                template="plotly_white",
                height=500
            )
            return fig
        else:
            fig, ax = plt.subplots(figsize=(12, 6))
            data_to_plot = [self.data[col].dropna() for col in columns]
            parts = ax.violinplot(data_to_plot, positions=range(len(columns)), showmeans=True)
            ax.set_xticks(range(len(columns)))
            ax.set_xticklabels(columns, rotation=45)
            ax.set_title('Violin Plot - Distribution Comparison')
            ax.grid(True, alpha=0.3)
            return fig
    
    def create_pair_plot(self, columns: List[str] = None, sample_size: int = 1000) -> plt.Figure:
        """Create pair plot for multiple variable relationships"""
        if columns is None:
            columns = self.numeric_columns[:4]  # Limit to first 4 columns for performance
        
        # Sample data if too large
        data_sample = self.data[columns]
        if len(data_sample) > sample_size:
            data_sample = data_sample.sample(n=sample_size, random_state=42)
        
        # Remove any remaining non-numeric columns
        data_sample = data_sample.select_dtypes(include=[np.number])
        
        if data_sample.shape[1] < 2:
            st.warning("Need at least 2 numeric columns for pair plot")
            return None
        
        fig = plt.figure(figsize=(12, 10))
        
        # Use seaborn for pair plot
        sns.pairplot(data_sample, diag_kind='hist', plot_kws={'alpha': 0.6})
        plt.suptitle('Pair Plot - Variable Relationships', y=1.02)
        
        return fig
    
    def create_distribution_comparison(self, column: str, filter_col: str = None, 
                                     filter_values: List = None, interactive: bool = True) -> Union[go.Figure, plt.Figure]:
        """Compare distributions with and without filters"""
        if interactive:
            fig = go.Figure()
            
            # Original distribution
            fig.add_trace(go.Histogram(
                x=self.data[column].dropna(),
                name="Original Data",
                opacity=0.7,
                nbinsx=30
            ))
            
            # Filtered distribution
            if filter_col and filter_values:
                filtered_data = self.data[self.data[filter_col].isin(filter_values)][column].dropna()
                fig.add_trace(go.Histogram(
                    x=filtered_data,
                    name="Filtered Data",
                    opacity=0.7,
                    nbinsx=30
                ))
            
            fig.update_layout(
                title=f"Distribution Comparison: {column}",
                xaxis_title=column,
                yaxis_title="Frequency",
                barmode='overlay',
                template="plotly_white",
                height=500
            )
            return fig
        else:
            fig, ax = plt.subplots(figsize=(12, 6))
            
            # Original distribution
            ax.hist(self.data[column].dropna(), bins=30, alpha=0.7, 
                   label='Original Data', edgecolor='black')
            
            # Filtered distribution
            if filter_col and filter_values:
                filtered_data = self.data[self.data[filter_col].isin(filter_values)][column].dropna()
                ax.hist(filtered_data, bins=30, alpha=0.7, 
                       label='Filtered Data', edgecolor='black')
            
            ax.set_xlabel(column)
            ax.set_ylabel('Frequency')
            ax.set_title(f'Distribution Comparison: {column}')
            ax.legend()
            ax.grid(True, alpha=0.3)
            return fig
    
    def create_statistical_summary_plot(self, column: str, interactive: bool = True) -> Union[go.Figure, plt.Figure]:
        """Create comprehensive statistical summary visualization"""
        data_clean = self.data[column].dropna()
        
        if interactive:
            # Create subplots
            fig = make_subplots(
                rows=2, cols=2,
                subplot_titles=('Histogram', 'Box Plot', 'Q-Q Plot', 'Statistics'),
                specs=[[{"secondary_y": False}, {"secondary_y": False}],
                       [{"secondary_y": False}, {"type": "table"}]]
            )
            
            # Histogram
            fig.add_trace(
                go.Histogram(x=data_clean, nbinsx=30, name="Distribution"),
                row=1, col=1
            )
            
            # Box plot
            fig.add_trace(
                go.Box(y=data_clean, name="Box Plot", boxpoints='outliers'),
                row=1, col=2
            )
            
            # Q-Q plot (approximate)
            from scipy import stats
            theoretical_quantiles = stats.norm.ppf(np.linspace(0.01, 0.99, len(data_clean)))
            sample_quantiles = np.sort(data_clean)
            
            fig.add_trace(
                go.Scatter(
                    x=theoretical_quantiles,
                    y=sample_quantiles,
                    mode='markers',
                    name="Q-Q Plot"
                ),
                row=2, col=1
            )
            
            # Statistics table
            stats_data = {
                'Statistic': ['Mean', 'Median', 'Std Dev', 'Min', 'Max', 'Skewness'],
                'Value': [
                    f"{np.mean(data_clean):.3f}",
                    f"{np.median(data_clean):.3f}",
                    f"{np.std(data_clean):.3f}",
                    f"{np.min(data_clean):.3f}",
                    f"{np.max(data_clean):.3f}",
                    f"{stats.skew(data_clean):.3f}"
                ]
            }
            
            fig.add_trace(
                go.Table(
                    header=dict(values=list(stats_data.keys())),
                    cells=dict(values=list(stats_data.values()))
                ),
                row=2, col=2
            )
            
            fig.update_layout(
                title=f"Statistical Summary: {column}",
                height=800,
                template="plotly_white"
            )
            return fig
        else:
            fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
            
            # Histogram
            ax1.hist(data_clean, bins=30, alpha=0.7, edgecolor='black')
            ax1.set_title('Distribution')
            ax1.set_xlabel(column)
            ax1.grid(True, alpha=0.3)
            
            # Box plot
            ax2.boxplot(data_clean)
            ax2.set_title('Box Plot')
            ax2.set_ylabel(column)
            ax2.grid(True, alpha=0.3)
            
            # Q-Q plot
            from scipy import stats
            stats.probplot(data_clean, dist="norm", plot=ax3)
            ax3.set_title('Q-Q Plot')
            ax3.grid(True, alpha=0.3)
            
            # Statistics text
            ax4.axis('off')
            stats_text = f"""
            Statistics for {column}:
            
            Mean: {np.mean(data_clean):.3f}
            Median: {np.median(data_clean):.3f}
            Std Dev: {np.std(data_clean):.3f}
            Min: {np.min(data_clean):.3f}
            Max: {np.max(data_clean):.3f}
            Skewness: {stats.skew(data_clean):.3f}
            Kurtosis: {stats.kurtosis(data_clean):.3f}
            """
            ax4.text(0.1, 0.5, stats_text, fontsize=12, verticalalignment='center',
                    bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgray"))
            
            plt.tight_layout()
            return fig


# Utility functions for quick plotting
def quick_histogram(data: pd.DataFrame, column: str, bins: int = 30) -> go.Figure:
    """Quick histogram function"""
    visualizer = DataVisualizer(data)
    return visualizer.create_histogram(column, bins, interactive=True)


def quick_scatter(data: pd.DataFrame, x_col: str, y_col: str, color_col: str = None) -> go.Figure:
    """Quick scatter plot function"""
    visualizer = DataVisualizer(data)
    return visualizer.create_scatter_plot(x_col, y_col, color_col, interactive=True)


def quick_correlation_heatmap(data: pd.DataFrame) -> go.Figure:
    """Quick correlation heatmap function"""
    visualizer = DataVisualizer(data)
    return visualizer.create_correlation_heatmap(interactive=True)


# Custom color palettes for consistent theming
CUSTOM_COLORS = {
    'primary': '#1f77b4',
    'secondary': '#ff7f0e',
    'success': '#2ca02c',
    'danger': '#d62728',
    'warning': '#ff7f0e',
    'info': '#17a2b8',
    'light': '#f8f9fa',
    'dark': '#343a40'
}

PLOTLY_THEME = {
    'layout': {
        'font': {'family': 'Arial, sans-serif', 'size': 12},
        'colorway': ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', 
                     '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf'],
        'plot_bgcolor': 'white',
        'paper_bgcolor': 'white'
    }
}