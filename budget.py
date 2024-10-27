import os
import json
from beancount import loader
from beancount.query import query
from collections import defaultdict
import pprint

# Set the path to your Beancount files
beancount_dir = "data/sample/"  # Replace this with the actual path
main_beancount = os.path.join(beancount_dir, "example.beancount")

# Load your Beancount file
entries, errors, options_map = loader.load_file(main_beancount)

if errors:
    print("Warning: There were errors when loading the Beancount file:")


# Define your budget
annual_budget = {
    # Fixed Expenses
    'Home:Dues': 858,
    'Home:Utilities:Electricity': 720,
    'Home:Utilities:Garbage': 392,
    'Home:Utilities:Internet': 600,
    'Home:Utilities:Propane': 1800,
    'Home:Utilities:Water': 888,
    'Transport:Car:Insurance': 3720,
    
    # Variable Expenses
    'Food:Groceries': 9600,
    'Food:Restaurant': 4800,
    'Food:Coffee': 600,
    'Food:Alcohol': 1200,
    'Transport:Car:Gas': 3000,
    'Transport:Car:Maintenance': 1200,
    'Transport:Car:Parking': 360,
    'Transport:Car:Toll': 240,
    'Healthcare': 2400,
    'Clothing': 2400,
    'Home:Consumables': 1200,
    'Home:Maintenance': 1800,
    'Home:Phone': 1200,
    
    # Pet Expenses (Charlie)
    'Charlie:Food': 1200,
    'Charlie:Healthcare': 600,
    'Charlie:Sitting': 600,
    'Charlie:Entertainment': 300,
    
    # Discretionary Expenses
    'Entertainment': 2400,
    'Entertainment:Gaming': 600,
    'Recreation': 2400,
    'Recreation:MountainBiking': 1200,
    'Recreation:Paragliding': 1200,
    'Recreation:Ski': 1200,
    'Travel:Airfare': 3600,
    'Travel:Hotel': 2400,
    'Travel:CarRental': 1200,
    'Travel:Transit': 600,
    'Travel:Miscellaneous': 600,
    'Computers': 1200,
    'Computers:Cloud': 240,
    'Computers:Accessories': 360,
    'Education': 1200,
    'Gift': 1200,
    'Fitness': 1200,
    
    # Savings and Investments
    'Home:Improvements': 3600,
}

monthly_budget = {k: v/12 for k, v in annual_budget.items()} # this needs to be modified to the list of things i actually budget monthly
 
# Queries
annual_query = """
SELECT
    YEAR(date) AS year,
    account,
    SUM(COST(position)) AS annual_sum
WHERE
    account ~ 'Expenses:.*'
GROUP BY
    year, account
ORDER BY
    year, account
"""

monthly_query = """
SELECT
    YEAR(date) AS year,
    MONTH(date) AS month,
    account,
    SUM(COST(position)) AS monthly_sum
WHERE
    account ~ 'Expenses:.*'
GROUP BY
    year, month, account
ORDER BY
    year, month, account
"""

# Run queries
annual_results = query.run_query(entries, options_map, query=annual_query)
monthly_results = query.run_query(entries, options_map, query=monthly_query)



# Helper function to categorize expenses
def categorize_expense(account):
    fixed_expenses = ['Home:Dues', 'Home:Utilities:', 'Transport:Car:Insurance']
    variable_expenses = ['Food:', 'Transport:Car:', 'Healthcare', 'Clothing', 'Home:Consumables', 'Home:Maintenance', 'Home:Phone']
    pet_expenses = ['Charlie:']
    discretionary_expenses = ['Entertainment', 'Recreation', 'Travel', 'Computers', 'Education', 'Gift', 'Fitness']
    
    if any(account.startswith(category) for category in fixed_expenses):
        return "Fixed Expenses"
    elif any(account.startswith(category) for category in variable_expenses):
        return "Variable Expenses"
    elif any(account.startswith(category) for category in pet_expenses):
        return "Pet Expenses (Charlie)"
    elif any(account.startswith(category) for category in discretionary_expenses):
        return "Discretionary Expenses"
    elif account.startswith('Home:Improvements'):
        return "Savings and Investments"
    else:
        return "Other Expenses"

