#!/usr/bin/env python3
import argparse
import os
import readline
import signal
import sys
from typing import Dict, List

class EnvCompleter:
    """Completer class for readline"""
    def __init__(self, keys: List[str]):
        self.keys = keys

    def complete(self, text: str, state: int) -> str:
        if text:
            matches = [key for key in self.keys if key.startswith(text)]
        else:
            matches = self.keys

        try:
            return matches[state]
        except IndexError:
            return None

class EnvManager:
    def __init__(self, env_file: str):
        self.env_file = env_file
        self.env_vars: Dict[str, str] = {}
        self.load_env_vars()
        
        # Setup signal handler for graceful exit
        signal.signal(signal.SIGINT, self.handle_interrupt)
        
        # Setup readline with custom completer
        self.setup_readline()

    def setup_readline(self) -> None:
        """Setup readline with custom completer"""
        if 'libedit' in readline.__doc__:
            # macOS specific
            readline.parse_and_bind("bind ^I rl_complete")
        else:
            # Linux/Unix specific
            readline.parse_and_bind("tab: complete")
        
        # Create and store completer instance to prevent garbage collection
        self.completer = EnvCompleter(list(self.env_vars.keys()))
        readline.set_completer(self.completer.complete)
        # Enable case-insensitive completion
        readline.set_completer_delims(' \t\n=')

    def handle_interrupt(self, signum, frame) -> None:
        """Handle Ctrl+C gracefully"""
        print('\nOperation cancelled. Exiting...')
        sys.exit(0)

    def load_env_vars(self) -> None:
        """Load environment variables from file"""
        self.env_vars.clear()
        try:
            with open(self.env_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        try:
                            key, value = line.split('=', 1)
                            self.env_vars[key.strip()] = value.strip()
                        except ValueError:
                            continue
        except FileNotFoundError:
            print(f"Creating new env file: {self.env_file}")

    def save_env_vars(self) -> None:
        """Save environment variables to file"""
        with open(self.env_file, 'w') as f:
            for key, value in self.env_vars.items():
                f.write(f"{key}={value}\n")

    def list_vars(self) -> None:
        """Display all environment variables"""
        if not self.env_vars:
            print("No environment variables found.")
            return
        
        print("\nCurrent Environment Variables:")
        print("-" * 50)
        for key, value in sorted(self.env_vars.items()):
            print(f"{key} = {value}")
        print("-" * 50)

    def add_var(self) -> None:
        """Add a new environment variable"""
        print("\nPress Tab for suggestions or Ctrl+C to cancel")
        key = input("Enter key: ").strip()
        if not key:
            print("Key cannot be empty!")
            return
        
        if key in self.env_vars:
            print("Key already exists! Use edit option to modify.")
            return
        
        value = input("Enter value: ").strip()
        self.env_vars[key] = value
        self.save_env_vars()
        print(f"Added: {key}={value}")
        
        # Update completer with new key
        self.setup_readline()

    def edit_var(self) -> None:
        """Edit an existing environment variable"""
        self.list_vars()
        print("\nPress Tab for suggestions or Ctrl+C to cancel")
        key = input("Enter key to edit: ").strip()
        
        if key not in self.env_vars:
            print("Key not found!")
            return
        
        current_value = self.env_vars[key]
        print(f"Current value: {current_value}")
        value = input("Enter new value (press Enter to keep current): ").strip()
        
        if not value:
            value = current_value
            print("Keeping current value.")
        
        self.env_vars[key] = value
        self.save_env_vars()
        print(f"Updated: {key}={value}")

    def delete_var(self) -> None:
        """Delete an environment variable"""
        self.list_vars()
        print("\nPress Tab for suggestions or Ctrl+C to cancel")
        key = input("Enter key to delete: ").strip()
        
        if key not in self.env_vars:
            print("Key not found!")
            return
        
        confirm = input(f"Are you sure you want to delete {key}? (y/N): ").strip().lower()
        if confirm == 'y':
            del self.env_vars[key]
            self.save_env_vars()
            print(f"Deleted: {key}")
            # Update completer after deletion
            self.setup_readline()
        else:
            print("Deletion cancelled.")

def main():
    parser = argparse.ArgumentParser(description='CLI Environment Variable Manager')
    parser.add_argument('--file', '-f', default='.env.example',
                      help='Path to env file (default: env-prod)')
    args = parser.parse_args()

    env_manager = EnvManager(args.file)
    
    print("\nTip: Use Ctrl+C to exit at any time")
    print("Tip: Use Tab for key suggestions when editing/deleting")
    
    while True:
        try:
            print("\nEnvironment Variable Manager")
            print("1. List all variables")
            print("2. Add new variable")
            print("3. Edit variable")
            print("4. Delete variable")
            print("5. Exit")
            
            choice = input("\nEnter your choice (1-5): ").strip()
            
            if choice == '1':
                env_manager.list_vars()
            elif choice == '2':
                env_manager.add_var()
            elif choice == '3':
                env_manager.edit_var()
            elif choice == '4':
                env_manager.delete_var()
            elif choice == '5':
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")
        except KeyboardInterrupt:
            print('\nGoodbye!')
            break

if __name__ == "__main__":
    main()
