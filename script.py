import os
import webbrowser
import requests  # Import requests for API calls
from cli import Menu

# Function to wait for the user to press space to return to the main menu
def wait_for_space():
    """Wait for the user to press the spacebar to return to the main menu."""
    input("Press [space] or Enter to return to the main menu...")

# Function to clone a Git repository
def clone_repository(data=None):
    repo_url = input("Enter the Git repository URL to clone: ").strip()
    target_dir = input("Enter the target directory (leave blank for current directory): ").strip()
    
    if not repo_url:
        print("Repository URL cannot be empty.")
        return
    
    command = f"git clone {repo_url}"
    if target_dir:
        command += f" {target_dir}"
    
    print(f"Cloning repository from {repo_url}...")
    os.system(command)
    print("Clone operation completed.")
    wait_for_space()

# Function to open the Git website
def install_git(data=None):
    print("Opening the Git website for installation...")
    webbrowser.open("https://git-scm.com/")
    wait_for_space()

# Function to view online commit history
def view_online_commit_history(data=None):
    repo_url = input("Enter the GitHub repository URL (e.g., https://github.com/user/repo): ").strip()
    
    if not repo_url.startswith("https://github.com/"):
        print("Only GitHub repositories are supported for now.")
        return
    
    # Extract the owner and repo name from the URL
    try:
        _, owner, repo = repo_url.rstrip("/").split("/")[-3:]
    except ValueError:
        print("Invalid GitHub repository URL.")
        return
    
    # GitHub API URL for commits
    api_url = f"https://api.github.com/repos/{owner}/{repo}/commits"
    
    print(f"Fetching commit history for {owner}/{repo}...")
    response = requests.get(api_url)
    
    if response.status_code != 200:
        print(f"Failed to fetch commit history. HTTP Status Code: {response.status_code}")
        return
    
    commits = response.json()
    print(f"Commit history for {owner}/{repo}:")
    for commit in commits[:10]:  # Display the latest 10 commits
        sha = commit.get("sha", "N/A")
        message = commit.get("commit", {}).get("message", "No commit message")
        author = commit.get("commit", {}).get("author", {}).get("name", "Unknown author")
        print(f"- {sha[:7]}: {message} (by {author})")
    wait_for_space()

# Function to initialize a Git repository
def initialize_git_repository(data=None):
    repo_path = input("Enter the path where you want to initialize the Git repository: ").strip()
    
    # Check if the path exists
    if not os.path.exists(repo_path):
        print(f"The path '{repo_path}' does not exist. Please provide a valid path.")
        return
    
    # Check if the path is a directory
    if not os.path.isdir(repo_path):
        print(f"The path '{repo_path}' is not a directory. Please provide a valid directory.")
        return
    
    try:
        # Change to the specified directory
        os.chdir(repo_path)
        print(f"Initializing a new Git repository in '{repo_path}'...")
        
        # Execute the 'git init' command
        result = os.system("git init")
        
        if result == 0:
            print("Git repository initialized successfully.")
        else:
            print("Failed to initialize the Git repository. Please ensure Git is installed and accessible.")
    except Exception as e:
        print(f"An error occurred: {e}")
    wait_for_space()

# Function to exit the program
def exit_program(data=None):
    """Exit the program."""
    print("Exiting the program. Goodbye!")
    exit()  # Exit the program

# Create the menu
menu = Menu("Git CLI Menu")
menu.add_option("Clone a Git repository", clone_repository)
menu.add_option("View Online Commit History", view_online_commit_history)
menu.add_option("Initialize Git Repository", initialize_git_repository)
menu.add_option("Install Git", install_git)
menu.add_option("Exit", exit_program)  # Add the Exit option

if __name__ == "__main__":
    while True:  # Loop to keep returning to the main menu
        menu.run()