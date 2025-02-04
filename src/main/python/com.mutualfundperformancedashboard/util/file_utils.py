from pathlib import Path
import csv

import yaml, os


class FileUtils:

    @staticmethod
    def get_properties():
        root_dir = FileUtils.get_project_root_pathlib()
        file_name = "config.yml"
        if root_dir:
            file_path = root_dir / "src"  / "main"  / "resources" / file_name
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
            file_path = root_dir / "src"  / "main"  / "resources" / file_name
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
