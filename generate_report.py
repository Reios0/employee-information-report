import pandas as pd

def get_salary_country(df):
    """Return the sum of annual salary by country as a dataframe."""
    return df.groupby(['Country']).agg(**{'Total Annual Salary': ('Annual Salary', 'sum')})

def get_salary_city(df):
    """Return the sum of annual salary by city as a dataframe."""
    return df.groupby(['Country', 'City']).agg(**{'Total Annual Salary': ('Annual Salary', 'sum')})

def get_salary_department(df):
    """Return the sum of annual salary by department as a dataframe."""
    return df.groupby(['Department']).agg(**{'Total Annual Salary': ('Annual Salary', 'sum')})

def get_avg_bonus_salary_country(df):
    """Return the average bonus % and salary by country as a dataframe."""
    return df.groupby(['Country']).agg(**{'Average Bonus %': ('Bonus %', 'mean'), 'Average Annual Salary': ('Annual Salary', 'mean')}).round(2)
    
def get_avg_bonus_salary_city(df):
    """Return the average bonus % and salary by city as a dataframe."""
    return df.groupby(['Country', 'City']).agg(**{'Average Bonus %': ('Bonus %', 'mean'), 'Average Annual Salary': ('Annual Salary', 'mean')}).round(2)

def get_avg_age_country(df):
    """Return the average age by country as a dataframe."""
    return df.groupby(['Country']).agg(**{'Average Age': ('Age', 'mean')}).round(0).astype('int')

def get_avg_age_city(df):
    """Return the average age by city as a dataframe."""
    return df.groupby(['Country', 'City']).agg(**{'Average Age': ('Age', 'mean')}).round(0).astype('int')

def get_avg_age_department(df):
    """Return the average age by department as a dataframe."""
    return df.groupby(['Department']).agg(**{'Average Age': ('Age', 'mean')}).round(0).astype('int')

def get_num_employee_department(df):
    """Return the number of employees in each department as a dataframe."""
    return df.groupby(['Department']).agg(**{'Employee Count': ('Employee ID', 'count')})

def get_num_employee_position(df):
    """Return the number of employees in each position as a dataframe."""
    return df.groupby(['Job Title']).agg(**{'Employee Count': ('Employee ID', 'count')})

if __name__ == "__main__":
    df = pd.read_csv('data/employee_data.csv', encoding='ISO-8859-1', parse_dates=[8, 13]) # Figured out the encoding by using the chardet library
    # Change type of column 'Age' to integer
    df.astype({'Age': 'int'})
    # Change type of column 'Annual Salary' to integer (assumes the sum of annual salary is not greater than 2 billion)
    df['Annual Salary'] = df['Annual Salary'].str.replace('$', '').str.replace(',', '').astype('int')
    # Change type of column 'Bonus %' to integer
    df['Bonus %'] = df['Bonus %'].str.replace('%', '').astype('int')

    # Use dictionary unpacking to allow spaces for named aggregation
    salary_country = get_salary_country(df)
    salary_country['Total Annual Salary'] = salary_country['Total Annual Salary'].map(lambda x: f"${'{:,}'.format(x)}")
    salary_city = get_salary_city(df)
    salary_city['Total Annual Salary'] = salary_city['Total Annual Salary'].map(lambda x: f"${'{:,}'.format(x)}")
    salary_department = get_salary_department(df)
    salary_department['Total Annual Salary'] = salary_department['Total Annual Salary'].map(lambda x: f"${'{:,}'.format(x)}")
    
    avg_bonus_salary_country = get_avg_bonus_salary_country(df)
    avg_bonus_salary_country['Average Annual Salary'] = avg_bonus_salary_country['Average Annual Salary'].map(lambda x: f"${'{:,}'.format(x)}")
    avg_bonus_salary_country['Average Bonus %'] = avg_bonus_salary_country['Average Bonus %'].map(lambda x: f"{'{:.2f}'.format(x)}%")
    avg_bonus_salary_city = get_avg_bonus_salary_city(df)
    avg_bonus_salary_city['Average Annual Salary'] = avg_bonus_salary_city['Average Annual Salary'].map(lambda x: f"${'{:,}'.format(x)}")
    avg_bonus_salary_city['Average Bonus %'] = avg_bonus_salary_city['Average Bonus %'].map(lambda x: f"{'{:.2f}'.format(x)}%")

    avg_age_country = get_avg_age_country(df)
    avg_age_city = get_avg_age_city(df)
    avg_age_department = get_avg_age_department(df)

    num_employee_department = get_num_employee_department(df)
    num_employee_position = get_num_employee_position(df)

