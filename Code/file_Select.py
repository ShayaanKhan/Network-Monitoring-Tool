import os

def select_file(current_path="./logs"):
    print("Available files and folders:")
    files = [f for f in os.listdir(current_path) if os.path.isfile(os.path.join(current_path, f)) and f.endswith(".csv")]
    folders = [f for f in os.listdir(current_path) if os.path.isdir(os.path.join(current_path, f))]

    for index, file in enumerate(files):
        print(f"{index + 1}. {file} (CSV)")

    for index, folder in enumerate(folders, start=len(files) + 1):
        print(f"{index}. {folder} (Folder)")

    print(f"{len(files) + len(folders) + 1}. Go back to parent folder")
    print(f"{len(files) + len(folders) + 2}. Cancel")

    selection = input("Enter the number of the file, folder, or option you want to select: ")
    try:
        selection_index = int(selection) - 1
        if 0 <= selection_index < len(files):
            selected_file = files[selection_index]
            relative_path = os.path.join(current_path, selected_file)
            print("Selected file:", relative_path)
            confirm = input("Do you want to select this file? (y/n/c for cancel): ")
            if confirm.lower() == "y":
                return relative_path
            elif confirm.lower() == "c":
                return None
            else:
                return select_file(current_path)
        elif len(files) <= selection_index < len(files) + len(folders):
            selected_folder = folders[selection_index - len(files)]
            print("Opening folder:", selected_folder)
            new_path = os.path.join(current_path, selected_folder)
            return select_file(new_path)
        elif selection_index == len(files) + len(folders):
            parent_path = os.path.dirname(current_path)
            print("Going back to parent folder:", parent_path)
            return select_file(parent_path)
        elif selection_index == len(files) + len(folders) + 1:
            print("Canceling selection.")
            return None
        else:
            print("Invalid selection.")
            return select_file(current_path)
    except ValueError:
        print("Invalid input. Please enter a valid number.")
        return select_file(current_path)
