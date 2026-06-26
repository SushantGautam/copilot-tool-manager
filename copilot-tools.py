#!/usr/bin/env python3
"""
Copilot Tool Manager - Fast enable/disable of Copilot agent tools.

Usage:
  ./copilot-tools.py status                    # Show current state
  ./copilot-tools.py disable browser           # Disable browser tools
  ./copilot-tools.py enable browser            # Enable browser tools
  ./copilot-tools.py disable terminal github   # Disable multiple categories
  ./copilot-tools.py list                      # List all tools with status
  ./copilot-tools.py disable_tool click_element  # Disable a single tool
  ./copilot-tools.py enable_tool click_element   # Enable a single tool

Categories: browser, file_ops, terminal, vscode, chat, github, memory, other
"""
import json, os, sys, sqlite3, platform

# Cross-platform database path
system = platform.system()
if system == "Darwin":
    DB_PATH = os.path.expanduser("~/Library/Application Support/Code/User/globalStorage/state.vscdb")
elif system == "Linux":
    DB_PATH = os.path.expanduser("~/.config/Code/User/globalStorage/state.vscdb")
elif system == "Windows":
    DB_PATH = os.path.expanduser("~/AppData/Roaming/Code/User/globalStorage/state.vscdb")
else:
    print(f"Unsupported OS: {system}")
    sys.exit(1)

CATEGORIES = {
    'browser': ['click_element','drag_element','handle_dialog','hover_element','navigate_page','open_browser_page','read_page','run_playwright_code','screenshot_page','type_in_page'],
    'file_ops': ['copilot_createDirectory','copilot_createFile','copilot_editFiles','copilot_readFile','copilot_viewImage','copilot_searchCodebase','copilot_findFiles','copilot_listDirectory','copilot_findTextInFiles'],
    'terminal': ['get_terminal_output','kill_terminal','run_in_terminal','send_to_terminal','terminal_last_command','terminal_selection'],
    'vscode': ['vscode_renameSymbol','vscode_listCodeUsages','vscode_askQuestions','vscode_searchExtensions_internal','copilot_installExtension','copilot_createNewWorkspace','copilot_runVscodeCommand','copilot_getVSCodeAPI'],
    'chat': ['runSubagent','execution_subagent','manage_todo_list'],
    'github': ['copilot_fetchWebPage','copilot_githubRepo','copilot_githubTextSearch'],
    'memory': ['copilot_memory','copilot_resolveMemoryFileUri'],
    'other': ['copilot_editNotebook','copilot_getErrors'],
}

def get_data():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT value FROM ItemTable WHERE key='chat/selectedTools'")
    row = cur.fetchone()
    if not row:
        print("Error: No tool config found. Have you used Configure Tools UI at least once?")
        sys.exit(1)
    data = json.loads(row[0])
    conn.close()
    return data

def save_data(data):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("UPDATE ItemTable SET value=? WHERE key='chat/selectedTools'", (json.dumps(data),))
    conn.commit()
    conn.close()

def status(data):
    enabled = [k for k,v in data['toolEntries'] if v]
    disabled = [k for k,v in data['toolEntries'] if not v]
    print(f"Enabled: {len(enabled)}, Disabled: {len(disabled)}, Total: {len(data['toolEntries'])}")
    # Show by category
    for cat, tools in CATEGORIES.items():
        cat_enabled = [t for t in tools if any(t == e[0] and e[1] for e in data['toolEntries'])]
        cat_disabled = [t for t in tools if any(t == e[0] and not e[1] for e in data['toolEntries'])]
        if cat_disabled:
            print(f"  {cat}: {len(cat_enabled)} enabled, {len(cat_disabled)} disabled")

def toggle(data, action, *args):
    tools_to_toggle = []
    for arg in args:
        if arg in CATEGORIES:
            tools_to_toggle.extend(CATEGORIES[arg])
        else:
            tools_to_toggle.append(arg)
    
    if not tools_to_toggle:
        print(f"Unknown category or tool: {args}")
        print(f"Available categories: {', '.join(CATEGORIES.keys())}")
        return
    
    for entry in data['toolEntries']:
        if entry[0] in tools_to_toggle:
            entry[1] = (action == 'enable')
    
    save_data(data)
    enabled = [k for k,v in data['toolEntries'] if v]
    disabled = [k for k,v in data['toolEntries'] if not v]
    action_verb = "Enabled" if action == 'enable' else "Disabled"
    print(f"Done. Enabled: {len(enabled)}, Disabled: {len(disabled)}")
    print(f"  {action_verb}: {', '.join(tools_to_toggle)}")

def list_tools(data):
    for cat, tools in CATEGORIES.items():
        print(f"\n{cat.upper()}:")
        for t in tools:
            for entry in data['toolEntries']:
                if entry[0] == t:
                    status_str = "✓ enabled" if entry[1] else "✗ disabled"
                    print(f"  {t}: {status_str}")
                    break

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)
    
    data = get_data()
    cmd = sys.argv[1]
    
    if cmd == 'status':
        status(data)
    elif cmd == 'list':
        list_tools(data)
    elif cmd in ('disable', 'enable'):
        toggle(data, cmd, *sys.argv[2:])
    elif cmd == 'disable_tool':
        toggle(data, 'disable', sys.argv[2])
    elif cmd == 'enable_tool':
        toggle(data, 'enable', sys.argv[2])
    else:
        print(f"Unknown command: {cmd}")
        print(__doc__)
