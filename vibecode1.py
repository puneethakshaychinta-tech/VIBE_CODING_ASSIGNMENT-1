import tkinter as tk
from tkinter import messagebox, ttk
import json
import os
from datetime import datetime

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🚀 Smart To-Do Manager")
        self.root.geometry("1000x700")
        self.root.minsize(800, 600)
        
        # Color scheme
        self.bg_color = "#1e1e2e"
        self.fg_color = "#ffffff"
        self.accent_color = "#00d4ff"
        self.success_color = "#27ae60"
        self.danger_color = "#e74c3c"
        self.frame_color = "#2d2d44"
        
        self.root.configure(bg=self.bg_color)
        
        # Main container
        self.main_container = tk.Frame(self.root, bg=self.bg_color)
        self.main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header
        self.create_header()
        
        # Content area with two columns
        self.content_frame = tk.Frame(self.main_container, bg=self.bg_color)
        self.content_frame.pack(fill="both", expand=True, pady=20)
        
        # Input section
        self.create_input_section()
        
        # Task list section
        self.create_task_section()
        
        # Footer
        self.create_footer()
        
        self.tasks = self.load_tasks()
        self.update_listbox()

    def create_header(self):
        header_frame = tk.Frame(self.main_container, bg=self.bg_color)
        header_frame.pack(fill="x", pady=(0, 20))
        
        title = tk.Label(
            header_frame,
            text="🚀 Smart To-Do Manager",
            font=("Segoe UI", 28, "bold"),
            bg=self.bg_color,
            fg=self.accent_color
        )
        title.pack(anchor="w")
        
        subtitle = tk.Label(
            header_frame,
            text="Organize your tasks efficiently",
            font=("Segoe UI", 11),
            bg=self.bg_color,
            fg="#888888"
        )
        subtitle.pack(anchor="w", pady=(5, 0))

    def create_input_section(self):
        input_frame = tk.Frame(self.content_frame, bg=self.frame_color, relief="flat", bd=0)
        input_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        # Add padding
        padding_frame = tk.Frame(input_frame, bg=self.frame_color)
        padding_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        tk.Label(
            padding_frame,
            text="✨ Add New Task",
            font=("Segoe UI", 14, "bold"),
            bg=self.frame_color,
            fg=self.accent_color
        ).pack(anchor="w", pady=(0, 15))
        
        self.task_entry = tk.Entry(
            padding_frame,
            font=("Segoe UI", 12),
            bg="#3d3d54",
            fg=self.fg_color,
            relief="flat",
            bd=0,
            insertbackground=self.accent_color
        )
        self.task_entry.pack(fill="x", pady=(0, 10), ipady=10)
        self.task_entry.bind("<Return>", lambda e: self.add_task())
        
        # Buttons
        btn_frame = tk.Frame(padding_frame, bg=self.frame_color)
        btn_frame.pack(fill="x", pady=10)
        
        add_btn = tk.Button(
            btn_frame,
            text="➕ Add Task",
            command=self.add_task,
            bg=self.success_color,
            fg=self.fg_color,
            relief="flat",
            bd=0,
            font=("Segoe UI", 11, "bold"),
            cursor="hand2",
            padx=20,
            pady=10
        )
        add_btn.pack(side="left", padx=(0, 10))
        
        clear_btn = tk.Button(
            btn_frame,
            text="🗑️ Clear All",
            command=self.clear_all,
            bg=self.danger_color,
            fg=self.fg_color,
            relief="flat",
            bd=0,
            font=("Segoe UI", 11, "bold"),
            cursor="hand2",
            padx=20,
            pady=10
        )
        clear_btn.pack(side="left")

    def create_task_section(self):
        task_frame = tk.Frame(self.content_frame, bg=self.frame_color, relief="flat", bd=0)
        task_frame.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        # Padding frame
        padding_frame = tk.Frame(task_frame, bg=self.frame_color)
        padding_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        tk.Label(
            padding_frame,
            text="📋 Your Tasks",
            font=("Segoe UI", 14, "bold"),
            bg=self.frame_color,
            fg=self.accent_color
        ).pack(anchor="w", pady=(0, 15))
        
        # Listbox with scrollbar
        list_container = tk.Frame(padding_frame, bg=self.frame_color)
        list_container.pack(fill="both", expand=True, pady=(0, 10))
        
        self.listbox = tk.Listbox(
            list_container,
            font=("Segoe UI", 11),
            bg="#3d3d54",
            fg=self.fg_color,
            relief="flat",
            bd=0,
            highlightthickness=0,
            selectmode="single",
            activestyle="none"
        )
        self.listbox.pack(side="left", fill="both", expand=True)
        
        scrollbar = tk.Scrollbar(list_container, command=self.listbox.yview, bg=self.frame_color, troughcolor=self.frame_color)
        scrollbar.pack(side="right", fill="y", padx=(5, 0))
        self.listbox.config(yscrollcommand=scrollbar.set)
        
        # Delete section
        delete_frame = tk.Frame(padding_frame, bg=self.frame_color)
        delete_frame.pack(fill="x")
        
        tk.Label(
            delete_frame,
            text="Delete Task (by number):",
            font=("Segoe UI", 10),
            bg=self.frame_color,
            fg="#aaaaaa"
        ).pack(anchor="w", pady=(0, 5))
        
        delete_input_frame = tk.Frame(delete_frame, bg=self.frame_color)
        delete_input_frame.pack(fill="x")
        
        self.delete_entry = tk.Entry(
            delete_input_frame,
            font=("Segoe UI", 11),
            bg="#3d3d54",
            fg=self.fg_color,
            relief="flat",
            bd=0,
            width=8,
            insertbackground=self.accent_color
        )
        self.delete_entry.pack(side="left", padx=(0, 10), ipady=8)
        
        delete_btn = tk.Button(
            delete_input_frame,
            text="❌ Delete",
            command=self.delete_task,
            bg=self.danger_color,
            fg=self.fg_color,
            relief="flat",
            bd=0,
            font=("Segoe UI", 10, "bold"),
            cursor="hand2",
            padx=15,
            pady=8
        )
        delete_btn.pack(side="left")

    def create_footer(self):
        footer_frame = tk.Frame(self.main_container, bg=self.bg_color)
        footer_frame.pack(fill="x", pady=(20, 0))
        
        separator = tk.Label(
            footer_frame,
            text="─" * 80,
            bg=self.bg_color,
            fg="#444444"
        )
        separator.pack()
        
        info_frame = tk.Frame(footer_frame, bg=self.bg_color)
        info_frame.pack(fill="x", pady=(10, 0))
        
        self.task_count_label = tk.Label(
            info_frame,
            text="",
            font=("Segoe UI", 10),
            bg=self.bg_color,
            fg="#888888"
        )
        self.task_count_label.pack(anchor="w")

    def add_task(self):
        task = self.task_entry.get().strip()
        if not task:
            messagebox.showerror("Error", "Please enter a task!")
            self.task_entry.focus()
            return
        self.tasks.append({"text": task, "created": datetime.now().strftime("%Y-%m-%d %H:%M")})
        self.update_listbox()
        self.task_entry.delete(0, tk.END)
        self.task_entry.focus()
        self.save_tasks()

    def delete_task(self):
        try:
            idx = int(self.delete_entry.get().strip()) - 1
            if 0 <= idx < len(self.tasks):
                del self.tasks[idx]
                self.update_listbox()
                self.delete_entry.delete(0, tk.END)
                self.save_tasks()
            else:
                messagebox.showerror("Error", "Invalid task number!")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number!")

    def clear_all(self):
        if messagebox.askyesno("Confirm", "Delete all tasks? This cannot be undone."):
            self.tasks = []
            self.update_listbox()
            self.save_tasks()

    def update_listbox(self):
        self.listbox.delete(0, tk.END)
        for i, task in enumerate(self.tasks):
            task_text = task["text"] if isinstance(task, dict) else task
            self.listbox.insert(tk.END, f"  {i+1}. {task_text}")
        
        # Update task count
        count = len(self.tasks)
        self.task_count_label.config(text=f"Total Tasks: {count} | Last updated: {datetime.now().strftime('%H:%M:%S')}")

    def save_tasks(self):
        with open("tasks.json", "w") as f:
            json.dump(self.tasks, f, indent=2)

    def load_tasks(self):
        if os.path.exists("tasks.json"):
            try:
                with open("tasks.json", "r") as f:
                    return json.load(f)
            except:
                return []
        return []

if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()