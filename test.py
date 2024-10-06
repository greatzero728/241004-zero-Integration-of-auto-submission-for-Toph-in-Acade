import tkinter as tk
from tkinter import scrolledtext
import autoSubmitToToph

def submit_code():
    problem_id = problem_id_entry.get()
    code = code_text.get("1.0", "end-1c")
    
    if not problem_id or not code.strip():
        result_label.config(text="Please fill out all fields.")
        return
    
    submission_id = autoSubmitToToph.submit(problem_id, code)
    
    if submission_id:
        submission_id_var.set(str(submission_id))
        result_label.config(text=f"Code submitted successfully! Submission ID: {submission_id}\n\n\n")
    else:
        result_label.config(text="Submission failed.")

def get_submission_status():
    submission_id = submission_id_var.get()
    
    if not submission_id.strip():
        result_label.config(text="Please enter a submission ID.")
        return
    
    status = autoSubmitToToph.get_status(submission_id)
    
    if status:
        result_label.config(text=f"Submission Status: {status}\n\n\n")
    else:
        result_label.config(text="Failed to retrieve submission status.")

# Initialize the login process (once when the GUI starts)
if autoSubmitToToph.login(autoSubmitToToph.TOPH_USERNAME, autoSubmitToToph.TOPH_PASSWORD):
    print("Logged in successfully!")
else:
    print("Login failed. Please check credentials.")

# Create the GUI
root = tk.Tk()
root.title("Toph Code Submitter")

# Problem ID label and entry
tk.Label(root, text="Problem ID:").grid(row=0, column=0, padx=10, pady=10)
problem_id_entry = tk.Entry(root)
problem_id_entry.grid(row=0, column=1, padx=10, pady=10)

# Code label and scrolled text box
tk.Label(root, text="Code:").grid(row=1, column=0, padx=10, pady=10)
code_text = scrolledtext.ScrolledText(root, height=10, width=50)
code_text.grid(row=1, column=1, padx=10, pady=10)

# Submit button
submit_button = tk.Button(root, text="Submit", command=submit_code)
submit_button.grid(row=2, column=1, padx=10, pady=10)

# Submission ID label and entry (output of the submit function)
tk.Label(root, text="Submission ID:").grid(row=3, column=0, padx=10, pady=10)
submission_id_var = tk.StringVar()
submission_id_entry = tk.Entry(root, textvariable=submission_id_var)
submission_id_entry.grid(row=3, column=1, padx=10, pady=10)

# Get Status button
get_status_button = tk.Button(root, text="Get Result", command=get_submission_status)
get_status_button.grid(row=4, column=1, padx=10, pady=10)

# Result label (displays success or error messages)
result_label = tk.Label(root, text="")
result_label.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

# Start the GUI event loop
root.mainloop()
