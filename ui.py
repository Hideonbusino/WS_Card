from run import *
import tkinter as tk
from tkinter import simpledialog
def gui_add_multiple_cards():
    dialog = tk.Toplevel(root)
    dialog.title("Enter start and end")
    tk.Label(dialog, text="Start:").grid(row=0, column=0)
    x_entry = tk.Entry(dialog)
    x_entry.grid(row=0, column=1)
    
    tk.Label(dialog, text="End:").grid(row=1, column=0)
    y_entry = tk.Entry(dialog)
    y_entry.grid(row=1, column=1)    
    def on_ok(event=None):
        x = int(x_entry.get())
        y = int(y_entry.get())
        dialog.destroy()
        collect_all(x, y)
        output_text.insert(tk.END, f"Finished adding card(s) from {x} to {y}\n")
    tk.Button(dialog, text="OK", command=on_ok).grid(row=2, columnspan=2)
    dialog.bind('<Return>', on_ok)

def gui_add_one_card():
    dialog = tk.Toplevel(root)
    dialog.title("Enter id and grade")
    tk.Label(dialog, text="ID:").grid(row=0, column=0)
    x_entry = tk.Entry(dialog)
    x_entry.grid(row=0, column=1)
    tk.Label(dialog, text="Grade:").grid(row=1, column=0)
    y_entry = tk.Entry(dialog)
    y_entry.grid(row=1, column=1)    
    def on_ok(event=None):
        x = x_entry.get()
        y = y_entry.get()
        dialog.destroy()
        output_text.insert(tk.END, f"Adding Card {x}......\n")
        info = add_ind_data(x, y)
        output_text.insert(tk.END, f"Finished adding card: {info}\n")
    tk.Button(dialog, text="OK", command=on_ok).grid(row=2, columnspan=2)   
    dialog.bind('<Return>', on_ok)

def gui_remove_row():
    x = simpledialog.askstring("Input", "Enter the id of the card to be removed:")
    if x == None:
        return
    remove_row(x)
    output_text.insert(tk.END, "Finished removing row\n")

'''def gui_remove_database():
    remove_all()
    output_text.insert(tk.END, "Finished removing database\n")'''

def gui_end_program():
    output_text.insert(tk.END, "Ending program\n")
    root.quit()

if __name__ == '__main__':
    root = tk.Tk()
    root.title("Card Management")
    
    # Create buttons with increased width and height
    button1 = tk.Button(root, text="Add Multiple Cards", command=gui_add_multiple_cards, width=20, height=2, font=("Arial", 14))
    button2 = tk.Button(root, text="Add One Card", command=gui_add_one_card, width=20, height=2, font=("Arial", 14))
    button3 = tk.Button(root, text="Remove Row", command=gui_remove_row, width=20, height=2, font=("Arial", 14))
    button5 = tk.Button(root, text="End", command=gui_end_program, width=20, height=2, font=("Arial", 14))
    # Create a text box for output with increased width and height
    output_text = tk.Text(root, wrap=tk.WORD, width=60, height=20, font=("Arial", 14))

    # Place buttons and text box on the window
    button1.pack(pady=10)  # Added padding for better spacing
    button2.pack(pady=10)
    button3.pack(pady=10)
    button5.pack(pady=10)
    output_text.pack(pady=20)


    # Start the Tkinter event loop
    root.mainloop()
