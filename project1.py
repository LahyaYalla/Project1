import pandas as pd
from datetime import timedelta

def analyze_employee_data(file_path):
    df = pd.read_csv(file_path)

    unique_values = df['Timecard Hours (as Time)'].unique()
    print("Unique values in 'Timecard Hours (as Time)':")
    print(unique_values)

    df['Timecard Hours (as Time)'] = pd.to_timedelta(df['Timecard Hours (as Time)'], errors='coerce')

    df['Time'] = pd.to_datetime(df['Time'], errors='coerce')

    df.sort_values(['Employee Name', 'Time'], inplace=True)

    df.reset_index(drop=True, inplace=True)

    def check_consecutive_days(series):
        return (series.diff().dt.days == 1).all()

    def check_time_between_shifts(group):
        time_diff = group['Time'].diff().shift(-1)
        return ((time_diff < timedelta(hours=10)) & (time_diff > timedelta(hours=1))).any()

    def check_hours_worked(group):
        return (group['Timecard Hours (as Time)'] > timedelta(hours=14)).any()

    consecutive_days = df.groupby('Employee Name')['Time'].agg(check_consecutive_days)
    time_between_shifts = df.groupby('Employee Name').apply(check_time_between_shifts)
    hours_worked = df.groupby('Employee Name').apply(check_hours_worked)

    print("\nEmployees who have worked for 7 consecutive days:")
    print(consecutive_days[consecutive_days].index.tolist())

    print("\nEmployees who have less than 10 hours between shifts but greater than 1 hour:")
    print(time_between_shifts[time_between_shifts].index.tolist())

    print("\nEmployees who have worked for more than 14 hours in a single shift:")
    print(hours_worked[hours_worked].index.tolist())

if __name__ == "__main__":
    file_path = r"C:\Users\lahya\Downloads\Assignment_Timecard.xlsx - Sheet1.csv"
    analyze_employee_data(file_path)
