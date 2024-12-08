import csv
from statistics import mean, median, stdev


class UserInteraction:
    def __init__(self):
        self.final_employee_data = []
        self.error_log = []
        self.bonus_rate = 0

    # def load_data(self):
    #     try:
    #         with open("emp_end_yr.txt", "r") as f:
    #             reader = csv.DictReader(f)
    #             self.final_employee_data = []
    #             for row in reader:
    #                 self.final_employee_data.append(row)
    #
    #         with open("error.txt", "r") as f:
    #             self.error_log = f.readlines()
    #
    #         print("Data loaded successfully!")
    #     except FileNotFoundError as e:
    #         print("Error loading data files: {}".format(e))
    #     except Exception as e:
    #         print("Unexpected error: {}".format(e))
    def load_data(self):
        """Load employee data from the emp_end_yr.txt."""
        try:
            with open("emp_end_yr.txt", "r") as f:
                reader = csv.DictReader(f)
                self.final_employee_data = []
                for row in reader:
                    emp = {
                        "ID": row["ID"],
                        "FirstName": row["FirstName"],
                        "LastName": row["LastName"],
                        "JobCode": row["JobCode"],
                        "BasePay": self.safe_float(row["BasePay"]),
                        "Utilization": self.safe_float(row["Utilization"]),
                        "Evaluation": self.safe_float(row["Evaluation"]),
                        "Sales": self.safe_float(row["Sales"]),
                        "Bonus": self.safe_float(row["Bonus"]),
                    }
                    self.final_employee_data.append(emp)
            with open("error.txt", "r") as f:
                self.error_log = f.readlines()

            print("Data loaded successfully!")
        except FileNotFoundError as e:
            print(f"Error loading data files: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

    # def simulate_bonus(self, rate):
    #     """Simulate total bonus payout for a given percentage rate"""
    #     try:
    #         rate = float(rate) / 100
    #         total_payout = 0
    #         consultant_count = 0
    #         director_count = 0
    #
    #         for emp in self.final_employee_data:
    #             if emp["JobCode"] == "C":  # Consultant
    #                 if (float(emp["Utilization"]) > self.get_utilization_percentile(65) and
    #                         float(emp["Evaluation/Sales"]) >= 3.5):
    #                     bonus = min(float(emp["BasePay"]) * rate, 50000)
    #                     total_payout += bonus
    #                     consultant_count += 1
    #             elif emp["JobCode"] == "D":  # Director
    #                 if float(emp["Utilization"]) > self.get_utilization_percentile(65):
    #                     try:
    #                         sales = float(emp["Evaluation/Sales"])
    #                         bonus = min(sales * rate, 150000)
    #                         total_payout += bonus
    #                         director_count += 1
    #                     except ValueError:
    #                         continue
    #
    #         print("\nBonus Simulation Results for {:.1f}% rate:".format(rate * 100))
    #         print("Total bonus payout: ${:,.2f}".format(total_payout))
    #         print("Number of eligible Consultants: {}".format(consultant_count))
    #         print("Number of eligible Directors: {}".format(director_count))
    #         if (consultant_count + director_count) > 0:
    #             avg_bonus = total_payout / (consultant_count + director_count)
    #             print("Average bonus per eligible employee: ${:,.2f}".format(avg_bonus))
    #         else:
    #             print("Average bonus per eligible employee: No eligible employees")
    #
    #         return total_payout
    #     except ValueError as e:
    #         print("Error: Invalid rate format. Please enter a numeric value. ({})".format(e))
    #         return 0
    #     except Exception as e:
    #         print("Error simulating bonus: {}".format(e))
    #         return 0
    def simulate_bonus(self, rate):
        """Simulate total bonus payout for a given percentage."""
        try:
            rate = float(rate) / 100
            total_payout = 0
            for emp in self.final_employee_data:
                if emp["JobCode"] == "C":
                    if emp["Evaluation"] >= 3.5:
                        bonus = min(emp["BasePay"] * rate, 50000)
                        total_payout += bonus
                elif emp["JobCode"] == "D":
                    if emp["Sales"] > 0:
                        bonus = min(emp["Sales"] * rate, 150000)
                        total_payout += bonus

            print("\nTotal Bonus Payout: ${:,.2f}".format(total_payout))
            return total_payout
        except Exception as e:
            print(f"Error simulating bonus: {e}")
            return 0

    def get_utilization_percentile(self, percentile):
        """Calculate the specified percentile of utilization rates"""
        try:
            utilizations = []
            for emp in self.final_employee_data:
                utilization_value = float(emp["Utilization"])
                utilizations.append(utilization_value)

            utilizations = sorted(utilizations)  # Sort the list

            index = int(len(utilizations) * percentile / 100)
            return utilizations[index]
        except Exception as e:
            print("Error calculating utilization percentile: {}".format(e))
            return 0

    def safe_float(self, value):
        try:
            return float(value)
        except ValueError:
            return 0.0

    def search_employee(self, emp_id=None, name=None, job_type=None):
        """Search employee details by ID, Name, or Job Type."""
        found = False
        for emp in self.final_employee_data:
            if (
                    (emp_id and emp["ID"] == str(emp_id)) or
                    (name and name.lower() in f"{emp['FirstName']} {emp['LastName']}".lower()) or
                    (job_type and emp["JobCode"] == job_type.upper())
            ):
                found = True
                job_title = "Consultant" if emp["JobCode"] == "C" else "Director"
                print(f"\nID: {emp['ID']}")
                print(f"{job_title}: {emp['FirstName']} {emp['LastName']}")
                print(f"Utilization: {emp['Utilization']}%")
                print(f"Sales: ${emp['Sales']}")
                print(f"Base Pay: ${emp['BasePay']}")
                print(f"Bonus: ${emp['Bonus']}")

        if not found:
            print("No matching employees found.")

    def descriptive_analytics(self):
        print("\nDescriptive Analytics")
        try:
            utilizations = []
            bonuses = []
            evaluations = []
            sales = []

            for emp in self.final_employee_data:
                utilizations.append(self.safe_float(emp["Utilization"]))
                bonuses.append(self.safe_float(emp["Bonus"]))
                evaluations.append(self.safe_float(emp["Evaluation"]))
                sales.append(self.safe_float(emp["Sales"]))

            metrics_data = [
                ("Utilization", utilizations),
                ("Evaluation", evaluations),
                ("Sales", sales),
                ("Bonus", bonuses)
            ]

            for i in range(len(metrics_data)):
                metric = metrics_data[i][0]
                data = metrics_data[i][1]

                valid_data = []
                for value in data:
                    if value > 0:
                        valid_data.append(value)

                if not valid_data:
                    print(f"\n{metric} Statistics: No valid data available.")
                    continue

                print(f"\n{metric} Statistics:")
                print(f"Count: {len(valid_data)}")
                print(f"Mean: {mean(valid_data):.2f}")
                print(f"Median: {median(valid_data):.2f}")
                print(
                    f"Std Dev: {stdev(valid_data):.2f}" if len(valid_data) > 1 else "Std Dev: N/A (insufficient data)")
                print(f"Min: {min(valid_data):.2f}")
                print(f"Max: {max(valid_data):.2f}")
        except Exception as e:
            print(f"Error generating analytics: {e}")

    # def recognition_and_probation(self):
    #     print("\nRecognition and Probation Lists")
    #     try:
    #         utilizations = []
    #         for emp in self.final_employee_data:
    #             utilization_value = self.safe_float(emp["Utilization"])
    #             utilizations.append(utilization_value)
    #
    #         valid_utilizations = []
    #         for value in utilizations:
    #             if value > 0:
    #                 valid_utilizations.append(value)
    #
    #         if not valid_utilizations:
    #             print("No valid utilization data available for recognition or probation.")
    #             return
    #
    #         mean_utilization = mean(valid_utilizations)
    #         std_dev_utilization = stdev(valid_utilizations) if len(valid_utilizations) > 1 else 0
    #         probation_threshold = mean_utilization - std_dev_utilization
    #         max_utilization = max(valid_utilizations)
    #
    #         # Top Performers (Utilization)
    #         top_utilization_performers = []
    #         for emp in self.final_employee_data:
    #             if self.safe_float(emp["Utilization"]) == max_utilization:
    #                 top_utilization_performers.append(emp)
    #
    #         print("\nTop Performers (Highest Utilization):")
    #         for emp in top_utilization_performers:
    #             print(
    #                 f"ID: {emp['ID']}, Name: {emp['FirstName']} {emp['LastName']}, Utilization: {emp['Utilization']}%")
    #
    #         # Top Performers (Sales)
    #         directors = []
    #         for emp in self.final_employee_data:
    #             if emp["JobCode"] == "D":
    #                 directors.append(emp)
    #
    #         top_sales_directors = []
    #         if directors:
    #             max_sales = max(self.safe_float(emp["Evaluation/Sales"]) for emp in directors)
    #             top_sales_directors = []
    #             for emp in directors:
    #                 if self.safe_float(emp["Evaluation/Sales"]) == max_sales:
    #                     top_sales_directors.append(emp)
    #
    #         print("\nTop Performers (Highest Sales):")
    #         for emp in top_sales_directors:
    #             print(f"ID: {emp['ID']}, Name: {emp['FirstName']} {emp['LastName']}, Sales: ${emp['Evaluation/Sales']}")
    #
    #         probation_list = [
    #             emp for emp in self.final_employee_data
    #             if
    #             self.safe_float(emp["Utilization"]) < probation_threshold and emp["JobCode"] == "C" and self.safe_float(
    #                 emp["Evaluation/Sales"]) < 1
    #         ]
    #
    #         print("\nEmployees on Probation (Utilization < Mean - Std Dev and Evaluation Score < 1):")
    #         if probation_list:
    #             for emp in probation_list:
    #                 print(
    #                     f"ID: {emp['ID']}, Name: {emp['FirstName']} {emp['LastName']}, Utilization: {emp['Utilization']}%, Evaluation Score: {emp['Evaluation/Sales']}")
    #         else:
    #             print("No employees meet the probation criteria.")
    #     except Exception as e:
    #         print(f"Error generating lists: {e}")
    def recognition_and_probation(self):
        """Generate recognition and probation lists based on given data format."""
        print("\nRecognition and Probation Lists")
        try:
            consultants = []
            directors = []

            for emp in self.final_employee_data:
                if emp["JobCode"] == "C":
                    consultants.append(emp)
                elif emp["JobCode"] == "D":
                    directors.append(emp)

            # Top Performers: Consultants (Highest Utilization)
            if consultants:
                max_util = -float('inf')

                for emp in consultants:
                    if emp["Utilization"] > max_util:
                        max_util = emp["Utilization"]

                top_consultants = []
                for emp in consultants:
                    if emp["Utilization"] == max_util:
                        top_consultants.append(emp)

                print("\nTop Performers (Highest Utilization):")
                for emp in top_consultants:
                    print(
                        f"ID: {emp['ID']}, Name: {emp['FirstName']} {emp['LastName']}, Utilization: {emp['Utilization']}%")

            # Top Performers: Directors (Highest Sales)
            if directors:
                max_sales = max(emp["Sales"] for emp in directors)
                top_directors = []
                for emp in directors:
                    if emp["Sales"] == max_sales:
                        top_directors.append(emp)
                print("\nTop Performer (Highest Sales):")
                for emp in top_directors:
                    print(f"ID: {emp['ID']}, Name: {emp['FirstName']} {emp['LastName']}, Sales: ${emp['Sales']}")

            # Probation List (Low Utilization and Low Evaluation for Consultants)
            total_util = 0
            count = 0

            for emp in self.final_employee_data:
                total_util += emp["Utilization"]
                count += 1

            if count > 0:
                mean_util = total_util / count
            else:
                mean_util = 0

            if len(self.final_employee_data) > 1:
                utilization_values = [emp["Utilization"] for emp in self.final_employee_data]
                std_dev_util = stdev(utilization_values)
            else:
                std_dev_util = 0

            probation_threshold = mean_util - std_dev_util

            probation_list = []

            for emp in consultants:
                if emp["Utilization"] < probation_threshold and emp["Evaluation"] < 1:
                    probation_list.append(emp)

            print("\nEmployees on Probation (Low Utilization and Evaluation):")
            if probation_list:
                for emp in probation_list:
                    print(
                        f"ID: {emp['ID']}, Name: {emp['FirstName']} {emp['LastName']}, Utilization: {emp['Utilization']}%, Evaluation: {emp['Evaluation']}")
            else:
                print("No employees meet the probation criteria.")
        except Exception as e:
            print(f"Error generating recognition/probation lists: {e}")

    def view_error_log(self):
        print("\nError Log:")
        if self.error_log:
            for line in self.error_log:
                print(line.strip())
        else:
            print("No errors logged.")

ui = UserInteraction()
ui.load_data()

while True:
    print("\nUser Interaction Menu:")
    print("1. Search for Employee")
    print("2. View Descriptive Analytics")
    print("3. Generate Recognition/Probation Lists")
    print("4. View Error Log")
    print("5. Simulate Bonus Rate")
    print("6. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        search_by = input("Search by ID, Name, or Job Type (Enter 'ID', 'Name', or 'Job'): ").lower()
        if search_by == "id":
            emp_id = input("Enter Employee ID: ")
            ui.search_employee(emp_id=emp_id)
        elif search_by == "name":
            name = input("Enter Employee Name: ")
            ui.search_employee(name=name)
        elif search_by == "job":
            job_type = input("Enter Job Type ('C' for Consultant, 'D' for Director): ")
            ui.search_employee(job_type=job_type)
        else:
            print("Invalid search option.")
    elif choice == "2":
        ui.descriptive_analytics()
    elif choice == "3":
        ui.recognition_and_probation()
    elif choice == "4":
        ui.view_error_log()
    elif choice == "5":
        while True:
            rate = input("Enter bonus percentage rate (or 'done' to finish): ")
            if rate.lower() == 'done':
                break
            try:
                ui.simulate_bonus(float(rate))
            except ValueError:
                print("Please enter a valid numeric percentage")
    elif choice == "6":
        print("Exiting program. Adios!")
        break
    else:
        print("Invalid choice. Please try again.")
