"""
Advanced Statistical Functions using NumPy
Lab 9 - Statistical Analysis Module
"""

import numpy as np
from typing import Union, Tuple, List, Dict, Any
import pandas as pd

class StatisticalAnalyzer:
    """
    A comprehensive statistical analysis class using NumPy for all computations.
    Implements advanced aggregation functions and boolean masking operations.
    """
    
    def __init__(self, data: Union[np.ndarray, pd.DataFrame]):
        """Initialize with data array or DataFrame"""
        if isinstance(data, pd.DataFrame):
            self.original_data = data
            self.numeric_data = data.select_dtypes(include=[np.number])
            self.array_data = self.numeric_data.values
        else:
            self.array_data = np.array(data)
            self.original_data = data
            self.numeric_data = None
    
    # Core Aggregation Functions
    def calculate_mean(self, column: str = None, axis: int = None) -> Union[float, np.ndarray]:
        """Calculate mean using NumPy"""
        if column and self.numeric_data is not None:
            return np.mean(self.numeric_data[column].values)
        return np.mean(self.array_data, axis=axis)
    
    def calculate_median(self, column: str = None, axis: int = None) -> Union[float, np.ndarray]:
        """Calculate median using NumPy"""
        if column and self.numeric_data is not None:
            return np.median(self.numeric_data[column].values)
        return np.median(self.array_data, axis=axis)
    
    def calculate_std(self, column: str = None, axis: int = None, ddof: int = 1) -> Union[float, np.ndarray]:
        """Calculate standard deviation using NumPy"""
        if column and self.numeric_data is not None:
            return np.std(self.numeric_data[column].values, ddof=ddof)
        return np.std(self.array_data, axis=axis, ddof=ddof)
    
    def calculate_variance(self, column: str = None, axis: int = None, ddof: int = 1) -> Union[float, np.ndarray]:
        """Calculate variance using NumPy"""
        if column and self.numeric_data is not None:
            return np.var(self.numeric_data[column].values, ddof=ddof)
        return np.var(self.array_data, axis=axis, ddof=ddof)
    
    def calculate_min(self, column: str = None, axis: int = None) -> Union[float, np.ndarray]:
        """Calculate minimum using NumPy"""
        if column and self.numeric_data is not None:
            return np.min(self.numeric_data[column].values)
        return np.min(self.array_data, axis=axis)
    
    def calculate_max(self, column: str = None, axis: int = None) -> Union[float, np.ndarray]:
        """Calculate maximum using NumPy"""
        if column and self.numeric_data is not None:
            return np.max(self.numeric_data[column].values)
        return np.max(self.array_data, axis=axis)
    
    def calculate_range(self, column: str = None, axis: int = None) -> Union[float, np.ndarray]:
        """Calculate range (max - min) using NumPy"""
        if column and self.numeric_data is not None:
            data = self.numeric_data[column].values
            return np.max(data) - np.min(data)
        return np.max(self.array_data, axis=axis) - np.min(self.array_data, axis=axis)
    
    def calculate_percentiles(self, percentiles: List[float], column: str = None, axis: int = None) -> np.ndarray:
        """Calculate percentiles using NumPy"""
        if column and self.numeric_data is not None:
            return np.percentile(self.numeric_data[column].values, percentiles)
        return np.percentile(self.array_data, percentiles, axis=axis)
    
    def calculate_skewness(self, column: str = None, axis: int = None) -> Union[float, np.ndarray]:
        """Calculate skewness using NumPy (Pearson's moment coefficient of skewness)"""
        if column and self.numeric_data is not None:
            data = self.numeric_data[column].values
        else:
            data = self.array_data
        
        # Remove NaN values
        data = data[~np.isnan(data)] if data.ndim == 1 else data
        
        mean = np.mean(data, axis=axis)
        std = np.std(data, axis=axis, ddof=1)
        
        # Avoid division by zero
        if np.any(std == 0):
            return np.nan
        
        # Calculate skewness: E[((X - μ) / σ)³]
        normalized = (data - mean) / std
        skewness = np.mean(normalized ** 3, axis=axis)
        
        return skewness
    
    def calculate_kurtosis(self, column: str = None, axis: int = None) -> Union[float, np.ndarray]:
        """Calculate kurtosis using NumPy"""
        if column and self.numeric_data is not None:
            data = self.numeric_data[column].values
        else:
            data = self.array_data
        
        # Remove NaN values
        data = data[~np.isnan(data)] if data.ndim == 1 else data
        
        mean = np.mean(data, axis=axis)
        std = np.std(data, axis=axis, ddof=1)
        
        # Avoid division by zero
        if np.any(std == 0):
            return np.nan
        
        # Calculate kurtosis: E[((X - μ) / σ)⁴] - 3 (excess kurtosis)
        normalized = (data - mean) / std
        kurtosis = np.mean(normalized ** 4, axis=axis) - 3
        
        return kurtosis
    
    # Boolean Masking and Filtering Functions
    def create_mask(self, column: str, condition: str, value: Union[float, int]) -> np.ndarray:
        """Create boolean mask based on condition"""
        if self.numeric_data is not None:
            data = self.numeric_data[column].values
        else:
            data = self.array_data
        
        conditions = {
            '>': data > value,
            '<': data < value,
            '>=': data >= value,
            '<=': data <= value,
            '==': data == value,
            '!=': data != value
        }
        
        return conditions.get(condition, np.ones(len(data), dtype=bool))
    
    def apply_mask(self, mask: np.ndarray, column: str = None) -> np.ndarray:
        """Apply boolean mask to filter data"""
        if column and self.numeric_data is not None:
            return self.numeric_data[column].values[mask]
        return self.array_data[mask]
    
    def filter_data(self, column: str, condition: str, value: Union[float, int]) -> Tuple[np.ndarray, np.ndarray]:
        """Filter data and return filtered and original arrays"""
        mask = self.create_mask(column, condition, value)
        filtered_data = self.apply_mask(mask, column)
        original_data = self.numeric_data[column].values if column and self.numeric_data is not None else self.array_data
        
        return filtered_data, original_data
    
    def get_outliers(self, column: str, method: str = 'iqr') -> Tuple[np.ndarray, np.ndarray]:
        """Detect outliers using IQR or Z-score method"""
        if self.numeric_data is not None:
            data = self.numeric_data[column].values
        else:
            data = self.array_data
        
        data = data[~np.isnan(data)]  # Remove NaN values
        
        if method == 'iqr':
            q1, q3 = np.percentile(data, [25, 75])
            iqr = q3 - q1
            lower_bound = q1 - 1.5 * iqr
            upper_bound = q3 + 1.5 * iqr
            outlier_mask = (data < lower_bound) | (data > upper_bound)
        
        elif method == 'zscore':
            z_scores = np.abs((data - np.mean(data)) / np.std(data))
            outlier_mask = z_scores > 3
        
        else:
            raise ValueError("Method must be 'iqr' or 'zscore'")
        
        outliers = data[outlier_mask]
        normal_data = data[~outlier_mask]
        
        return outliers, normal_data
    
    # Comprehensive Statistical Summary
    def get_summary_statistics(self, column: str = None) -> Dict[str, Any]:
        """Get comprehensive statistical summary"""
        if column and self.numeric_data is not None:
            data = self.numeric_data[column].values
            data = data[~np.isnan(data)]  # Remove NaN values
        else:
            data = self.array_data.flatten()
            data = data[~np.isnan(data)]  # Remove NaN values
        
        if len(data) == 0:
            return {"error": "No valid data points"}
        
        summary = {
            'count': len(data),
            'mean': np.mean(data),
            'median': np.median(data),
            'std': np.std(data, ddof=1),
            'variance': np.var(data, ddof=1),
            'min': np.min(data),
            'max': np.max(data),
            'range': np.max(data) - np.min(data),
            'q1': np.percentile(data, 25),
            'q3': np.percentile(data, 75),
            'iqr': np.percentile(data, 75) - np.percentile(data, 25),
            'skewness': self.calculate_skewness(column),
            'kurtosis': self.calculate_kurtosis(column)
        }
        
        return summary
    
    def correlation_matrix(self) -> np.ndarray:
        """Calculate correlation matrix using NumPy"""
        if self.numeric_data is not None:
            return np.corrcoef(self.numeric_data.values, rowvar=False)
        return np.corrcoef(self.array_data, rowvar=False)
    
    def get_column_names(self) -> List[str]:
        """Get numeric column names"""
        if self.numeric_data is not None:
            return list(self.numeric_data.columns)
        return [f"Column_{i}" for i in range(self.array_data.shape[1]) if self.array_data.ndim > 1]


