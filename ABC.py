import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Set page title
st.set_page_config(page_title="Data Forecasting Analyzer", layout="wide")
st.title("📊 Excel Data Analyzer & Forecasting Checker")
st.write("Upload an Excel file to analyze numerical columns, view histograms, and check if the data is ready for forecasting.")

# File uploader
uploaded_file = st.file_uploader("Choose an Excel file", type=["xlsx", "xls"])

if uploaded_file is not None:
    try:
        # Read Excel file
        df = pd.read_excel(uploaded_file)
        st.success("File uploaded successfully!")
        
        # Display raw data preview
        with st.expander("👀 View Raw Data Preview"):
            st.dataframe(df.head())

        # Filter for numerical columns
        numerical_cols = df.select_dtypes(include=['number']).columns.tolist()

        if not numerical_cols:
            st.warning("No numerical columns found in the uploaded Excel file.")
        else:
            st.subheader("📈 Statistical Analysis & Histograms")
            
            for col in numerical_cols:
                st.write(f"---")
                st.markdown(f"### Column: **{col}**")
                
                # Calculate metrics
                mean_val = df[col].mean()
                median_val = df[col].median()
                
                # Display metrics in columns
                col1, col2 = st.columns(2)
                col1.metric(label="Mean", value=f"{mean_val:.2f}")
                col2.metric(label="Median", value=f"{median_val:.2f}")
                
                # Check if mean and median are approximately close (within 5% relative difference)
                # Avoid division by zero if median is 0
                if median_val != 0:
                    percentage_diff = abs(mean_val - median_val) / abs(median_val)
                else:
                    percentage_diff = abs(mean_val - median_val)

                if percentage_diff <= 0.05: # 5% threshold
                    st.success("✅ The mean and median are close. **The data can be used for forecasting.**")
                else:
                    st.info("⚠️ The mean and median have a notable variance. This data might have skewness/outliers.")

                # Plot Histogram
                fig, ax = plt.subplots(figsize=(7, 3))
                ax.hist(df[col].dropna(), bins=20, color='skyblue', edgecolor='black', alpha=0.7)
                ax.axvline(mean_val, color='red', linestyle='dashed', linewidth=1.5, label=f'Mean: {mean_val:.2f}')
                ax.axvline(median_val, color='green', linestyle='dashed', linewidth=1.5, label=f'Median: {median_val:.2f}')
                ax.set_title(f'Histogram of {col}')
                ax.set_xlabel('Value')
                ax.set_ylabel('Frequency')
                ax.legend()
                
                st.pyplot(fig)
                
    except Exception as e:
        st.error(f"Error processing the file: {e}")
