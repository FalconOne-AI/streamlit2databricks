# STREAMLIT APP - Financial Data Submission to Databricks
# File: streamlit_app.py

import streamlit as st
import pandas as pd
from databricks import sql
import uuid
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go

# ============================================================================
# PAGE CONFIG
# ============================================================================

st.set_page_config(
    page_title="Financial Data Submission Portal",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# DATABRICKS CONNECTION
# ============================================================================

@st.cache_resource
def get_databricks_connection():
    """Create cached Databricks connection"""
    try:
        connection = sql.connect(
            server_hostname=st.secrets["databricks"]["host"],
            http_path=st.secrets["databricks"]["http_path"],
            access_token=st.secrets["databricks"]["token"]
        )
        return connection
    except Exception as e:
        st.error(f"Connection failed: {e}")
        return None

# ============================================================================
# DATA OPERATIONS
# ============================================================================

def submit_financial_data(business_unit, revenue, expenses, submitted_by):
    """Submit financial data to Databricks"""
    connection = get_databricks_connection()
    if not connection:
        return False, "Connection failed"
    
    try:
        cursor = connection.cursor()
        
        submission_id = f"sub_{uuid.uuid4().hex[:8]}"
        profit_margin = ((revenue - expenses) / revenue * 100) if revenue > 0 else 0
        
        query = """
        INSERT INTO financial_submissions 
        (submission_id, business_unit, submission_date, revenue, expenses, 
         profit_margin, submitted_by, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        
        cursor.execute(query, (
            submission_id,
            business_unit,
            datetime.now(),
            float(revenue),
            float(expenses),
            float(profit_margin),
            submitted_by,
            datetime.now()
        ))
        
        cursor.close()
        return True, submission_id
        
    except Exception as e:
        return False, str(e)

@st.cache_data(ttl=30)
def fetch_all_data():
    """Fetch all financial data"""
    connection = get_databricks_connection()
    if not connection:
        return pd.DataFrame()
    
    try:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT * FROM financial_submissions 
            ORDER BY submission_date DESC 
            LIMIT 100
        """)
        
        columns = [desc[0] for desc in cursor.description]
        data = cursor.fetchall()
        
        df = pd.DataFrame(data, columns=columns)
        
        # Convert data types for Plotly compatibility
        if not df.empty:
            df['revenue'] = pd.to_numeric(df['revenue'], errors='coerce')
            df['expenses'] = pd.to_numeric(df['expenses'], errors='coerce')
            df['profit_margin'] = pd.to_numeric(df['profit_margin'], errors='coerce')
        
        cursor.close()
        
        return df
        
    except Exception as e:
        st.error(f"Fetch failed: {e}")
        return pd.DataFrame()

@st.cache_data(ttl=30)
def get_summary_stats():
    """Get summary statistics"""
    connection = get_databricks_connection()
    if not connection:
        return pd.DataFrame()
    
    try:
        cursor = connection.cursor()
        query = """
        SELECT 
            business_unit,
            COUNT(*) as submission_count,
            SUM(revenue) as total_revenue,
            SUM(expenses) as total_expenses,
            AVG(profit_margin) as avg_profit_margin
        FROM financial_submissions
        GROUP BY business_unit
        ORDER BY total_revenue DESC
        """
        
        cursor.execute(query)
        columns = [desc[0] for desc in cursor.description]
        data = cursor.fetchall()
        
        df = pd.DataFrame(data, columns=columns)
        
        # Convert data types for Plotly compatibility
        if not df.empty:
            df['submission_count'] = pd.to_numeric(df['submission_count'], errors='coerce')
            df['total_revenue'] = pd.to_numeric(df['total_revenue'], errors='coerce')
            df['total_expenses'] = pd.to_numeric(df['total_expenses'], errors='coerce')
            df['avg_profit_margin'] = pd.to_numeric(df['avg_profit_margin'], errors='coerce')
        
        cursor.close()
        
        return df
        
    except Exception as e:
        st.error(f"Summary fetch failed: {e}")
        return pd.DataFrame()

# ============================================================================
# UI COMPONENTS
# ============================================================================

def show_header():
    """Display header section"""
    st.title("💰 Financial Data Submission Portal")
    st.markdown("---")

def show_data_entry_form():
    """Display data entry form"""
    st.header("📝 Submit Financial Data")
    
    with st.form("financial_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            business_unit = st.selectbox(
                "Business Unit",
                ["Sales", "Marketing", "Operations", "Engineering", "Finance", "HR"]
            )
            
            revenue = st.number_input(
                "Revenue ($)",
                min_value=0.0,
                value=100000.0,
                step=1000.0,
                format="%.2f"
            )
        
        with col2:
            submitted_by = st.text_input(
                "Your Name",
                value="Demo User"
            )
            
            expenses = st.number_input(
                "Expenses ($)",
                min_value=0.0,
                value=75000.0,
                step=1000.0,
                format="%.2f"
            )
        
        # Calculate profit margin preview
        if revenue > 0:
            profit_margin = ((revenue - expenses) / revenue * 100)
            st.info(f"💡 Profit Margin Preview: {profit_margin:.2f}%")
        
        submitted = st.form_submit_button("Submit Data", use_container_width=True)
        
        if submitted:
            with st.spinner("Submitting data..."):
                success, result = submit_financial_data(
                    business_unit, revenue, expenses, submitted_by
                )
                
                if success:
                    st.success(f"✅ Data submitted successfully! ID: {result}")
                    st.balloons()
                    # Clear cache to show updated data
                    st.cache_data.clear()
                    st.rerun()
                else:
                    st.error(f"❌ Submission failed: {result}")

