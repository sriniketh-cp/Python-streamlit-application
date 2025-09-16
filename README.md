# 📊 Lab 9: Advanced Statistical Analysis Dashboard

A comprehensive Python Streamlit application for advanced statistical analysis on CSV datasets using NumPy, featuring modern UI design with Tailwind CSS integration.

![Dashboard Screenshot](https://via.placeholder.com/800x400/1f77b4/ffffff?text=Statistical+Analysis+Dashboard)

## 🚀 Features

### Core Statistical Functions
- **Advanced Aggregation Functions** using NumPy:
  - Mean, Median, Standard Deviation
  - Variance, Min/Max, Range
  - Percentiles (10th, 25th, 50th, 75th, 90th, 95th, 99th)
  - Skewness and Kurtosis calculations
  - Inter-quartile Range (IQR)

### Boolean Masking & Data Filtering
- **Dynamic Data Filtering** with NumPy boolean indexing
- **Conditional Masks** for advanced data analysis
- **Interactive Filter Controls**:
  - Greater than (>), Less than (<)
  - Greater/Equal (>=), Less/Equal (<=)
  - Equal (==), Not Equal (!=)
- **Real-time Statistics Comparison** between filtered and original data

### Comprehensive Data Visualizations
- **Interactive Charts** using Plotly, Matplotlib, and Seaborn:
  - 📊 **Histograms** for distribution analysis
  - 📦 **Box Plots** for outlier detection
  - 🔍 **Scatter Plots** for correlation analysis
  - 🎯 **Correlation Heatmaps**
  - 📈 **Bar Charts** for categorical data
  - 📉 **Line Plots** for trend analysis
  - 🎻 **Violin Plots** for distribution comparison
  - 🔗 **Pair Plots** for multi-variable relationships

### Modern UI & User Experience
- **Professional Design** with Tailwind CSS integration
- **Responsive Layout** that works on all devices
- **Interactive Dashboard** with real-time updates
- **Smooth Animations** and transitions
- **Custom Color Schemes** and typography
- **Card-based Layout** for organized information display

### Technical Features
- **CSV File Upload** functionality
- **Sample Dataset Generator** for testing
- **Dynamic Column Selection** for analysis
- **Real-time Statistics Calculation**
- **Export Functionality** for processed data
- **Comprehensive Error Handling**
- **Progress Indicators** for long operations
- **Memory Usage Optimization**

## 📁 Project Structure

```
Python-streamlit-application/
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── utils/
│   ├── stats.py               # NumPy statistical functions
│   └── visualizations.py     # Plotting functions
├── styles/
│   └── main.css              # Custom CSS with Tailwind integration
└── README.md                 # Documentation
```

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation Steps

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/Python-streamlit-application.git
   cd Python-streamlit-application
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   streamlit run app.py
   ```

4. **Access the dashboard:**
   Open your browser and navigate to `http://localhost:8501`

## 📊 Usage Guide

### 1. Data Upload
- **Upload CSV File**: Use the file uploader to load your dataset
- **Generate Sample Data**: Click "Generate Sample Dataset" for testing
- **Data Preview**: View data shape, types, and first 10 rows

### 2. Statistical Analysis
- **Select Column**: Choose any numeric column for analysis
- **Choose Analysis Type**: Select from:
  - Basic Statistics (mean, median, std, etc.)
  - Distribution Analysis (histograms, percentiles)
  - Outlier Detection (IQR or Z-score methods)
  - Correlation Analysis (heatmaps, correlation values)

### 3. Data Filtering & Boolean Masking
- **Configure Filters**: Select column, condition, and threshold
- **Apply Masks**: Use NumPy boolean indexing to filter data
- **Compare Results**: View statistics for original vs filtered data
- **Export Filtered Data**: Download processed datasets

### 4. Advanced Visualizations
- **Interactive Charts**: Create various plot types
- **Customization Options**: Adjust colors, sizes, and groupings
- **Export Plots**: Save visualizations as images

### 5. Dashboard Overview
- **Quick Metrics**: View key dataset statistics
- **Data Quality**: Check for missing values and data types  
- **Memory Usage**: Monitor application performance

## 🧮 Statistical Functions

### Basic Statistics (using NumPy)
```python
# Mean calculation
mean = np.mean(data)

# Standard deviation
std = np.std(data, ddof=1)

# Percentiles
percentiles = np.percentile(data, [25, 50, 75])

# Skewness calculation
skewness = np.mean(((data - mean) / std) ** 3)
```

### Boolean Masking Examples
```python
# Create boolean mask
mask = data > threshold

# Apply mask to filter data
filtered_data = data[mask]

# Conditional filtering
condition_mask = (data > lower_bound) & (data < upper_bound)
```

### Outlier Detection
```python
# IQR method
q1, q3 = np.percentile(data, [25, 75])
iqr = q3 - q1
outliers = data[(data < q1 - 1.5*iqr) | (data > q3 + 1.5*iqr)]

# Z-score method
z_scores = np.abs((data - np.mean(data)) / np.std(data))
outliers = data[z_scores > 3]
```

## 🎨 UI Components

### Modern Design Elements
- **Gradient Backgrounds**: Eye-catching header with gradient colors
- **Card Layout**: Organized information in modern cards
- **Interactive Metrics**: Hover effects and animations
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Custom Color Palette**: Professional color scheme
- **Typography**: Inter font for modern look

### Tailwind CSS Integration
- **Utility Classes**: Rapid UI development
- **Responsive Grid**: Flexible layouts
- **Shadow Effects**: Depth and visual hierarchy
- **Animations**: Smooth transitions and hover effects

## 📈 Performance Optimizations

- **Data Sampling**: Large datasets automatically sampled for performance
- **Lazy Loading**: Visualizations created on-demand
- **Memory Management**: Efficient data structures using NumPy
- **Caching**: Streamlit caching for improved responsiveness
- **Error Handling**: Graceful degradation for edge cases

## 🧪 Testing Features

### Sample Data Generator
The application includes a built-in sample dataset generator that creates:
- **Normal Distribution** data (μ=50, σ=15)
- **Skewed Distribution** data (exponential)
- **Uniform Distribution** data (0-100)
- **Bimodal Distribution** data (two peaks)
- **Categorical Data** (1-5 scale)
- **Correlated Features** for relationship testing

### Test Cases
- Large datasets (1000+ rows)
- Missing value handling
- Different data types
- Edge cases and error conditions

## 🔧 Configuration

### Custom Styling
Modify `styles/main.css` to customize:
- Color schemes
- Typography
- Layout spacing
- Animation speeds
- Component styling

### Application Settings
Update `app.py` configuration:
- Page title and icon
- Layout settings
- Default values
- Feature toggles

## 📊 Data Requirements

### Supported File Formats
- **CSV files** (.csv)
- **UTF-8 encoding** recommended
- **Header row** required

### Data Constraints
- **Numeric Columns**: Required for statistical analysis
- **File Size**: Recommended under 50MB for optimal performance
- **Missing Values**: Handled automatically
- **Data Types**: Automatic detection and conversion

## 🚨 Error Handling

The application includes comprehensive error handling for:
- **File Upload Errors**: Invalid formats, encoding issues
- **Data Processing Errors**: Missing columns, type conversion
- **Statistical Calculation Errors**: Division by zero, empty datasets
- **Visualization Errors**: Invalid column selections, rendering issues
- **Memory Errors**: Large dataset handling

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and test thoroughly
4. Commit your changes: `git commit -am 'Add feature'`
5. Push to the branch: `git push origin feature-name`
6. Create a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **NumPy** for powerful numerical computing
- **Streamlit** for the amazing web app framework
- **Plotly** for interactive visualizations
- **Tailwind CSS** for modern styling utilities
- **Matplotlib & Seaborn** for additional plotting capabilities

## 📞 Support

If you encounter any issues or have questions:
1. Check the [Issues](https://github.com/your-username/Python-streamlit-application/issues) page
2. Create a new issue with detailed description
3. Include error messages and screenshots if applicable

---

**Built with ❤️ using Python, NumPy, Streamlit, and Modern Web Technologies**