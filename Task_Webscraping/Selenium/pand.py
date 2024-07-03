import pandas as pd

# Read the CSV file into a Pandas DataFrame
df = pd.read_csv('C:\Users\laksh\OneDrive\Desktop\Beautiful_souap\Selenium\ProformaInvoice_STL Digital.csv')
existing_column = df['Remarks / Payment Instructions:']

# Define values for the new column based on existing column
# For example, let's say we want to double the values in the existing column
new_column_values = existing_column * 2

# Insert the new column into the DataFrame
# You can specify the position using the 'insert' method
# For example, let's insert the new column after the existing column
df.insert(loc=df.columns.get_loc('Remarks / Payment Instructions:') + 1, column='New_Column_Name', value=new_column_values)

# Alternatively, you can just assign the new column to the DataFrame
# df['New_Column_Name'] = new_column_values

# Save the modified DataFrame to a new CSV file or overwrite the existing one
df.to_csv('output_file.csv', index=False)
