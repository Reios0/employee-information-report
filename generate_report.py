import os
import pandas as pd
import matplotlib.pyplot as plt
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML

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

    # Dictionary unpacking is used in all the functions to allow spaces for named aggregation

    salary_country = get_salary_country(df)
    # Plot the dataframe as a bar graph and save it as PNG
    salary_country_plot = salary_country.plot(kind='bar', title='Sum of annual salary by country', xlabel='Country', ylabel='Sum of annual salary')
    salary_country_plot.figure.savefig('plots/salary_country.png', bbox_inches="tight")
    salary_country['Total Annual Salary'] = salary_country['Total Annual Salary'].map(lambda x: f"${'{:,}'.format(x)}") # Format to currency

    salary_city = get_salary_city(df)
    # Plot the dataframe as a bar graph and save it as PNG
    salary_city_plot = salary_city.plot(kind='bar', title='Sum of annual salary by city', xlabel='City', ylabel='Sum of annual salary')
    salary_city_plot.figure.savefig('plots/salary_city.png', bbox_inches="tight")
    salary_city['Total Annual Salary'] = salary_city['Total Annual Salary'].map(lambda x: f"${'{:,}'.format(x)}") # Format to currency

    salary_department = get_salary_department(df)
    # Plot the dataframe as a bar graph and save it as PNG
    salary_department_plot = salary_department.plot(kind='bar', title='Sum of annual salary by department', xlabel='Department', ylabel='Sum of annual salary')
    salary_department_plot.figure.savefig('plots/salary_department.png', bbox_inches="tight")
    salary_department['Total Annual Salary'] = salary_department['Total Annual Salary'].map(lambda x: f"${'{:,}'.format(x)}") # Format to currency
    
    avg_bonus_salary_country = get_avg_bonus_salary_country(df)
    avg_bonus_salary_country['Average Annual Salary'] = avg_bonus_salary_country['Average Annual Salary'].map(lambda x: f"${'{:,}'.format(x)}") # Format to currency
    avg_bonus_salary_country['Average Bonus %'] = avg_bonus_salary_country['Average Bonus %'].map(lambda x: f"{'{:.2f}'.format(x)}%") # Format to percentage
    avg_bonus_salary_city = get_avg_bonus_salary_city(df)
    avg_bonus_salary_city['Average Annual Salary'] = avg_bonus_salary_city['Average Annual Salary'].map(lambda x: f"${'{:,}'.format(x)}") # Format to currency
    avg_bonus_salary_city['Average Bonus %'] = avg_bonus_salary_city['Average Bonus %'].map(lambda x: f"{'{:.2f}'.format(x)}%") # Format to percentage

    avg_age_country = get_avg_age_country(df)
    avg_age_city = get_avg_age_city(df)
    avg_age_department = get_avg_age_department(df)

    num_employee_department = get_num_employee_department(df)
    # Plot the dataframe as a pie graph and save it as PNG
    num_employee_department_plot = num_employee_department.plot(kind='pie', title='Employees in each department', y='Employee Count', ylabel='', legend=None)
    num_employee_department_plot.figure.savefig('plots/num_employee_department.png', bbox_inches="tight")

    num_employee_position = get_num_employee_position(df)
    # Plot the dataframe as a pie graph and save it as PNG
    num_employee_position_plot = num_employee_position.plot(kind='pie', title='Employees in each position', y='Employee Count', ylabel='', labeldistance=None)
    # Change pie graph legend location
    plt.legend(loc=(1, -0.5))
    num_employee_position_plot.figure.savefig('plots/num_employee_position.png', bbox_inches="tight")
    
    current_folder = os.path.dirname(os.path.abspath(__file__))
    
    # Render template html with dataframes
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template('template.html')
    template_vars = {
        'salary_country': salary_country.to_html(),
        'salary_country_plot': 'file:\\' + os.path.join(current_folder, 'plots', 'salary_country.png'),
        'salary_city': salary_city.to_html(),
        'salary_city_plot': 'file:\\' + os.path.join(current_folder, 'plots', 'salary_city.png'),
        'salary_department': salary_department.to_html(),
        'salary_department_plot': 'file:\\' + os.path.join(current_folder, 'plots', 'salary_department.png'),
        'avg_bonus_salary_country': avg_bonus_salary_country.to_html(),
        'avg_bonus_salary_city': avg_bonus_salary_city.to_html(),
        'avg_age_country': avg_age_country.to_html(),
        'avg_age_city': avg_age_city.to_html(),
        'avg_age_department': avg_age_department.to_html(),
        'num_employee_department': num_employee_department.to_html(),
        'num_employee_department_plot': 'file:\\' + os.path.join(current_folder, 'plots', 'num_employee_department.png'),
        'num_employee_position': num_employee_position.to_html(),
        'num_employee_position_plot': 'file:\\' + os.path.join(current_folder, 'plots', 'num_employee_position.png'),
    }
    html_out = template.render(template_vars)
    # Generate pdf
    HTML(string=html_out, base_url=current_folder).write_pdf('report.pdf', presentational_hints=True)