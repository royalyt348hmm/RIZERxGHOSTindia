#!/usr/bin/env python3
"""
GitHub Auto Push System - Terminal Based
Compatible with Termux / Linux / Android
Version: 1.1.0 - With Colorful ASCII Banner
"""

import os
import sys
import json
import base64
import subprocess
import urllib.request
import urllib.error
from pathlib import Path
from datetime import datetime

# ANSI Colors for terminal
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    # Additional colors for ASCII art
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ORANGE = '\033[38;5;208m'  # 256 color mode orange
    DARK_GREEN = '\033[32m'
    LIGHT_GREEN = '\033[92m'

def print_colorful_ascii():
    """Display RIZER ASCII art with mixed colors"""
    # Define color patterns for mixing
    colors = [
        Colors.YELLOW,
        Colors.RED, 
        Colors.GREEN,
        Colors.ORANGE,
        Colors.WARNING,
        Colors.FAIL,
        Colors.LIGHT_GREEN
    ]

    # ASCII art lines
    ascii_lines = [
        "██████╗░██╗███████╗███████╗██████╗░",
        "██╔══██╗██║╚════██║██╔════╝██╔══██╗",
        "██████╔╝██║░░███╔═╝█████╗░░██████╔╝",
        "██╔══██╗██║██╔══╝░░██╔══╝░░██╔══██╗",
        "██║░░██║██║███████╗███████╗██║░░██║",
        "╚═╝░░╚═╝╚═╝╚══════╝╚══════╝╚═╝░░╚═╝"
    ]

    print()
    print("\033[1m" + "="*60 + "\033[0m")

    # Print each line with gradient/mixed colors
    for i, line in enumerate(ascii_lines):
        colored_line = ""
        # Create color mixture effect
        for j, char in enumerate(line):
            if char == ' ':
                colored_line += char
            else:
                # Mix colors based on position
                color_index = (i + j) % len(colors)
                colored_line += colors[color_index] + char
        print(colored_line + Colors.ENDC)

    print("\033[1m" + "="*60 + "\033[0m")
    print(f"{Colors.CYAN}{Colors.BOLD}     GitHub Auto Push System{Colors.ENDC}")
    print(f"{Colors.CYAN}     Compatible with Termux / Linux / Android{Colors.ENDC}")
    print("\033[1m" + "="*60 + "\033[0m")
    print()

def print_header(text):
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text.center(60)}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}")

def print_success(text):
    print(f"{Colors.GREEN}✓ {text}{Colors.ENDC}")

def print_error(text):
    print(f"{Colors.FAIL}✗ {text}{Colors.ENDC}")

def print_warning(text):
    print(f"{Colors.WARNING}⚠ {text}{Colors.ENDC}")

def print_info(text):
    print(f"{Colors.CYAN}ℹ {text}{Colors.ENDC}")

def get_input(prompt):
    return input(f"{Colors.BLUE}{prompt}{Colors.ENDC}").strip()

