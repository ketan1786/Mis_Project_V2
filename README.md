
# **Employee Performance Evaluation and Bonus Calculation System**

## **Project Overview**
This project processes employee data, evaluates performance metrics, calculates bonuses, and provides interactive tools for advanced analysis. It consists of three main components: data processing, performance evaluation, and user interaction with analytics.

## **File Structure**
1. **`Project_Srinivas_v3.py`** - Handles data processing and parsing.
2. **`Project_Shukla_v2.py`** - Computes performance metrics and determines bonuses.
3. **`ketan_new_v3.py`** - Implements user interaction, advanced analytics, and descriptive statistics.

## **Project Flow**
1. **Data Processing and Parsing (Team Member 1)**:
   - Run `Project_Srinivas_v3.py`.
   - This script reads and processes raw data from files (`sales.txt`, `timesheet.txt`, `evaluation.txt`, `emp_beg_yr.txt`).
   - Outputs:
     - A cleaned and processed `employee_data.csv`.
     - An `error.txt` log for any data inconsistencies.
   - Utilization rates are also calculated during this step.

2. **Performance Metrics and Bonus Calculation (Team Member 2)**:
   - Run `Project_Shukla_v2.py`.
   - This script:
     - Processes evaluation scores for consultants.
     - Determines bonus eligibility based on evaluation scores and utilization rates.
     - Calculates bonuses for consultants and directors.
     - Outputs the final processed data into `emp_end_yr.txt`.

3. **User Interaction and Analytics (Team Member 3)**:
   - Run `ketan_new_v3.py`.
   - This script allows users to:
     - Search employee details.
     - Simulate bonus payouts based on different rates.
     - View recognition and probation lists.
     - Analyze data using descriptive statistics.
     - View the error log for debugging.

## **Execution Instructions**
1. Ensure all required input files (`sales.txt`, `timesheet.txt`, `evaluation.txt`, `emp_beg_yr.txt`) are in the same directory as the scripts.
2. Run the scripts in the following order:
   - Step 1: `Project_Srinivas_v3.py` for data processing.
   - Step 2: `Project_Shukla_v2.py` for performance and bonus calculations.
   - Step 3: `ketan_new_v3.py` for user interaction and analytics.
3. After running all scripts, final outputs will be available in:
   - `emp_end_yr.txt` (final employee data with bonuses).
   - `employee_data.csv` (cleaned and processed raw data).
   - `error.txt` (error log for any inconsistencies).

## **Prerequisites**
- Python 3.x installed on your system.
- Libraries required:
  - `csv`
  - `statistics`
  - `datetime`

## **Collaboration**
- Each team member has contributed a specific module:
  - **Data Processing**: `Project_Srinivas_v3.py`.
  - **Performance Metrics and Bonus Calculation**: `Project_Shukla_v2.py`.
  - **User Interaction and Advanced Features**: `ketan_new_v3.py`.

## **Support**
For questions or issues, please contact the project team.
