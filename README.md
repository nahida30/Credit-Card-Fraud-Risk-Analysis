https://credit-card-fraud-risk-analysis-bina.streamlit.app/

🎯 Project Overview
In commercial financial sectors, standard business intelligence tools are highly effective for aggregating historical data but lack the native architecture to predict behavioral patterns dynamically. This repository bridges that gap.

By analyzing a transaction dataset containing attributes like transaction amount (INR), transaction vertical categories, demographic location mapping, and user fraud history metadata, this project delivers:

Historical Reporting: Precise, cross-filtering tracking of systemic risks, seasonal fraud vectors, and monetary exposure.

Predictive Intelligence: An embedded Random Forest Classifier trained on transaction telemetry to output immediate risk probabilities for incoming real-time payment vectors.

📊 Core Feature Architecture
1. The Interactive Dashboard Layer (Power BI Replicated)
Using Streamlit and Plotly Dark Engines, the UI seamlessly captures the original Power BI corporate dark aesthetic:

Dynamic Filter Panel: Interactive sidebar enabling multidimensional data sub-setting across Fraud Classification Types, State Demographics, and Target Merchant Entities.

Executive Metrics Matrix: Real-time calculated KPI indicator cards displaying baseline criticalities: Fraud Rate %, Fraudulent Case Volumes, Critical Risk Ratios, and Top Active Fraud Types.

Categorized Volume Charting: A horizontal stacked bar chart analyzing monetary distributions by fraud type overlaid against transaction verticals (E-commerce, Groceries, Transportation, etc.).

Risk Density Donut Graph: An isolated pie chart visualizing exact transaction exposures mapped to specific categorical risk bands (Low, Medium, High, Critical).

Spatio-Temporal Trends: Parallel bar-and-line visualizations charting total fraudulent counts partitioned by geographic state boundaries and true month-by-month calendar chronology.

2. The AI/ML Pipeline Engine
Moving beyond historical visual aggregations, the Python implementation injects a true machine learning layer:

Algorithmic Selection: Built using a Random Forest Ensemble (scikit-learn) due to its strength in parsing complex, non-linear conditional thresholds (e.g., assessing an isolated high-value transaction versus a high-value transaction paired with a high historical risk profile).

Feature Encoding Pipeline: Ingests string-categorical dimensions (Fraud Type and Transaction Category) and dynamically prepares them via robust numerical label encoders.

Live Sandbox Assessor: An interactive form at the bottom of the dashboard allowing risk analysts to input simulated parameters—Transaction Amount, User Fraud Score, and Suspected Patterns—to instantly evaluate and flag an anomaly percentage index on demand.

🛠️ Technology Stack
Language: Python

Web Framework: Streamlit

Data Manipulation: Pandas, NumPy

Interactive Visualization: Plotly Express, Plotly Graph Objects

Machine Learning & Pipolining: Scikit-Learn (Random Forest, Label Encoder)

Data Sources Provided: .csv (Cleaned Transaction Profiles) & .pbix (Power BI Compiled Archive)

🚀 Installation & Local Deployment
1. Clone the Repository
Bash
git clone https://github.com/yourusername/credit-card-fraud-risk-analysis.git
cd credit-card-fraud-risk-analysis

2. Install Dependencies
Bash
pip install -r requirements.txt

3. Run the Engine Local Server
Bash
streamlit run app.py
