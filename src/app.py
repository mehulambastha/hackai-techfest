# SET-UP the UI
from async_tkinter_loop import async_handler, async_mainloop
import tkinter as tk

# initialise the empty object for storing user data
tkinter_inputs = {}

# using async handler for the tkinter app
'''
    Function: capture_inputs
    Arguments: None
    returns: none
    
    functionality:
        - Runs when "Save and exit" button is clicked.
        - Captures the city, state, country, maximum temperature and minimum temperature from the input fields in tkinter window
        - saves the above mentioned data into the tkinter_inputs object as key, value. Keys being city, state, country, min_temp and max_temp
        - quits the window and move on to agent functionalities
'''
@async_handler
async def capture_inputs():
    print("City: %s\nState: %s\nCountry: %s\nMinimum Temperature: %s\nMaximum Temperature: %s" % (e1.get(), e2.get(), e3.get(), e4.get(), e5.get()))
    tkinter_inputs["city"] = e1.get().lower()
    tkinter_inputs["state"] = e2.get().lower()
    tkinter_inputs["country"] = e3.get().lower()
    tkinter_inputs["min_temp"] = e4.get()
    tkinter_inputs["max_temp"] = e5.get()
    root.destroy()

'''
    Function: create_tkinter_app
    Arguments: None
    Returns: None
    
    functionalities:
        - called from the user.py file in agents folder
        - used to create the tkinter window along with input fields , their labels and save and exit button
'''
def create_tkinter_app():
    # define them globally so that they can be used in the capture_input function also
    global root, e1, e2, e3, e4, e5
    
    # define the root tkinter window
    root = tk.Tk()
    root.title("Temperature Monitoring System")
    
    # Define the five labels for input fields
    tk.Label(root, text="City").grid(row=0)
    tk.Label(root, text="State").grid(row=1)
    tk.Label(root, text="Country").grid(row=2)
    tk.Label(root, text="Minimum Temperature").grid(row=3)
    tk.Label(root, text="Maximimum Temperature").grid(row=4)

    # Accepting single line inputs for the five fields and storing them in e1, e2, e3, e4, e5 input fields
    e1 = tk.Entry(root)
    e2 = tk.Entry(root)
    e3 = tk.Entry(root)
    e4 = tk.Entry(root)
    e5 = tk.Entry(root)

    # Positioning of the input fields according to the default grid positioning system in Tkinter
    e1.grid(row=0, column=1)
    e2.grid(row=1, column=1)
    e3.grid(row=2, column=1)
    e4.grid(row=3, column=1)
    e5.grid(row=4, column=1)

    # Save and exit button
    # "command" defines the on-click logic o the button. In this case it calls the capture_inputs function
    tk.Button(root, text='Save and exit', command=capture_inputs).grid(row=5, column=1, sticky=tk.W, pady=4)

    # Finally render and run the tkinter window
    async_mainloop(root)
   
   
   
'''
    Function: get_tkinter_inputs
    Argmuments: None,
    Returns: tkinter_inputs <type: Object>
    
    functionality:
        - called from the user.py file in agents folder
        - returns the user inputs packed in an object for further operations
''' 
def get_tkinter_inputs():
    return tkinter_inputs