'''
# Process annual results
print("Annual Budget Comparison:")
annual_totals = defaultdict(float)
for row in annual_results[1]:  # Access the data rows from the results tuple
    year = row.year
    account = row.account.split('Expenses:')[-1]
    actual = float(row.annual_sum.get_positions()[0].units.number)
    budgeted = annual_budget.get(account, 0)
    difference = actual - budgeted
    category = categorize_expense(account)
    annual_totals[category] += actual
    print(f"{year} - {account}: Budget ${budgeted:.2f}, Actual ${actual:.2f}, Difference ${difference:.2f}")

# Process monthly results
print("\nMonthly Budget Comparison:")
monthly_totals = defaultdict(lambda: defaultdict(float))
for row in monthly_results[1]:  # Access the data rows from the results tuple
    year = row.year
    month = row.month
    account = row.account.split('Expenses:')[-1]
    actual = float(row.monthly_sum.get_positions()[0].units.number)
    category = categorize_expense(account)
    monthly_totals[f"{year}-{month:02d}"][category] += actual

for year_month, categories in monthly_totals.items():
    print(f"\n{year_month}:")
    total_actual = sum(categories.values())
    total_budgeted = sum(monthly_budget.values())
    for category, actual in categories.items():
        print(f"  {category}: Actual ${actual:.2f}")
    print(f"  Overall: Budget ${total_budgeted:.2f}, Actual ${total_actual:.2f}, Difference ${total_actual - total_budgeted:.2f}")

# Identify uncategorized or unexpected expenses
print("\nUncategorized or Unexpected Expenses:")
for row in annual_results[1]:  # Access the data rows from the results tuple
    account = row.account.split('Expenses:')[-1]
    if account not in annual_budget and account != 'FIXME':
        actual = float(row.annual_sum.get_positions()[0].units.number)
        print(f"{account}: ${actual:.2f}")

print("\nNote: 'FIXME' category is excluded from comparisons. Please review these separately.")

'''


def analyze_budget():
    # Create data structure to hold all our analysis
    category_totals = defaultdict(lambda: {"budget": 0, "actual": 0, "items": []})
    
    # Calculate budget totals for each category
    for account, budget in annual_budget.items():
        category = categorize_expense(account)
        category_totals[category]["budget"] += budget
    
    # Process actual spending
    for row in annual_results[1]:
        account = row.account.split('Expenses:')[-1]
        actual = float(row.annual_sum.get_positions()[0].units.number)
        budgeted = annual_budget.get(account, 0)
        difference = actual - budgeted
        category = categorize_expense(account)
        
        # Add to category totals
        category_totals[category]["actual"] += actual
        
        # Store item details
        category_totals[category]["items"].append({
            "name": account.split(':')[-1] if ':' in account else account,
            "budget": budgeted,
            "actual": actual,
            "difference": difference,
            "percentageUsed": (actual / budgeted * 100) if budgeted > 0 else 0
        })
        
        # Print detailed line item
        print(f"{row.year} - {account}: Budget ${budgeted:.2f}, Actual ${actual:.2f}, Difference ${difference:.2f}")
    
    # Convert to list format for JSON
    category_data = []
    for category, data in category_totals.items():
        category_data.append({
            "category": category,
            "budget": data["budget"],
            "actual": data["actual"],
            "difference": data["actual"] - data["budget"],
            "percentageUsed": (data["actual"] / data["budget"] * 100) if data["budget"] > 0 else 0,
            "items": sorted(data["items"], key=lambda x: abs(x["difference"]), reverse=True)
        })
    
    # Print monthly summary
    print("\nMonthly Budget Comparison:")
    monthly_totals = defaultdict(lambda: defaultdict(float))
    for row in monthly_results[1]:
        month_key = f"{row.year}-{row.month:02d}"
        account = row.account.split('Expenses:')[-1]
        actual = float(row.monthly_sum.get_positions()[0].units.number)
        category = categorize_expense(account)
        monthly_totals[month_key][category] += actual

    for month_key, categories in monthly_totals.items():
        print(f"\n{month_key}:")
        total_actual = sum(categories.values())
        total_budgeted = sum(monthly_budget.values())
        for category, actual in categories.items():
            print(f"  {category}: Actual ${actual:.2f}")
        print(f"  Overall: Budget ${total_budgeted:.2f}, Actual ${total_actual:.2f}, "
              f"Difference ${total_actual - total_budgeted:.2f}")
    
    # Print uncategorized expenses
    print("\nUncategorized or Unexpected Expenses:")
    for row in annual_results[1]:
        account = row.account.split('Expenses:')[-1]
        if account not in annual_budget and account != 'FIXME':
            actual = float(row.annual_sum.get_positions()[0].units.number)
            print(f"{account}: ${actual:.2f}")
    
    return category_data

if __name__ == "__main__":
    print("Annual Budget Comparison:")
    export_data = analyze_budget()
    
    # Export to JSON
    os.makedirs("output", exist_ok=True)
    json_file = os.path.join("output", "budget_data.json")
    with open(json_file, "w") as f:
        json.dump(export_data, f, indent=2)
    print(f"\nData exported to {json_file}")
    
    # Print overall summary
    total_budget = sum(annual_budget.values())
    total_actual = sum(category["actual"] for category in export_data)
    print(f"\nOverall Summary:")
    print(f"Total Budget: ${total_budget:,.2f}")
    print(f"Total Actual: ${total_actual:,.2f}")
    print(f"Difference: ${total_actual - total_budget:,.2f}")