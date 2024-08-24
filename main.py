import tkinter as tk
from tkinter import filedialog, messagebox
from pypdf import PdfReader, PdfWriter

def split_pdf(input_file, start_page, end_page, output_file):
    reader = PdfReader(input_file)
    writer = PdfWriter()
    
    # Ensure valid page range
    if start_page < 0 or end_page >= len(reader.pages) or start_page > end_page:
        raise ValueError("Invalid page range")

    # Add pages to the writer
    for i in range(start_page, end_page + 1):
        writer.add_page(reader.pages[i])
    
    # Write the output PDF
    with open(output_file, "wb") as output_pdf:
        writer.write(output_pdf)

def upload_file():
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if file_path:
        pdf_file_path.set(file_path)

def save_as_file():
    file_path = filedialog.asksaveasfilename(
        defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
    return file_path

def split_pdf_action():
    input_file = pdf_file_path.get()
    if not input_file:
        messagebox.showerror("Error", "Please upload a PDF file")
        return

    try:
        start_page = int(start_page_entry.get()) - 1
        end_page = int(end_page_entry.get()) - 1
        
        output_file = save_as_file()
        if output_file:
            split_pdf(input_file, start_page, end_page, output_file)
            messagebox.showinfo("Success", f"PDF saved to {output_file}")
        else:
            messagebox.showerror("Error", "Output file path not specified.")

    except ValueError as ve:
        messagebox.showerror("Error", str(ve))
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Tkinter setup
root = tk.Tk()
root.title("PDF Splitter")

# Create a canvas for the gradient background
canvas = tk.Canvas(root, width=400, height=400)
canvas.pack(fill="both", expand=True)

# Draw a gradient background
def draw_gradient(canvas):
    width = canvas.winfo_width()
    height = canvas.winfo_height()
    
    for i in range(height):
        color = '#{:02x}{:02x}{:02x}'.format(0, int(255 * (1 - i / height)), 255)
        canvas.create_line(0, i, width, i, fill=color, width=1)

draw_gradient(canvas)

# Frame setup for better layout
frame = tk.Frame(root, bg="#ffffff", padx=20, pady=20)
frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.9, relheight=0.8)

# PDF file path variable
pdf_file_path = tk.StringVar()

# Widgets
upload_button = tk.Button(frame, text="Upload PDF", command=upload_file, font=("Helvetica", 12, "bold"), bg="#4CAF50", fg="white")
upload_button.grid(row=0, column=0, pady=10, columnspan=2, sticky="ew")

file_label = tk.Label(frame, textvariable=pdf_file_path, wraplength=300, font=("Helvetica", 10), bg="#ffffff")
file_label.grid(row=1, column=0, pady=5, columnspan=2, sticky="w")

tk.Label(frame, text="Start Page:", font=("Helvetica", 10), bg="#ffffff").grid(row=2, column=0, pady=5, sticky="w")
start_page_entry = tk.Entry(frame, font=("Helvetica", 10))
start_page_entry.grid(row=2, column=1, pady=5, sticky="ew")

tk.Label(frame, text="End Page:", font=("Helvetica", 10), bg="#ffffff").grid(row=3, column=0, pady=5, sticky="w")
end_page_entry = tk.Entry(frame, font=("Helvetica", 10))
end_page_entry.grid(row=3, column=1, pady=5, sticky="ew")

split_button = tk.Button(frame, text="Split PDF", command=split_pdf_action, font=("Helvetica", 12, "bold"), bg="#2196F3", fg="white")
split_button.grid(row=4, column=0, columnspan=2, pady=20)

# Main loop
root.mainloop()
