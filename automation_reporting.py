import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import json

# ---------------------- DATA GENERATION ----------------------

def generate_data():
    np.random.seed(42)

    products = ["Laptop", "Phone", "Tablet", "Chair", "Desk"]
    regions = ["North", "South", "East", "West"]

    data = []

    for i in range(1, 201):
        product = np.random.choice(products)
        category = "Electronics" if product in ["Laptop", "Phone", "Tablet"] else "Furniture"
        region = np.random.choice(regions)
        sales = np.random.randint(5000, 60000)
        quantity = np.random.randint(1, 5)
        date = pd.to_datetime("2024-01-01") + pd.to_timedelta(np.random.randint(0, 60), unit='d')

        data.append([i, product, category, region, sales, quantity, date])

    df = pd.DataFrame(data, columns=["OrderID", "Product", "Category", "Region", "Sales", "Quantity", "Date"])
    df.to_csv("sales_data.csv", index=False)

    print("Dataset generated with 200 rows!\n")


# ---------------------- DATA ANALYSIS ----------------------

def analyze_data():

    df = pd.read_csv("sales_data.csv")

    print("Raw Data:")
    print(df.head())

    df.drop_duplicates(inplace=True)
    df['Sales'] = pd.to_numeric(df['Sales'], errors='coerce')
    df['Quantity'] = pd.to_numeric(df['Quantity'], errors='coerce')
    df.dropna(inplace=True)

    df['Date'] = pd.to_datetime(df['Date'])

    print("\nCleaned Data:")
    print(df.head())

    # ---------------- KPI METRICS ----------------
    total_sales = df['Sales'].sum()
    total_orders = df['OrderID'].nunique()

    print(f"\nTotal Sales: {total_sales}")
    print(f"Total Orders: {total_orders}")

    # ---------------- GROUP ANALYSIS ----------------
    sales_by_region = df.groupby('Region')['Sales'].sum()
    sales_by_category = df.groupby('Category')['Sales'].sum()
    sales_by_product = df.groupby('Product')['Sales'].sum()

    print("\nSales by Region:")
    print(sales_by_region)

    print("\nSales by Category:")
    print(sales_by_category)

    print("\nTop Products:")
    print(sales_by_product.sort_values(ascending=False))

    # ---------------- JSON REPORT ----------------
    report = {
        "Total Sales": float(total_sales),
        "Total Orders": int(total_orders),
        "Sales by Region": sales_by_region.to_dict(),
        "Sales by Category": sales_by_category.to_dict(),
        "Top Products": sales_by_product.to_dict()
    }

    with open("report.json", "w") as f:
        json.dump(report, f, indent=4)

    print("\nReport saved as report.json")

    # ---------------- VISUALIZATIONS ----------------

    # Sales by Region
    plt.figure()
    sales_by_region.plot(kind='bar')
    plt.title("Sales by Region")
    plt.ylabel("Sales")
    plt.show()

    # Sales by Category
    plt.figure()
    sales_by_category.plot(kind='bar')
    plt.title("Sales by Category")
    plt.ylabel("Sales")
    plt.show()

    # Top Products
    plt.figure()
    sales_by_product.sort_values(ascending=False).plot(kind='bar')
    plt.title("Sales by Product")
    plt.ylabel("Sales")
    plt.show()

    # Sales Distribution
    plt.figure()
    sns.histplot(df['Sales'], bins=10)
    plt.title("Sales Distribution")
    plt.show()

    # Sales Trend
    plt.figure()
    df_sorted = df.sort_values('Date')
    sns.lineplot(x='Date', y='Sales', data=df_sorted)
    plt.title("Sales Trend Over Time")
    plt.xticks(rotation=30)
    plt.show()

    # Category vs Sales
    plt.figure()
    sns.boxplot(x='Category', y='Sales', data=df)
    plt.title("Sales by Category")
    plt.show()

    # Region vs Sales
    plt.figure()
    sns.boxplot(x='Region', y='Sales', data=df)
    plt.title("Region vs Sales")
    plt.show()

    # Quantity vs Sales
    plt.figure()
    sns.scatterplot(x='Quantity', y='Sales', data=df)
    plt.title("Quantity vs Sales")
    plt.show()


# ---------------------- MAIN ----------------------

if __name__ == "__main__":
    generate_data()
    analyze_data()