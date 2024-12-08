#!/usr/bin/env python3
"""
Data Processing and Parsing
@author: jashwanthsrinivas
"""

import csv
from datetime import datetime

class DataProcessor:
    def __init__(self):
        self.employees = {}
        self.timesheet_errors = set()
        self.evaluation_errors = set()
        self.sales_errors = set()
        self.duplicate_errors = set()
        self.all_file_ids = set()
        self.missing_ids = set()
        self.evaluation_score_mapping = {
            'excellent': 5,
            'good': 4,
            'dependable': 4,
            'prompt': 4,
            'poor': 2,
            'error': 2,
            'unreliable': 2,
            'late': 2
        }

    def read_employee_data(self):
        """Read and process initial employee data from emp_beg_yr.txt"""
        print("Reading employee data from emp_beg_yr.txt...")
        try:
            with open('emp_beg_yr.txt', 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    emp_id = int(row['ID'])
                    if emp_id in self.employees:
                        self.duplicate_errors.add(emp_id)
                    else:
                        self.employees[emp_id] = {
                            'id': emp_id,
                            'last_name': row['LastName'],
                            'first_name': row['FirstName'],
                            'job_code': row['JobCode'],
                            'base_pay': float(row['BasePay']),
                            'hours': 0,
                            'utilization': 0,
                            'evaluation_score': 0,
                            'sales': 0,
                        }
                        self.all_file_ids.add(emp_id)

                # Find missing IDs in sequence
                for i in range(min(self.all_file_ids), max(self.all_file_ids) + 1):
                    if i not in self.all_file_ids:
                        self.missing_ids.add(i)
        except FileNotFoundError:
            print("Error: emp_beg_yr.txt file not found.")
        except Exception as e:
            print(f"Error reading employee data: {str(e)}")

    def process_timesheets(self):
        """Validate and process timesheet data."""
        print("Processing timesheet data...")
        try:
            with open('timesheet.txt', 'r') as file:
                for line_no, line in enumerate(file, start=1):
                    if line.strip():
                        try:
                            emp_id, hours = line.strip().split(',')
                            emp_id = int(emp_id)
                            hours = float(hours)

                            if emp_id in self.employees:
                                self.employees[emp_id]['hours'] += hours
                            else:
                                self.timesheet_errors.add(emp_id)
                        except ValueError:
                            print(f"Invalid record at line {line_no}: {line.strip()}")
        except Exception as e:
            print(f"Error processing timesheets: {str(e)}")

    def process_evaluations(self):
        """Process employee evaluation data from evaluation.txt"""
        print("Processing evaluation data...")
        try:
            with open('evaluation.txt', 'r') as file:
                for line_no, line in enumerate(file, start=1):
                    if line.strip():
                        try:
                            emp_id, comments = line.strip().split('#', 1)
                            emp_id = int(emp_id)

                            if emp_id in self.employees:
                                positive_count = sum(keyword in comments.lower() for keyword in self.evaluation_score_mapping if keyword in self.evaluation_score_mapping and keyword in comments.lower())
                                negative_count = sum(keyword in comments.lower() for keyword in self.evaluation_score_mapping if keyword in self.evaluation_score_mapping and keyword in comments.lower() and self.evaluation_score_mapping[keyword] < 4)
                                if negative_count == 0:
                                    score = 10.0
                                else:
                                    score = round(positive_count / negative_count, 1)
                                self.employees[emp_id]['evaluation_score'] = score
                            else:
                                self.evaluation_errors.add((emp_id, line_no))
                        except ValueError:
                            print(f"Invalid evaluation record at line {line_no}: {line.strip()}")
        except FileNotFoundError:
            print("Error: evaluation.txt file not found.")
        except Exception as e:
            print(f"Error processing evaluations: {str(e)}")

    def process_sales(self):
        """Process sales data from sales.txt"""
        print("Processing sales data...")
        try:
            with open('sales.txt', 'r') as file:
                for line_no, line in enumerate(file, start=1):
                    if line.strip():
                        try:
                            emp_id, sales = line.strip().split(',')
                            emp_id = int(emp_id)
                            sales = float(sales)

                            if emp_id in self.employees and self.employees[emp_id]['job_code'] == 'D':
                                self.employees[emp_id]['sales'] = sales
                            else:
                                self.sales_errors.add((emp_id, line_no))
                        except ValueError:
                            print(f"Invalid sales record at line {line_no}: {line.strip()}")
        except Exception as e:
            print(f"Error processing sales: {str(e)}")

    def calculate_utilization(self):
        """Calculate utilization rates"""
        print("Calculating utilization rates...")
        total_hours = 0
        total_utilization = 0
        for emp_data in self.employees.values():
            try:
                rate = (emp_data['hours'] / 2250) * 100
                emp_data['utilization'] = min(round(rate, 2), 100)
                total_hours += emp_data['hours']
                total_utilization += emp_data['utilization']
            except Exception as e:
                print(f"Error calculating utilization: {str(e)}")

        average_utilization = total_utilization / len(self.employees)
        print(f"\nUtilization Statistics:")
        print(f"Total Hours Worked: {total_hours:.2f}")
        print(f"Total Utilization: {total_utilization:.2f}%")
        print(f"Average Utilization: {average_utilization:.2f}%")

    def write_error_log(self):
        """Write error log."""
        print("Writing error log...")
        try:
            with open('error.txt', 'w') as file:
                current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                file.write(f"Error Log Generated at: {current_time}\n\n")

                if self.timesheet_errors or self.missing_ids:
                    file.write("Timesheet Errors:\n")
                    for emp_id in sorted(self.timesheet_errors):
                        file.write(f"Timesheet error: Employee ID {emp_id} not found.\n")
                    if self.missing_ids:
                        file.write("\nMissing Employee IDs: {")
                        file.write(", ".join(map(str, sorted(self.missing_ids))))
                        file.write("}\n")
                    file.write("\n")

                if self.evaluation_errors:
                    file.write("Evaluation Errors:\n")
                    for emp_id, line in sorted(self.evaluation_errors):
                        file.write(f"Evaluation error: Employee ID {emp_id} not found at line {line}.\n")
                    file.write("\n")

                if self.sales_errors:
                    file.write("Sales Errors:\n")
                    for emp_id, line in sorted(self.sales_errors):
                        file.write(f"Sales error: Employee ID {emp_id} not found at line {line}.\n")
                    file.write("\n")

                if self.duplicate_errors:
                    file.write("Duplicate Errors:\n")
                    for emp_id in sorted(self.duplicate_errors):
                        file.write(f"Duplicate error: Employee ID {emp_id} found multiple times.\n")
                    file.write("\n")
        except Exception as e:
            print(f"Error writing error log: {str(e)}")

    def write_employee_data(self):
        """Write processed employee data to a CSV file"""
        print("Writing employee data to a CSV file...")
        try:
            with open('employee_data.csv', 'w', newline='') as file:
                fieldnames = ['id', 'last_name', 'first_name', 'job_code', 'base_pay', 'hours', 'utilization', 'evaluation_score', 'sales']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                for emp_data in self.employees.values():
                    writer.writerow({
                        'id': emp_data['id'],
                        'last_name': emp_data['last_name'],
                        'first_name': emp_data['first_name'],
                        'job_code': emp_data['job_code'],
                        'base_pay': emp_data['base_pay'],
                        'hours': emp_data['hours'],
                        'utilization': emp_data['utilization'],
                        'evaluation_score': emp_data['evaluation_score'],
                        'sales': emp_data['sales']
                    })
        except Exception as e:
            print(f"Error writing employee data to CSV: {str(e)}")

    def process_data(self):
        """Main processing method"""
        print("\nStarting data processing...")
        self.read_employee_data()
        self.process_timesheets()
        self.process_evaluations()
        self.process_sales()
        self.calculate_utilization()
        self.write_error_log()
        self.write_employee_data()
        print("\nProcessing complete!")

processor = DataProcessor()
processor.process_data()