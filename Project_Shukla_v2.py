"""
Created on Wed Dec 4 00:09:40 2024
Performance Metrics and Bonus Computation
@author: adarshshukla
"""

import csv
# from statistics import mean, median, stdev

class PerformanceMetricsProcessor:
    def __init__(self):
        self.employees = {}
        self.consultant_eval_scores = {}
        self.bonuses = {}
        self.evaluation_score_mapping = {
            'excellent': 5,
            'good': 4,
            'average': 3,
            'poor': 2,
            'bad': 1
        }

    def extract_evaluation_data(self):
        """Extract and process evaluation data from evaluation.txt"""
        print("Extracting evaluation data...")
        try:
            with open('evaluation.txt', 'r') as file:
                for line in file:
                    if line.strip():
                        parts = line.strip().split('#')
                        if len(parts) >= 2:
                            emp_id = int(parts[0])
                            rating = parts[1].strip().lower()
                            for keyword, score in self.evaluation_score_mapping.items():
                                if keyword in rating:
                                    self.consultant_eval_scores[emp_id] = score
                                    break
                            else:
                                self.consultant_eval_scores[emp_id] = 3
        except Exception as e:
            print(f"Error extracting evaluation data: {str(e)}")

    # def compute_evaluation_scores(self):
    #     """Compute evaluation scores for Consultants and load sales for Directors."""
    #     print("Computing evaluation scores...")
    #     try:
    #         with open('employee_data.csv', 'r') as file:
    #             reader = csv.DictReader(file)
    #             for row in reader:
    #                 emp_id = int(row['id'])
    #                 job_code = row['job_code']
    #                 first_name = row['first_name']
    #                 last_name = row['last_name']
    #
    #                 # Load evaluation score for consultants
    #                 if emp_id in self.consultant_eval_scores:
    #                     score = self.consultant_eval_scores[emp_id]
    #                 else:
    #                     score = 'N/A'
    #
    #                 # Initialize employee data, including sales for Directors
    #                 self.employees[emp_id] = {
    #                     'id': emp_id,
    #                     'first_name': first_name,
    #                     'last_name': last_name,
    #                     'job_code': job_code,
    #                     'base_pay': float(row['base_pay']),
    #                     'hours': float(row['hours']),
    #                     'utilization': float(row['utilization']),
    #                     'evaluation_score': score,
    #                     'sales': float(row['sales']) if job_code == 'D' and row['sales'] else 0
    #                 }
    #     except Exception as e:
    #         print(f"Error computing evaluation scores: {str(e)}")
    def compute_evaluation_scores(self):
        """Compute evaluation scores for Consultants and load sales for Directors."""
        print("Computing evaluation scores...")
        try:
            with open('employee_data.csv', 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    emp_id = int(row['id'])
                    job_code = row['job_code']
                    first_name = row['first_name']
                    last_name = row['last_name']

                    score = self.consultant_eval_scores.get(emp_id, 0)

                    self.employees[emp_id] = {
                        'id': emp_id,
                        'first_name': first_name,
                        'last_name': last_name,
                        'job_code': job_code,
                        'base_pay': float(row['base_pay']),
                        'hours': float(row['hours']),
                        'utilization': float(row['utilization']),
                        'evaluation_score': score,
                        'sales': float(row['sales']) if job_code == 'D' and row['sales'] else 0
                    }
        except Exception as e:
            print(f"Error computing evaluation scores: {str(e)}")

    def determine_bonus_eligibility(self):
        """Determine employees eligible for bonuses."""
        print("Determining bonus eligibility...")
        try:
            utilization_values = []
            for emp in self.employees.values():
                if emp['job_code'] == 'C':
                    utilization_values.append(emp['utilization'])

            if not utilization_values:
                print("No valid utilization data available for bonus eligibility.")
                return

            sorted_utilization = sorted(utilization_values)
            index_65th_percentile = int(len(utilization_values) * 0.65)
            utilization_65th_percentile = sorted_utilization[index_65th_percentile]

            for emp_id, emp_data in self.employees.items():
                if emp_data['job_code'] == 'C' and emp_data['utilization'] >= utilization_65th_percentile and emp_data[
                    'evaluation_score'] != 'N/A' and emp_data['evaluation_score'] >= 3.5:
                    bonus_amount = self.calculate_bonus(emp_data, 0.1)
                    self.bonuses[emp_id] = bonus_amount
                elif emp_data['job_code'] == 'D':
                    bonus_amount = self.calculate_bonus(emp_data, 0.15)
                    self.bonuses[emp_id] = bonus_amount
        except Exception as e:
            print(f"Error determining bonus eligibility: {str(e)}")

    def calculate_bonus(self, emp_data, bonus_rate):
        """Calculate bonuses based on the rate."""
        base_pay = emp_data['base_pay']
        job_code = emp_data['job_code']
        evaluation_score = emp_data['evaluation_score']

        if job_code == 'C' and evaluation_score != 'N/A':
            bonus_cap = 50000
            bonus = base_pay * bonus_rate
        elif job_code == 'D':
            bonus_cap = 150000
            bonus = emp_data.get('sales', 0) * bonus_rate
        else:
            return 0

        return min(bonus, bonus_cap)

    # def write_final_data(self):
    #     """Write final data to emp_end_yr.txt"""
    #     print("Writing final data to emp_end_yr.txt...")
    #     try:
    #         with open('emp_end_yr.txt', 'w') as file:
    #             file.write('ID,FirstName,LastName,JobCode,BasePay,Utilization,Evaluation/Sales,Bonus\n')
    #             for emp_id, emp_data in self.employees.items():
    #                 bonus = self.bonuses.get(emp_id, 0)
    #                 evaluation_score = emp_data['evaluation_score'] if emp_data['job_code'] == 'C' else 0
    #                 if evaluation_score == 'N/A':
    #                     evaluation_score = 0
    #                 file.write(
    #                     f"{emp_data['id']},{emp_data['first_name']},{emp_data['last_name']},{emp_data['job_code']},"
    #                     f"{emp_data['base_pay']},{emp_data['utilization']},{evaluation_score},{bonus}\n"
    #                 )
    #
    #     except Exception as e:
    #         print(f"Error writing final data to emp_end_yr.txt: {str(e)}")
    # def write_final_data(self):
    #     """Write final data to emp_end_yr.txt with correct Evaluation and Sales values."""
    #     print("Writing final data to emp_end_yr.txt...")
    #     try:
    #         with open('emp_end_yr.txt', 'w') as file:
    #             # Header includes separate Evaluation and Sales columns
    #             file.write('ID,FirstName,LastName,JobCode,BasePay,Utilization,Evaluation,Sales,Bonus\n')
    #             for emp_id, emp_data in self.employees.items():
    #                 # Retrieve evaluation and sales values
    #                 evaluation = emp_data.get('evaluation_score', 0)
    #                 sales = emp_data.get('sales', 0)  # Ensure sales is loaded correctly
    #                 bonus = self.bonuses.get(emp_id, 0)
    #
    #                 # Write data to the output file
    #                 file.write(
    #                     f"{emp_data['id']},{emp_data['first_name']},{emp_data['last_name']},{emp_data['job_code']},"
    #                     f"{emp_data['base_pay']},{emp_data['utilization']},{evaluation},{sales},{bonus}\n"
    #                 )
    #         print("emp_end_yr.txt updated successfully.")
    #     except Exception as e:
    #         print(f"Error writing final data to emp_end_yr.txt: {str(e)}")
    def write_final_data(self):
        """Write final data to emp_end_yr.txt with Evaluation and Sales values."""
        print("Writing final data to emp_end_yr.txt...")
        try:
            with open('emp_end_yr.txt', 'w') as file:
                file.write('ID,FirstName,LastName,JobCode,BasePay,Utilization,Evaluation,Sales,Bonus\n')
                for emp_id, emp_data in self.employees.items():
                    evaluation = emp_data.get('evaluation_score', 0)
                    sales = emp_data.get('sales', 0)
                    bonus = self.bonuses.get(emp_id, 0)

                    file.write(
                        f"{emp_data['id']},{emp_data['first_name']},{emp_data['last_name']},{emp_data['job_code']},"
                        f"{emp_data['base_pay']},{emp_data['utilization']},{evaluation},{sales},{bonus}\n"
                    )
            print("emp_end_yr.txt updated successfully.")
        except Exception as e:
            print(f"Error writing final data to emp_end_yr.txt: {str(e)}")

    def process_data(self):
        """Main processing method"""
        print("\nStarting performance metrics and bonus computation...")

        self.extract_evaluation_data()
        self.compute_evaluation_scores()
        self.determine_bonus_eligibility()
        self.write_final_data()

        print("\nProcessing complete!")

processor = PerformanceMetricsProcessor()
processor.process_data()