# using python script to install packages listed in requirements.txt

import subprocess
import os

def install_requirements(requirements_file="requirements.txt"):
    """
    Installs Python packages listed in a requirements.txt file.

    Args:
        requirements_file (str): The path to the requirements.txt file.
    """
    if not os.path.exists(requirements_file):
        print(f"Error: The file '{requirements_file}' was not found.")
        return

    try:
        # Construct the pip install command
        command = ["pip", "install", "-r", requirements_file]

        # Execute the command
        print(f"Installing packages from {requirements_file}...")
        process = subprocess.run(command, check=True, capture_output=True, text=True)

        # Print success message and output
        print("Installation successful!")
        print(process.stdout)

    except subprocess.CalledProcessError as e:
        # Handle errors during installation
        print(f"Error during installation: {e}")
        print(f"Stderr: {e.stderr}")
    except FileNotFoundError:
        print("Error: 'pip' command not found. Ensure Python and pip are installed and in your PATH.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    # Call the function to install requirements
    install_requirements()
