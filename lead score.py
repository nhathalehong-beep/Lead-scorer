import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox

class LeadScorer:
    def __init__(self):
        self.required_fields = [
            'Contact name',
            'Company name',
            'Email',
            'Phone',
            'Personal ID',
            'Business License'
        ]
        
    def calculate_score(self, data):
        score = 0
        missing_fields = []
        
        for field in self.required_fields[:-1]:  # Excluding Business License
            if pd.notna(data.get(field)):
                score += 1
            else:
                missing_fields.append(field)
        
        # Special handling for Business License
        if data.get('Company Type') == 'Company' and pd.notna(data.get('Business License')):
            score += 1
        elif data.get('Company Type') == 'Company' and pd.isna(data.get('Business License')):
            missing_fields.append('Business License')
            
        return score, missing_fields

class LeadScorerApp:
    def __init__(self):
        self.scorer = LeadScorer()
        self.window = tk.Tk()
        self.window.title("Lead Scorer")
        self.create_widgets()
        
    def create_widgets(self):
        # Input fields
        tk.Label(self.window, text="Contact Name*:").grid(row=0, column=0)
        self.contact_name = tk.Entry(self.window)
        self.contact_name.grid(row=0, column=1)
        
        tk.Label(self.window, text="Company Name*:").grid(row=1, column=0)
        self.company_name = tk.Entry(self.window)
        self.company_name.grid(row=1, column=1)
        
        tk.Label(self.window, text="Email*:").grid(row=2, column=0)
        self.email = tk.Entry(self.window)
        self.email.grid(row=2, column=1)
        
        tk.Label(self.window, text="Phone*:").grid(row=3, column=0)
        self.phone = tk.Entry(self.window)
        self.phone.grid(row=3, column=1)
        
        tk.Label(self.window, text="Personal ID*:").grid(row=4, column=0)
        self.personal_id = tk.Entry(self.window)
        self.personal_id.grid(row=4, column=1)
        
        tk.Label(self.window, text="Company Type:").grid(row=5, column=0)
        self.company_type = tk.StringVar(value="Individual")
        tk.Radiobutton(self.window, text="Individual", variable=self.company_type, 
                      value="Individual").grid(row=5, column=1)
        tk.Radiobutton(self.window, text="Company", variable=self.company_type, 
                      value="Company").grid(row=5, column=2)
        
        tk.Label(self.window, text="Business License:").grid(row=6, column=0)
        self.business_license = tk.Entry(self.window)
        self.business_license.grid(row=6, column=1)
        
        # Buttons
        tk.Button(self.window, text="Calculate Score", 
                 command=self.calculate_manual_score).grid(row=7, column=0)
        tk.Button(self.window, text="Upload File", 
                 command=self.upload_file).grid(row=7, column=1)
        
    def calculate_manual_score(self):
        data = {
            'Contact name': self.contact_name.get(),
            'Company name': self.company_name.get(),
            'Email': self.email.get(),
            'Phone': self.phone.get(),
            'Personal ID': self.personal_id.get(),
            'Business License': self.business_license.get(),
            'Company Type': self.company_type.get()
        }
        
        score, missing_fields = self.scorer.calculate_score(data)
        self.show_result(score, missing_fields)
        
    def upload_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Excel files", "*.xlsx *.xls"), ("CSV files", "*.csv")])
        if file_path:
            if file_path.endswith('.csv'):
                df = pd.read_csv(file_path)
            else:
                df = pd.read_excel(file_path)
            
            results = []
            for _, row in df.iterrows():
                score, missing = self.scorer.calculate_score(row)
                results.append(f"Score: {score}/6, Missing: {', '.join(missing) if missing else 'None'}")
            
            self.show_file_results(results)
    
    def show_result(self, score, missing_fields):
        message = f"Lead Score: {score}/6\n"
        if missing_fields:
            message += f"Missing fields: {', '.join(missing_fields)}"
        messagebox.showinfo("Result", message)
    
    def show_file_results(self, results):
        result_window = tk.Toplevel(self.window)
        result_window.title("File Results")
        
        for i, result in enumerate(results):
            tk.Label(result_window, text=f"Record {i+1}: {result}").pack()
    
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = LeadScorerApp()
    app.run()