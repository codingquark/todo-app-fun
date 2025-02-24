# POSIX-Compliant CLI Todo App

A simple command-line interface (CLI) todo application that is POSIX-compliant. This app allows you to manage your tasks efficiently from the terminal.

## Features

- [x] Add tasks with optional tags
- [x] List tasks (with filters for completed/incomplete and tags)
- [x] Delete tasks
- [x] Mark tasks as completed
- [x] Edit task titles and tags
- [x] Search tasks by title or tags
- [x] List all tags used in tasks
- [x] Configurable database location
- [x] Automatic tracking of creation and update dates
- [ ] Notifications (coming soon)

## Storage

Tasks are stored in a local SQLite database. The default location is `~/.todo.db`, but this can be configured. Each task includes:
- Title
- Completion status
- Creation date
- Last update date
- Tags (optional)

## Configuration

The app uses a configuration file located at `~/.todo_config.json`. You can view and modify the configuration using the `config` command:

- View current configuration:
  ```
  ./todo.py config --show
  ```
- Set a configuration value:
  ```
  ./todo.py config --set db_file /path/to/your/database.db
  ```

## Installation

1. Ensure you have Python 3.6+ installed on your system.
2. Clone this repository:
   ```
   git clone https://github.com/yourusername/posix-cli-todo.git
   cd posix-cli-todo
   ```
3. Make the script executable:
   ```
   chmod +x todo.py
   ```
4. (Optional) Create a symlink to run the app from anywhere:
   ```
   sudo ln -s $(pwd)/todo.py /usr/local/bin/todo
   ```

## Usage

Run `./todo.py` (or just `todo` if you created a symlink) followed by a command:

- `add`: Add a new task
- `list`: List tasks
- `delete`: Delete a task
- `complete`: Mark a task as completed
- `edit`: Edit a task's title or tags
- `search`: Search for tasks
- `tags`: List all tags
- `config`: Manage configuration

For detailed help on each command, use:
```
./todo.py <command> --help
```

## Examples

1. Add a task:
   ```
   ./todo.py add "Buy groceries" --tags shopping,food
   ```

2. List all tasks:
   ```
   ./todo.py list
   ```

3. List only incomplete tasks with a specific tag:
   ```
   ./todo.py list --incomplete --tags shopping
   ```

4. Mark a task as completed:
   ```
   ./todo.py complete 1
   ```

5. Edit a task:
   ```
   ./todo.py edit 2 "Buy organic groceries" --tags shopping,organic
   ```

6. Search for tasks:
   ```
   ./todo.py search "groceries"
   ```

7. List all tags:
   ```
   ./todo.py tags
   ```

8. Change the database location:
   ```
   ./todo.py config --set db_file /path/to/your/database.db
   ```
