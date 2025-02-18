# Env File Manager

A simple command-line tool for managing environment variables in .env files. This tool provides an interactive CLI interface to create, read, update, and delete environment variables in your .env files.

## Features

- 🔄 Interactive CLI menu interface
- ⌨️ Tab completion for existing environment variables
- 🔍 View all environment variables in a formatted display
- ➕ Add new environment variables
- ✏️ Edit existing variables
- 🗑️ Delete variables with confirmation
- 🔄 Auto-saves changes to file
- ⚡ Keyboard shortcut (Ctrl+C) for quick exit
- 📁 Support for custom env file paths

## Installation

1. Clone the repository:
```bash
git clone https://github.com/RonLi-io/env-manager.git
cd env-manager
```

2. Make the script executable:
```bash
chmod +x env_manager.py
```

3. Dependencies:
The script uses Python's built-in libraries, so no additional installation is required.

## Usage

### Basic Usage
```bash
./env_manager.py
```
This will manage variables in the default `.env.example` file in the current directory.

### File Options
The tool provides flexibility in choosing which environment file to manage:

```bash
# Default usage (manages 'env-prod' in current directory)
./env_manager.py

# Using -f or --file to specify a different file
./env_manager.py -f .env.production
./env_manager.py --file /path/to/your/.env

# Examples
./env_manager.py -f .env.staging     # Manage staging environment
./env_manager.py -f .env.local       # Manage local environment
./env_manager.py -f configs/.env     # Manage env file in different directory
```

If the specified file doesn't exist, the tool will create it automatically when you add your first variable.

### Interactive Menu Options
1. List all variables
2. Add new variable
3. Edit variable
4. Delete variable
5. Exit

### Keyboard Shortcuts
- `Ctrl+C`: Exit the program at any time
- `Tab`: Auto-complete existing variable names when editing/deleting

## Dependencies

- Python 3.6+
- readline (usually comes with Python, but might need installation on some systems)

### Installing readline (if needed)

#### Ubuntu/Debian:
```bash
sudo apt-get install libreadline-dev
```

#### RHEL/CentOS:
```bash
sudo yum install readline-devel
```

#### macOS:
```bash
brew install readline
```

## Contributing

Feel free to open issues or submit pull requests if you have suggestions for improvements.

## License

[MIT License](LICENSE)