def generate_sample_data(n_samples: int = 1000, n_features: int = 5, random_state: int = 42) -> pd.DataFrame:
    """Generate sample dataset for testing"""
    np.random.seed(random_state)
    
    data = {}
    
    # Generate different types of distributions
    data['normal_dist'] = np.random.normal(50, 15, n_samples)
    data['skewed_dist'] = np.random.exponential(2, n_samples)
    data['uniform_dist'] = np.random.uniform(0, 100, n_samples)
    data['bimodal_dist'] = np.concatenate([
        np.random.normal(30, 5, n_samples//2),
        np.random.normal(70, 5, n_samples//2)
    ])
    
    # Add some categorical-like data converted to numeric
    data['categories'] = np.random.choice([1, 2, 3, 4, 5], n_samples, p=[0.1, 0.2, 0.4, 0.2, 0.1])
    
    # Add additional features with correlations
    for i in range(n_features - 5):
        # Create correlated feature
        base_feature = data['normal_dist']
        noise = np.random.normal(0, 10, n_samples)
        correlation_strength = np.random.uniform(0.3, 0.8)
        data[f'feature_{i+1}'] = correlation_strength * base_feature + (1 - correlation_strength) * noise
    
    df = pd.DataFrame(data)
    
    # Add some missing values randomly
    mask = np.random.random(df.shape) < 0.02  # 2% missing values
    df = df.mask(mask)
    
    return df


# Utility functions for quick analysis
def quick_stats(data: Union[np.ndarray, pd.DataFrame, List], column: str = None) -> Dict[str, Any]:
    """Quick statistical analysis function"""
    analyzer = StatisticalAnalyzer(data)
    return analyzer.get_summary_statistics(column)


def compare_groups(data: pd.DataFrame, group_column: str, value_column: str) -> Dict[str, Dict[str, Any]]:
    """Compare statistics between different groups"""
    results = {}
    
    for group in data[group_column].unique():
        if pd.isna(group):
            continue
        group_data = data[data[group_column] == group][value_column].values
        group_data = group_data[~np.isnan(group_data)]
        
        if len(group_data) > 0:
            analyzer = StatisticalAnalyzer(group_data)
            results[str(group)] = analyzer.get_summary_statistics()
    
    return results