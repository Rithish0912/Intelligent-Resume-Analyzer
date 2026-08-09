import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
from file_reader import read_resume
from analyzer import analyze_resumes

class ResumeAnalyzerGUI:
    def __init__(self, root):
        self.root = root
        root.title("Intelligent Resume Analyzer")
        root.geometry("700x600")

        self.jd_path = tk.StringVar()
        self.resume_folder = tk.StringVar()
        self.results = []

        frame_jd = tk.Frame(root)
        frame_jd.pack(pady=10, fill='x', padx=20)
        tk.Label(frame_jd, text="Job Description (JD):").pack(side='left')
        tk.Entry(frame_jd, textvariable=self.jd_path, width=50).pack(side='left', padx=10)
        tk.Button(frame_jd, text="Browse", command=self.select_jd).pack(side='left')

        frame_folder = tk.Frame(root)
        frame_folder.pack(pady=10, fill='x', padx=20)
        tk.Label(frame_folder, text="Resumes Folder:").pack(side='left')
        tk.Entry(frame_folder, textvariable=self.resume_folder, width=50).pack(side='left', padx=10)
        tk.Button(frame_folder, text="Browse", command=self.select_folder).pack(side='left')

        btn_analyze = tk.Button(root, text="Analyze", command=self.analyze, bg='lightblue', font=('Arial', 12))
        btn_analyze.pack(pady=10)

        self.tree = ttk.Treeview(root, columns=('Score',), show='tree headings', height=20)
        self.tree.heading('#0', text='Resume File')
        self.tree.heading('Score', text='Match Score')
        self.tree.column('#0', width=400)
        self.tree.column('Score', width=150, anchor='center')
        self.tree.pack(pady=10, fill='both', expand=True, padx=20)

        btn_save = tk.Button(root, text="Save Results as CSV", command=self.save_results)
        btn_save.pack(pady=5)

    def select_jd(self):
        path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("Word files", "*.docx")])
        if path:
            self.jd_path.set(path)

    def select_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.resume_folder.set(folder)

    def analyze(self):
        jd_file = self.jd_path.get()
        folder = self.resume_folder.get()
        if not jd_file or not folder:
            messagebox.showerror("Error", "Please select both JD and resumes folder.")
            return

        try:
            jd_content = read_resume(jd_file)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read JD: {e}")
            return

        resumes = {}
        for fname in os.listdir(folder):
            if fname.lower().endswith(('.txt', '.docx')):
                full_path = os.path.join(folder, fname)
                try:
                    content = read_resume(full_path)
                    resumes[fname] = content
                except Exception as e:
                    print(f"Warning: Could not read {fname}: {e}")

        if not resumes:
            messagebox.showerror("Error", "No valid resume files found in the folder.")
            return

        results = analyze_resumes(jd_content, resumes)

        for item in self.tree.get_children():
            self.tree.delete(item)

        for fname, score in results:
            self.tree.insert('', 'end', text=fname, values=(f"{score:.4f}",))

        self.results = results
        messagebox.showinfo("Done", f"Analyzed {len(results)} resumes.")

    def save_results(self):
        if not self.results:
            messagebox.showwarning("No results", "Please run analysis first.")
            return
        filepath = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if filepath:
            try:
                import csv
                with open(filepath, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(['Resume File', 'Match Score'])
                    for fname, score in self.results:
                        writer.writerow([fname, f"{score:.4f}"])
                messagebox.showinfo("Saved", f"Results saved to {filepath}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save: {e}")