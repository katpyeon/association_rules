# Association Rule-Based Product Recommendation System

This project is a web application that discovers association rules through Market Basket Analysis and recommends products based on these rules.

## Main Features

- Analyze associations between products in grocery purchase data
- Recommend products that are likely to be purchased together when a specific product is selected
- Easily check results through an intuitive web interface

## Tech Stack

- **Python 3.6+**
- **Poetry**: Dependency management
- **Pandas**: Data analysis and processing
- **MLxtend**: Association rule mining (Apriori algorithm)
- **Gradio**: Web interface implementation

## Installation

### Prerequisites

- Python 3.6 or higher
- [Poetry](https://python-poetry.org/docs/#installation) installed

### Installation Steps

1. Clone the repository

```bash
git clone https://github.com/katpyeon/association_rules.git
cd association_rules
```

2. Install dependencies using Poetry

```bash
poetry install
```

3. Run the project

There are two ways to use Poetry:

**Method 1: Using poetry run (Recommended)**

```bash
poetry run python src/app.py
```

**Method 2: Run Python directly**

```bash
# This command runs in Poetry's environment without manually activating the virtual environment
poetry shell
python src/app.py
```

> **Note**: The latest version of Poetry recommends using `poetry run`. This method ensures your code always runs with the correct dependencies without environment activation issues.

## How to Use

1. Once the application is running, open your web browser and go to `http://localhost:7860`

2. Select a product from the dropdown to receive the top 5 products most likely to be purchased together.

## Dataset

This project uses a grocery purchase dataset (`datasets/groceries_dataset.csv`). The dataset has the following format:

- Member_number: Member ID
- Date: Purchase date
- itemDescription: Name of the purchased product

## Project Structure

```
association_rules/
├── datasets/            # Dataset directory
│   └── groceries_dataset.csv
├── src/                 # Source code
│   └── app.py           # Main application
├── pyproject.toml       # Poetry configuration file
├── poetry.lock          # Poetry dependency lock file
├── .gitignore           # Git ignore file
└── README.md            # Project description
```

## Poetry Development Commands

```bash
# Add a dependency
poetry add <package_name>

# Add a development dependency
poetry add --dev <package_name>

# Update dependencies
poetry update

# Check virtual environment info
poetry env info
```

## Running with a Different Dataset

This project can be used with other transaction datasets. To analyze your own data, follow these steps:

### 1. Prepare Your Dataset

The new dataset should follow this format:

- CSV file format
- Required columns:
  - `Member_number`: Customer ID (will be converted to string)
  - `Date`: Purchase date (must be parsable as a date)
  - `itemDescription`: Name of the purchased product

Example:

```
Member_number,Date,itemDescription
1001,2023-01-05,Milk
1001,2023-01-05,Bread
1002,2023-01-06,Apple
```

### 2. Replace the Dataset

How to add your prepared dataset to the project:

1. Save the new dataset in the `datasets/` directory.
2. Edit the `src/app.py` file to change the data path:

```python
# Find and modify this line
 df = pd.read_csv("datasets/groceries_dataset.csv")

# Change to your new dataset path
 df = pd.read_csv("datasets/your_new_dataset.csv")
```

### 3. Adjust Hyperparameters (Optional)

Depending on your dataset, you can adjust the parameters for generating association rules:

```python
# Find these lines
frequent_itemsets = apriori(as_df, min_support=0.0045, use_colnames=True)
rules = association_rules(frequent_itemsets, metric="conviction", min_threshold=0.001)

# Adjust parameters based on your dataset size and characteristics:
# - min_support: Lower values generate more rules, higher values include only stronger associations
# - min_threshold: Minimum threshold for conviction value
```

### 4. Run the Code

After making changes, run the code as usual:

```bash
poetry run python src/app.py
```

> **Note**: If your dataset is very large, processing may take a long time. It's recommended to test with a smaller sample first.

## License

This project is licensed under the MIT License.


---

<a href="https://www.buymeacoffee.com/katpyeon" target="_blank">
  <img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" height="40" />
</a>