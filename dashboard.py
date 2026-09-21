import pandas as pd
import requests
import streamlit as st

API_URL = "http://localhost:8000"

st.set_page_config(page_title="Revenue Lens", page_icon="📈", layout="wide")
st.title("Revenue Lens")
st.caption("Retail intelligence dashboard powered by FastAPI, pandas, and scikit-learn.")

try:
    overview = requests.get(f"{API_URL}/analytics/overview", timeout=3).json()
    products = requests.get(f"{API_URL}/analytics/products?limit=6", timeout=3).json()
    anomalies = requests.get(f"{API_URL}/analytics/anomalies", timeout=3).json()
except requests.RequestException:
    st.error("Start the API first with: uvicorn revenue_lens.main:app --reload")
    st.stop()

metrics = st.columns(4)
metrics[0].metric("Revenue", f"€{overview['total_revenue']:,.0f}")
metrics[1].metric("Transactions", overview["transactions"])
metrics[2].metric("Customers", overview["unique_customers"])
metrics[3].metric("Repeat customers", f"{overview['repeat_customer_rate']}%")

left, right = st.columns([3, 2])
with left:
    st.subheader("Top products by revenue")
    product_frame = pd.DataFrame(products)
    st.bar_chart(product_frame.set_index("product_name")["revenue"])
    st.dataframe(product_frame, use_container_width=True, hide_index=True)
with right:
    st.subheader("Transactions requiring review")
    st.caption("Isolation Forest flags unusual transaction patterns; review them before taking action.")
    st.dataframe(pd.DataFrame(anomalies), use_container_width=True, hide_index=True)