def show_kpi_metrics(df):
    """Display KPI metrics"""
    if df.empty:
        st.warning("No data available")
        return
    
    st.header("📊 Key Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_revenue = df['revenue'].sum()
        st.metric(
            "Total Revenue",
            f"${total_revenue:,.0f}",
            delta=None
        )
    
    with col2:
        total_expenses = df['expenses'].sum()
        st.metric(
            "Total Expenses",
            f"${total_expenses:,.0f}",
            delta=None
        )
    
    with col3:
        avg_margin = df['profit_margin'].mean()
        st.metric(
            "Avg Profit Margin",
            f"{avg_margin:.1f}%",
            delta=None
        )
    
    with col4:
        submission_count = len(df)
        st.metric(
            "Total Submissions",
            submission_count,
            delta=None
        )

def show_visualizations(df, summary_df):
    """Display data visualizations"""
    if df.empty or summary_df.empty:
        st.info("Submit data to see visualizations")
        return
    
    st.header("📈 Data Visualizations")
    
    tab1, tab2, tab3 = st.tabs(["Revenue Analysis", "Profit Margins", "Business Units"])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            # Revenue by Business Unit
            fig1 = px.bar(
                summary_df,
                x='business_unit',
                y='total_revenue',
                title='Total Revenue by Business Unit',
                labels={'total_revenue': 'Revenue ($)', 'business_unit': 'Business Unit'},
                color='total_revenue',
                color_continuous_scale='Blues'
            )
            fig1.update_layout(showlegend=False)
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            # Expenses vs Revenue Scatter
            fig2 = px.scatter(
                df,
                x='revenue',
                y='expenses',
                color='business_unit',
                title='Expenses vs Revenue',
                labels={'revenue': 'Revenue ($)', 'expenses': 'Expenses ($)'},
                size='profit_margin',
                hover_data=['business_unit', 'profit_margin']
            )
            st.plotly_chart(fig2, use_container_width=True)
    
    with tab2:
        col1, col2 = st.columns(2)
        
        with col1:
            # Profit Margin by Unit
            fig3 = px.bar(
                summary_df,
                x='avg_profit_margin',
                y='business_unit',
                orientation='h',
                title='Average Profit Margin by Business Unit',
                labels={'avg_profit_margin': 'Profit Margin (%)', 'business_unit': 'Business Unit'},
                color='avg_profit_margin',
                color_continuous_scale='Greens'
            )
            fig3.update_layout(showlegend=False)
            st.plotly_chart(fig3, use_container_width=True)
        
        with col2:
            # Profit Margin Distribution
            fig4 = px.box(
                df,
                x='business_unit',
                y='profit_margin',
                title='Profit Margin Distribution',
                labels={'profit_margin': 'Profit Margin (%)', 'business_unit': 'Business Unit'},
                color='business_unit'
            )
            fig4.update_layout(showlegend=False)
            st.plotly_chart(fig4, use_container_width=True)
    
    with tab3:
        col1, col2 = st.columns(2)
        
        with col1:
            # Submission Count Pie Chart
            fig5 = px.pie(
                summary_df,
                values='submission_count',
                names='business_unit',
                title='Submissions by Business Unit',
                hole=0.4
            )
            st.plotly_chart(fig5, use_container_width=True)
        
        with col2:
            # Summary Table
            st.subheader("Summary Statistics")
            display_df = summary_df.copy()
            display_df['total_revenue'] = display_df['total_revenue'].apply(lambda x: f"${x:,.2f}")
            display_df['total_expenses'] = display_df['total_expenses'].apply(lambda x: f"${x:,.2f}")
            display_df['avg_profit_margin'] = display_df['avg_profit_margin'].apply(lambda x: f"{x:.2f}%")
            st.dataframe(display_df, use_container_width=True, hide_index=True)

def show_recent_submissions(df):
    """Display recent submissions table"""
    if df.empty:
        return
    
    st.header("🕐 Recent Submissions")
    
    # Format dataframe for display
    display_df = df.head(10).copy()
    display_df['revenue'] = display_df['revenue'].apply(lambda x: f"${x:,.2f}")
    display_df['expenses'] = display_df['expenses'].apply(lambda x: f"${x:,.2f}")
    display_df['profit_margin'] = display_df['profit_margin'].apply(lambda x: f"{x:.2f}%")
    
    st.dataframe(
        display_df[['business_unit', 'revenue', 'expenses', 'profit_margin', 'submitted_by', 'submission_date']],
        use_container_width=True,
        hide_index=True
    )

# ============================================================================
# MAIN APP
# ============================================================================

def main():
    """Main application"""
    
    # Sidebar
    with st.sidebar:
        st.image("https://www.databricks.com/wp-content/uploads/2021/10/db-nav-logo.svg", width=200)
        st.markdown("---")
        st.subheader("About")
        st.write("This demo app showcases financial data submission to Databricks Delta tables with real-time analytics.")
        
        st.markdown("---")
        
        if st.button("🔄 Refresh Data", use_container_width=True):
            st.cache_data.clear()
            st.rerun()
        
        st.markdown("---")
        st.caption("Built with Streamlit + Databricks")
    
    # Main content
    show_header()
    
    # Data entry form
    show_data_entry_form()
    
    st.markdown("---")
    
    # Fetch data
    with st.spinner("Loading data..."):
        df = fetch_all_data()
        summary_df = get_summary_stats()
    
    # Display metrics and visualizations
    if not df.empty:
        show_kpi_metrics(df)
        st.markdown("---")
        show_visualizations(df, summary_df)
        st.markdown("---")
        show_recent_submissions(df)
    else:
        st.info("👋 Welcome! Submit your first financial data entry above to get started.")

if __name__ == "__main__":
    main()
