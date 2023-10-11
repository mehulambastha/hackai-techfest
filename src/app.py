# SET-UP the UI
from async_tkinter_loop import async_handler, async_mainloop
import tkinter as tk

tkinter_inputs = {}

@async_handler
async def capture_inputs():
    print("City: %s\nState: %s\nCountry: %s\nMinimum Temperature: %s\nMaximum Temperature: %s" % (e1.get(), e2.get(), e3.get(), e4.get(), e5.get()))
    tkinter_inputs["city"] = e1.get().lower()
    tkinter_inputs["state"] = e2.get().lower()
    tkinter_inputs["country"] = e3.get().lower()
    tkinter_inputs["min_temp"] = e4.get()
    tkinter_inputs["max_temp"] = e5.get()
    root.destroy()


def create_tkinter_app():
    global root, e1, e2, e3, e4, e5
    root = tk.Tk()
    root.title("Temperature Monitoring System")
    tk.Label(root, text="City").grid(row=0)
    tk.Label(root, text="State").grid(row=1)
    tk.Label(root, text="Country").grid(row=2)
    tk.Label(root, text="Minimum Temperature").grid(row=3)
    tk.Label(root, text="Maximimum Temperature").grid(row=4)

    e1 = tk.Entry(root)
    e2 = tk.Entry(root)
    e3 = tk.Entry(root)
    e4 = tk.Entry(root)
    e5 = tk.Entry(root)

    e1.grid(row=0, column=1)
    e2.grid(row=1, column=1)
    e3.grid(row=2, column=1)
    e4.grid(row=3, column=1)
    e5.grid(row=4, column=1)

    tk.Button(root, text='Save and exit', command=capture_inputs).grid(row=5, column=1, sticky=tk.W, pady=4)

    async_mainloop(root)
    
def get_tkinter_inputs():
    return tkinter_inputs