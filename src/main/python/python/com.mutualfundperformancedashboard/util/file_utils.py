from pathlib import Path
import csv
import pandas as pd
from datetime import datetime

import yaml, os


class FileUtils:

    @staticmethod
    def get_properties():
        root_dir = FileUtils.get_project_root_pathlib()
        file_name = "config.yml"
        if root_dir:
            file_path = root_dir / "src" / "main" / "resources" / file_name
            return FileUtils.get_properties_from_given_path(file_path)
        else:
            raise RuntimeError(file_name, " not exists in ", root_dir)

    @staticmethod
    def get_properties_from_given_path(file_path):
        with open(file_path, 'r') as file:
            print("loaded")
            properties = yaml.safe_load(file)
        return properties

    @staticmethod
    def get_mutual_funds_list():
        root_dir = FileUtils.get_project_root_pathlib()
        file_name = "mutual_funds_list.csv"
        if root_dir:
            file_path = root_dir / "src" / "main" / "resources" / file_name
            return FileUtils.get_mutual_funds_list_from_csv(file_path)
        else:
            raise RuntimeError(file_name, " not exists in ", root_dir)

    @staticmethod
    def get_mutual_funds_list_from_csv(file_path):
        mutual_funds_list = []

        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            # next(reader)  # Skip the header row (optional). Remove this line if no header row
            for row in reader:
                try:
                    mutual_funds_list.append(row['Scheme_Name'])  # Append the element at the specified index
                except IndexError:
                    print(
                        f"Warning: Row has fewer columns than expected. Skipping row.")  # Handle if row doesn't have the column
                    continue
        return mutual_funds_list

    @staticmethod
    def get_project_root_pathlib(marker="mutual_fund_performance_dashboard"):
        current_path = Path.cwd()
        while current_path != current_path.parent:
            if (current_path / marker).exists() or (current_path / marker).is_dir():
                return current_path / marker
            current_path = current_path.parent
        return None

    @staticmethod
    def save_summaries_to_excel(scheme_summary_list):
        """
        Saves a list of scheme summary DataFrames to an Excel file.

        Args:
            scheme_summary_list: A list of DataFrames, each containing the summary for a single scheme.

        Returns:
            None
        """

        if not scheme_summary_list:
            print("No scheme summaries found. Skipping Excel export.")
            return

        root_dir = FileUtils.get_project_root_pathlib()

        today = datetime.now().strftime('%Y-%m-%d')
        filename = f'scheme_summary_excel_{today}.xlsx'

        target_file_path = root_dir / "src" / "main" / "target" / filename

        with pd.ExcelWriter(target_file_path, engine='xlsxwriter') as writer:
            workbook = writer.book

            # Concatenate all DataFrames into a single DataFrame
            all_summaries_df = pd.concat(scheme_summary_list, ignore_index=True)

            # Write the combined DataFrame to Excel
            all_summaries_df.to_excel(writer, sheet_name='Summary', index=False, header=True)

            # Access the worksheet
            worksheet = writer.sheets['Summary']

            # Apply conditional formatting
            green_format = workbook.add_format({'bg_color': '#C6EFCE'})  # Light Green
            red_format = workbook.add_format({'bg_color': '#F2DEDE'})  # Light Red
            worksheet.conditional_format('D2:D{}'.format(len(all_summaries_df) + 1),
                                         {'type': 'cell', 'criteria': '>', 'value': 0.0,
                                          'format': green_format})  # Changed 'value': 0 to 'value': 0.0
            worksheet.conditional_format('D2:D{}'.format(len(all_summaries_df) + 1),
                                         {'type': 'cell', 'criteria': '<', 'value': 0.0,
                                          'format': red_format})  # Changed 'value': 0 to 'value': 0.0

            # Auto-adjust column widths
            worksheet.autofit()

    @staticmethod
    def save_summaries_to_csv(summaries_list):
        """
        Saves a list of scheme summary DataFrames to a CSV file.

        Args:
            summaries_list: A list of DataFrames, each containing the summary for a single scheme.
            filename: The name of the CSV file to be created.

        Returns:
            None
        """
        if not summaries_list:
            print("No scheme summaries found. Skipping CSV export.")
            return

        root_dir = FileUtils.get_project_root_pathlib()

        today = datetime.now().strftime('%Y-%m-%d')
        filename = f'scheme_summary_csv)_{today}.csv'

        target_file_path = root_dir / "src" / "main" / "target" / filename

        # Concatenate all DataFrames into a single DataFrame
        all_summaries_df = pd.concat(summaries_list, ignore_index=True)

        # Save the DataFrame to CSV
        all_summaries_df.to_csv(target_file_path, index=False)
