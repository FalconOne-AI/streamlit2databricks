# Financial Data Submission Portal

A demo application showcasing real-time financial data submission and analytics using Streamlit and Databricks.

## 🎯 Overview

This application demonstrates a multi-user financial data submission system where different business units can submit revenue and expense data, which is stored in Databricks Delta tables and visualized in real-time.

## ✨ Features

- **Multi-User Data Entry**: Business units can submit financial metrics through an intuitive form
- **Real-Time Analytics**: Instant visualization updates after data submission
- **Delta Lake Storage**: Reliable, ACID-compliant data storage in Databricks
- **Interactive Dashboards**: Plotly-powered charts for revenue, expenses, and profit margins
- **KPI Metrics**: At-a-glance key performance indicators
- **Recent Submissions**: Track the latest data entries

## 🏗️ Architecture

```
Streamlit UI → Databricks SQL Connector → Delta Table → Real-time Visualizations
```

- **Frontend**: Streamlit (Python web framework)
- **Backend**: Databricks SQL Warehouse
- **Storage**: Delta Lake tables
- **Visualization**: Plotly charts
- **Deployment**: Streamlit Cloud

## 📋 Prerequisites

- Databricks account (Free tier or above)
- GitHub account
- Streamlit Cloud account (free)

## 🚀 Quick Start

### 1. Set Up Databricks

Create a Delta table in your Databricks workspace:

```sql
CREATE TABLE IF NOT EXISTS financial_submissions (
  submission_id STRING,
  business_unit STRING,
  submission_date TIMESTAMP,
  revenue DECIMAL(15,2),
  expenses DECIMAL(15,2),
  profit_margin DECIMAL(5,2),
  submitted_by STRING,
  created_at TIMESTAMP
) USING DELTA;
```

### 2. Get Databricks Credentials

You'll need:
- **Workspace URL**: `your-workspace.cloud.databricks.com`
- **HTTP Path**: Found in SQL Warehouses → Connection Details
- **Access Token**: User Settings → Developer → Access Tokens

### 3. Clone This Repository

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

### 4. Install Dependencies (Local Testing)

```bash
pip install -r requirements.txt
```

### 5. Configure Secrets (Local Testing)

Create `.streamlit/secrets.toml`:

```toml
[databricks]
host = "your-workspace.cloud.databricks.com"
http_path = "/sql/1.0/warehouses/xxxxx"
token = "your-access-token"
```

**⚠️ IMPORTANT**: Never commit this file to Git! It's already in `.gitignore`.

### 6. Run Locally

```bash
streamlit run streamlit_app.py
```

### 7. Deploy to Streamlit Cloud

1. Push your code to GitHub (without secrets)
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Create new app from your repository
4. Add secrets in Advanced Settings → Secrets
5. Deploy!

## 📁 Project Structure

```
├── streamlit_app.py       # Main application
├── requirements.txt       # Python dependencies
├── .gitignore            # Git ignore rules
├── README.md             # This file
└── .streamlit/
    └── secrets.toml      # Local secrets (not committed)
```

## 🔒 Security Notes

- Secrets are managed through Streamlit Cloud's encrypted secrets management
- Never commit credentials to Git
- Use Databricks access tokens with appropriate permissions
- Consider setting token expiration for production use

## 📊 Data Schema

| Column | Type | Description |
|--------|------|-------------|
| submission_id | STRING | Unique identifier for each submission |
| business_unit | STRING | Business unit name (Sales, Marketing, etc.) |
| submission_date | TIMESTAMP | When the data was submitted |
| revenue | DECIMAL(15,2) | Revenue amount in dollars |
| expenses | DECIMAL(15,2) | Expenses amount in dollars |
| profit_margin | DECIMAL(5,2) | Calculated profit margin percentage |
| submitted_by | STRING | Name of the person submitting |
| created_at | TIMESTAMP | Record creation timestamp |

## 🎨 Visualizations

The app includes:
- **Revenue Analysis**: Bar charts showing total revenue by business unit
- **Expense Correlation**: Scatter plot comparing expenses vs revenue
- **Profit Margins**: Horizontal bar chart of average margins
- **Distribution Analysis**: Box plots showing profit margin spread
- **Submission Overview**: Pie chart of submissions by unit

## 🧪 Testing in Google Colab

A Colab notebook is available for testing Databricks connectivity before deployment:

1. Open Google Colab
2. Add Databricks credentials to Colab Secrets
3. Run the prototype notebook to verify connection
4. Test data submission and retrieval functions

## 🐛 Troubleshooting

### Connection Issues
- Verify SQL Warehouse is running in Databricks
- Check HTTP path format: `/sql/1.0/warehouses/xxxxx`
- Ensure access token hasn't expired
- Remove `https://` from hostname

### Data Not Showing
- Click the "Refresh Data" button in the sidebar
- Verify table name matches exactly
- Check Databricks query history for errors

### Slow Performance
- Databricks free tier may have cold starts
- Keep SQL Warehouse running during demo
- Cache settings are optimized (30-second TTL)

## 🔄 Development Workflow

1. **Prototype** in Google Colab to test Databricks operations
2. **Develop** features in the Streamlit app locally
3. **Test** thoroughly with sample data
4. **Deploy** to Streamlit Cloud
5. **Iterate** based on feedback

## 📈 Future Enhancements

- [ ] User authentication and authorization
- [ ] Data export functionality (CSV/Excel)
- [ ] Date range filtering for historical analysis
- [ ] Email notifications for submissions
- [ ] Comparison views (MoM, YoY)
- [ ] Data validation and business rules
- [ ] Audit logging
- [ ] Multi-currency support

## 🤝 Contributing

This is a demo project for client presentation. For modifications:

1. Create a feature branch
2. Test thoroughly locally
3. Update documentation
4. Submit for review

## 📝 License

This is a proprietary demo/proof-of-concept project. All rights reserved.

For licensing inquiries or to discuss implementation for your organization, please contact the project owner.

## 📞 Support

For questions or issues:
- Check Troubleshooting section above
- Review Databricks documentation
- Check Streamlit documentation

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io)
- Powered by [Databricks](https://databricks.com)
- Visualizations using [Plotly](https://plotly.com)

---

**Demo Version** | Built for Client Presentation | Copyright © 2025 The Select Group. All Rights Reserved. | Last Updated: December 2025