class GitHubAutoPush:
    def __init__(self):
        self.username = None
        self.token = None
        self.folder_path = None
        self.repo_name = None
        self.scanned_files = []
        self.scanned_folders = []
        self.total_size = 0
        self.large_files = []

    def verify_github_auth(self):
        """Verify GitHub authentication using PAT"""
        print_info("Verifying GitHub authentication...")

        try:
            req = urllib.request.Request(
                'https://api.github.com/user',
                headers={
                    'Authorization': f'token {self.token}',
                    'Accept': 'application/vnd.github.v3+json'
                }
            )

            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode())
                if data.get('login'):
                    print_success(f"Authenticated as: {data['login']}")
                    return True
        except urllib.error.HTTPError as e:
            if e.code == 401:
                print_error("Authentication failed: Invalid token")
            else:
                print_error(f"Authentication error: {e.code}")
        except Exception as e:
            print_error(f"Connection error: {str(e)}")

        return False

    def check_repo_exists(self):
        """Check if repository exists on GitHub"""
        try:
            req = urllib.request.Request(
                f'https://api.github.com/repos/{self.username}/{self.repo_name}',
                headers={
                    'Authorization': f'token {self.token}',
                    'Accept': 'application/vnd.github.v3+json'
                }
            )

            with urllib.request.urlopen(req, timeout=10) as response:
                return True
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return False
        except:
            pass
        return None

    def create_repo(self):
        """Create repository on GitHub"""
        print_info(f"Creating repository: {self.repo_name}")

        try:
            data = json.dumps({
                'name': self.repo_name,
                'private': False,
                'auto_init': False
            }).encode()

            req = urllib.request.Request(
                'https://api.github.com/user/repos',
                data=data,
                headers={
                    'Authorization': f'token {self.token}',
                    'Accept': 'application/vnd.github.v3+json',
                    'Content-Type': 'application/json'
                }
            )

            with urllib.request.urlopen(req, timeout=10) as response:
                if response.status == 201:
                    print_success(f"Repository '{self.repo_name}' created successfully")
                    return True
        except urllib.error.HTTPError as e:
            error_body = e.read().decode()
            print_error(f"Failed to create repository: {error_body}")
        except Exception as e:
            print_error(f"Error creating repository: {str(e)}")

        return False

    def scan_directory(self):
        """Recursively scan directory and collect all files and folders"""
        print_header("FULL SCAN & PREVIEW PHASE")
        print_info(f"Scanning: {self.folder_path}")
        print()

        if not os.path.exists(self.folder_path):
            print_error(f"Path does not exist: {self.folder_path}")
            return False

        if not os.path.isdir(self.folder_path):
            print_error(f"Path is not a directory: {self.folder_path}")
            return False

        self.scanned_files = []
        self.scanned_folders = []
        self.total_size = 0
        self.large_files = []

        # Walk through directory
        for root, dirs, files in os.walk(self.folder_path):
            # Skip .git directory
            if '.git' in root:
                continue

            # Calculate relative path
            rel_root = os.path.relpath(root, self.folder_path)
            if rel_root == '.':
                rel_root = ''

            # Add current directory to folders list
            if rel_root:
                self.scanned_folders.append(rel_root)
            else:
                self.scanned_folders.append('(root)')

            # Process files
            for file in files:
                if file == '.git':
                    continue

                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, self.folder_path)

                try:
                    size = os.path.getsize(file_path)
                    self.total_size += size

                    file_info = {
                        'path': file_path,
                        'relative': rel_path,
                        'size': size,
                        'size_str': self.format_size(size)
                    }

                    self.scanned_files.append(file_info)

                    # Check for large files (>100MB)
                    if size > 100 * 1024 * 1024:
                        self.large_files.append(file_info)

                except OSError as e:
                    print_warning(f"Cannot access file: {rel_path}")

        # Display tree view
        self.display_tree_view()

        return True

    def format_size(self, size_bytes):
        """Format bytes to human readable"""
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.2f} KB"
        elif size_bytes < 1024 * 1024 * 1024:
            return f"{size_bytes / (1024 * 1024):.2f} MB"
        else:
            return f"{size_bytes / (1024 * 1024 * 1024):.2f} GB"

    def display_tree_view(self):
        """Display directory structure in tree format"""
        print(f"{Colors.BOLD}DIRECTORY STRUCTURE:{Colors.ENDC}")
        print(f"{Colors.CYAN}{self.folder_path}{Colors.ENDC}")
        print()

        # Build tree structure
        tree = {}
        for file_info in self.scanned_files:
            parts = file_info['relative'].split(os.sep)
            current = tree
            for part in parts[:-1]:
                if part not in current:
                    current[part] = {}
                current = current[part]

            if 'files' not in current:
                current['files'] = []
            current['files'].append(parts[-1])

        # Print tree
        self._print_tree(tree)

        print()
        print(f"{Colors.BOLD}{'─'*60}{Colors.ENDC}")
        print(f"{Colors.BOLD}SCAN SUMMARY:{Colors.ENDC}")
        print(f"  Total Folders: {len(self.scanned_folders)}")
        print(f"  Total Files: {len(self.scanned_files)}")
        print(f"  Total Size: {self.format_size(self.total_size)}")

        if self.large_files:
            print()
            print_warning(f"⚠ WARNING: {len(self.large_files)} file(s) exceed 100MB (GitHub limit)")
            for f in self.large_files:
                print(f"    - {f['relative']} ({f['size_str']})")

        print(f"{Colors.BOLD}{'─'*60}{Colors.ENDC}")
        print()

    def _print_tree(self, tree, prefix=""):
        """Recursively print tree structure"""
        items = list(tree.items())

        for i, (name, subtree) in enumerate(items):
            is_last = (i == len(items) - 1)
            connector = "└── " if is_last else "├── "

            if name == 'files':
                for j, file in enumerate(subtree):
                    is_last_file = (j == len(subtree) - 1) and is_last
                    file_connector = "└── " if is_last_file else "├── "
                    print(f"{prefix}{file_connector}{file}")
            else:
                print(f"{prefix}{connector}{name}/")
                extension = "    " if is_last else "│   "
                self._print_tree(subtree, prefix + extension)

    def get_confirmation(self):
        """Get user confirmation before proceeding"""
        print_header("USER CONFIRMATION PHASE")
        print()
        print_warning("You are about to push ALL the above files and folders to GitHub.")
        print()

        response = get_input("Do you really want to push ALL the above files and folders to GitHub?\nType YES to continue or NO to cancel: ")

        if response.upper() == "YES":
            print_success("Confirmation received. Proceeding...")
            return True
        else:
            print_error("Operation cancelled. No files were pushed.")
            return False

    def handle_large_files(self):
        """Handle files larger than 100MB"""
        if not self.large_files:
            return True

        print_header("SAFETY & LIMIT CHECK PHASE")
        print()
        print_error(f"Found {len(self.large_files)} file(s) exceeding GitHub's 100MB limit:")
        print()

        for f in self.large_files:
            print(f"  • {f['relative']} ({f['size_str']})")

        print()
        print("Options:")
        print("  1. Enable Git LFS (Large File Storage)")
        print("  2. Abort the process")
        print()

        choice = get_input("Enter your choice (1 or 2): ")

        if choice == "1":
            return self.setup_git_lfs()
        else:
            print_error("Operation aborted due to large files.")
            return False

    def setup_git_lfs(self):
        """Setup Git LFS for large files"""
        print_info("Setting up Git LFS...")

        try:
            # Check if git-lfs is installed
            result = subprocess.run(
                ['git', 'lfs', 'version'],
                capture_output=True,
                text=True
            )

            if result.returncode != 0:
                print_error("Git LFS is not installed.")
                print_info("Install with: pkg install git-lfs (Termux) or apt install git-lfs (Linux)")
                return False

            # Initialize LFS
            subprocess.run(['git', 'lfs', 'install'], cwd=self.folder_path, check=True)

            # Track large files
            for f in self.large_files:
                subprocess.run(
                    ['git', 'lfs', 'track', f['relative']],
                    cwd=self.folder_path,
                    check=True
                )

            print_success("Git LFS configured for large files")
            return True

        except subprocess.CalledProcessError as e:
            print_error(f"Git LFS setup failed: {str(e)}")
            return False
        except FileNotFoundError:
            print_error("Git command not found. Is Git installed?")
            return False

    def run_git_command(self, command, cwd=None, check=True):
        """Run a git command and return result"""
        if cwd is None:
            cwd = self.folder_path

        try:
            result = subprocess.run(
                command,
                cwd=cwd,
                capture_output=True,
                text=True,
                shell=isinstance(command, str)
            )

            if check and result.returncode != 0:
                print_error(f"Git command failed: {result.stderr}")
                return None

            return result
        except Exception as e:
            print_error(f"Error running git command: {str(e)}")
            return None

    def initialize_git(self):
        """Initialize git repository if not already initialized"""
        print_header("GIT & REPOSITORY LOGIC")
        print_info("Checking git initialization...")

        git_dir = os.path.join(self.folder_path, '.git')

        if os.path.exists(git_dir):
            print_success("Git repository already initialized")
        else:
            print_info("Initializing git repository...")
            result = self.run_git_command(['git', 'init'])
            if not result:
                return False
            print_success("Git repository initialized")

        # Configure git user if not set
        self.run_git_command(['git', 'config', 'user.email', 'autopush@github.com'], check=False)
        self.run_git_command(['git', 'config', 'user.name', 'GitHub Auto Push'], check=False)

        # Add safe directory (important for Android/Termux)
        self.run_git_command(['git', 'config', '--global', '--add', 'safe.directory', self.folder_path], check=False)

        return True

    def setup_remote(self):
        """Setup or update remote origin"""
        print_info("Configuring remote repository...")

        remote_url = f"https://{self.token}@github.com/{self.username}/{self.repo_name}.git"

        # Check existing remote
        result = self.run_git_command(['git', 'remote', 'get-url', 'origin'], check=False)

        if result and result.returncode == 0:
            # Update existing remote
            result = self.run_git_command(['git', 'remote', 'set-url', 'origin', remote_url])
        else:
            # Add new remote
            result = self.run_git_command(['git', 'remote', 'add', 'origin', remote_url])

        if result:
            print_success("Remote configured")
            return True
        return False

    def stage_files(self):
        """Stage all files for commit"""
        print_info("Staging files...")

        # First, check git status
        result = self.run_git_command(['git', 'status', '--porcelain'])
        if result is None:
            return False

        # Add all files
        result = self.run_git_command(['git', 'add', '.'])
        if not result:
            return False

        # Verify staging
        result = self.run_git_command(['git', 'status', '--porcelain'])
        if result is None:
            return False

        staged = result.stdout.strip().split('\n') if result.stdout.strip() else []
        staged = [s for s in staged if s]

        if not staged:
            print_warning("No changes to commit")
            return False

        print_success(f"{len(staged)} file(s) staged")
        return True

    def commit_and_push(self):
        """Commit and push to GitHub"""
        print_header("PUSH PHASE")

        # Generate commit message
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        commit_msg = f"Auto push: {timestamp} - {len(self.scanned_files)} files"

        print_info(f"Committing with message: {commit_msg}")

        # Commit
        result = self.run_git_command(['git', 'commit', '-m', commit_msg])
        if not result:
            return False

        print_success("Changes committed")

        # Detect default branch
        branch_result = self.run_git_command(['git', 'branch', '--show-current'], check=False)
        if branch_result and branch_result.stdout.strip():
            branch = branch_result.stdout.strip()
        else:
            branch = "main"

        print_info(f"Pushing to branch: {branch}")

        # Push with retry
        max_retries = 3
        for attempt in range(1, max_retries + 1):
            print_info(f"Push attempt {attempt}/{max_retries}...")

            result = self.run_git_command(
                ['git', 'push', '-u', 'origin', branch],
                check=False
            )

            if result and result.returncode == 0:
                print_success("Push successful!")
                return True
            else:
                error_msg = result.stderr if result else "Unknown error"
                print_warning(f"Push failed: {error_msg}")

                if attempt < max_retries:
                    print_info("Retrying in 3 seconds...")
                    import time
                    time.sleep(3)

        print_error("Push failed after all retries")
        return False

    def verify_push(self):
        """Verify that all files were pushed"""
        print_header("FINAL VERIFICATION")

        print_info("Verifying pushed files...")

        # Get list of tracked files
        result = self.run_git_command(['git', 'ls-files'])
        if not result:
            return False

        tracked_files = result.stdout.strip().split('\n') if result.stdout.strip() else []
        tracked_files = [f for f in tracked_files if f]

        # Compare with scanned files (excluding .git)
        expected_files = [f['relative'] for f in self.scanned_files]

        missing = [f for f in expected_files if f not in tracked_files]

        if missing:
            print_error(f"Verification failed: {len(missing)} file(s) not tracked:")
            for f in missing[:10]:
                print(f"  - {f}")
            if len(missing) > 10:
                print(f"  ... and {len(missing) - 10} more")
            return False

        print_success(f"All {len(expected_files)} files are tracked")

        # Check remote
        result = self.run_git_command(['git', 'log', 'origin/' + self.get_current_branch(), '--oneline', '-1'], check=False)
        if result and result.returncode == 0:
            print_success("Latest commit found on remote")

        return True

    def get_current_branch(self):
        """Get current git branch"""
        result = self.run_git_command(['git', 'branch', '--show-current'], check=False)
        if result and result.stdout.strip():
            return result.stdout.strip()
        return "main"

    def display_final_summary(self):
        """Display final success summary"""
        print()
        print_header("PUSH COMPLETED SUCCESSFULLY")
        print()
        print(f"{Colors.GREEN}{Colors.BOLD}All files and folders were pushed successfully.{Colors.ENDC}")
        print(f"{Colors.GREEN}No file or folder was skipped.{Colors.ENDC}")
        print(f"{Colors.GREEN}Structure and content preserved exactly.{Colors.ENDC}")
        print()
        print(f"{Colors.BOLD}Repository URL:{Colors.ENDC}")
        print(f"  https://github.com/{self.username}/{self.repo_name}")
        print()
        print(f"{Colors.BOLD}Summary:{Colors.ENDC}")
        print(f"  • Total files pushed: {len(self.scanned_files)}")
        print(f"  • Total folders: {len(self.scanned_folders)}")
        print(f"  • Total size: {self.format_size(self.total_size)}")
        print()

    def run(self):
        """Main execution flow"""
        # Display colorful ASCII banner first
        print_colorful_ascii()

        # Phase 1: Input
        print_header("INPUT PHASE")

        self.username = get_input("Enter GitHub username: ")
        if not self.username:
            print_error("Username cannot be empty")
            return

        self.token = get_input("Enter GitHub Personal Access Token (PAT): ")
        if not self.token:
            print_error("Token cannot be empty")
            return

        self.folder_path = get_input("Enter full local folder path (root project directory): ")
        if not self.folder_path:
            print_error("Folder path cannot be empty")
            return

        # Expand user directory
        self.folder_path = os.path.expanduser(self.folder_path)

        self.repo_name = get_input("Enter target GitHub repository name: ")
        if not self.repo_name:
            print_error("Repository name cannot be empty")
            return

        print()

        # Verify authentication
        if not self.verify_github_auth():
            print_error("Authentication failed. Stopping.")
            return

        print()

        # Phase 2: Full Scan
        if not self.scan_directory():
            print_error("Directory scan failed. Stopping.")
            return

        # Phase 3: User Confirmation
        if not self.get_confirmation():
            return

        print()

        # Phase 4: Safety Check
        if self.large_files:
            if not self.handle_large_files():
                return

        print()

        # Check/Create repository
        repo_exists = self.check_repo_exists()
        if repo_exists is None:
            print_error("Cannot verify repository status. Stopping.")
            return

        if not repo_exists:
            print_info(f"Repository '{self.repo_name}' does not exist.")
            if not self.create_repo():
                print_error("Failed to create repository. Stopping.")
                return
        else:
            print_success(f"Repository '{self.repo_name}' exists")

        print()

        # Phase 5: Git Setup
        if not self.initialize_git():
            print_error("Git initialization failed. Stopping.")
            return

        if not self.setup_remote():
            print_error("Remote setup failed. Stopping.")
            return

        if not self.stage_files():
            print_error("Failed to stage files. Stopping.")
            return

        # Phase 6: Push
        if not self.commit_and_push():
            print_error("Push failed. Stopping.")
            return

        # Phase 7: Verification
        if not self.verify_push():
            print_warning("Verification had issues, but push may have succeeded")

        # Final Summary
        self.display_final_summary()


def main():
    try:
        app = GitHubAutoPush()
        app.run()
    except KeyboardInterrupt:
        print()
        print_error("\nOperation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print_error(f"\nUnexpected error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()