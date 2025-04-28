import pandas as pd
from ydata_profiling import ProfileReport

# Load dataset
df = pd.read_csv('../data/crime_dataset_india.csv')

# Generate report
profile = ProfileReport(df, title="Auto Analytics Report 2", explorative=True)
profile.to_file("report2.html")
