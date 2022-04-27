import tkinter as tk
import tkinter_dndr
import file_worker

VERSION = "1.0.0"

blocks = {} # tkinter ui object: {data}



def spawn_obj(type=0):
    global blocks
    if type == 0:
        print("Spawn block motors")
        button = tk.Button(text="Motors\nType: None\nData:None\nDirection:None", bd=0, bg="lightblue")
        blocks[button] = {"action": type,
                                        "type": None,
                                        "steps_cnt": None,
                                        "direction": None, 
                                        "comment": None}
        button.bind("<Button-3>", lambda _, block_ui=button: configure_block(0, block_ui))
        button.grid(row=3, column=0)
        dndr_button = tkinter_dndr.DragDropResizeWidget(button)
        dndr_button.make_draggable() 
        button.bind('<Double-Button-1>', lambda x=0: spawn_obj(0))
    elif type == 1:
        print("Spawn block servo") #Not fully supported yet
        button = tk.Button(text="Servos\nType: None\nData:None", bd=0, bg="#FF3632")
        blocks[button] = {"action": type,
                                        "type": None,
                                        "steps_cnt": None,
                                        "comment": None}
        button.bind("<Button-3>", lambda _, block_ui=button: configure_block(1, block_ui))
        button.grid(row=3, column=1)
        dndr_button = tkinter_dndr.DragDropResizeWidget(button)
        dndr_button.make_draggable() 
        button.bind('<Double-Button-1>', lambda x=1: spawn_obj(1))


        

        

def save(block_ui, type_action, type_data, direction_data, comment_entry):
    global blocks
    block_ui["text"] = f"Motors\nType: {type_action}\nData:{type_data.get()}\nDirection:{direction_data.get()[0]}"
    blocks[block_ui] = {"action": 0,
                                        "type": type_action,
                                        "steps_cnt": type_data.get(),
                                        "direction": direction_data.get()[0], 
                                        "comment": comment_entry.get("1.0",tk.END)}
    print(blocks[block_ui] )

def configure_block(block_type, block_ui):
    global blocks
    if block_type == 0:
        configure_window = tk.Toplevel(root)
        configure_window.title("Configure block")
        configure_window.geometry("500x300")
        tk.Label(configure_window, text="Counter type:", font="Arial 13 bold").pack()
        
        options = [
            "Steps count",
            "Future"
        ]
        directions_options = [
            "↑ Forward",
            "←Left",
            "→ Right",
            "↓ Backward"
        ]
        choose_var = tk.StringVar(configure_window, value=options[0])
        counter_type_chooser = tk.OptionMenu(configure_window, choose_var, *options)
        counter_type_chooser.pack()
        tk.Label(configure_window, text="Steps count", font="Arial 13 bold").pack()
        saved_data_var = ""
        if block_ui in blocks:
            saved_data_var = blocks[block_ui]["steps_cnt"]
        data_var = tk.StringVar(value=saved_data_var)
        
        action_data = tk.Entry(configure_window, textvariable=data_var)
        action_data.pack()

        tk.Label(configure_window, text="Direction", font="Arial 13 bold").pack()
        choose_direction_var = tk.StringVar(configure_window, value=directions_options[0])
        direction_chooser = tk.OptionMenu(configure_window, choose_direction_var, *directions_options)
        direction_chooser.pack()

        tk.Label(configure_window, text="Comment", font="Arial 13 bold").pack()
        comment_entry = tk.Text(configure_window, width=40, height=5)
        comment_entry.pack()
        if block_ui in blocks and blocks[block_ui]["comment"]:
            comment_entry.insert(tk.END, blocks[block_ui]["comment"])

        
        save_btn = tk.Button(configure_window, text="Save", command=lambda a=block_ui, b=options.index(choose_var.get()), c=data_var, d=choose_direction_var, e = comment_entry: save(a, b, c, d, e))
        save_btn.pack()

root = tk.Tk()
mainmenu = tk.Menu(root)
root.config(menu=mainmenu) 
filemenu = tk.Menu(mainmenu, tearoff=0)
filemenu.add_command(label="Open project", command=lambda prj = "projects/20220427-191902/", root=root: file_worker.read_project(prj, root))
filemenu.add_command(label="New project")
filemenu.add_command(label="Save project", command=lambda data=blocks: file_worker.write_project(data))
filemenu.add_command(label="Exit")

sourcemenu = tk.Menu(mainmenu, tearoff=0)
sourcemenu.add_command(label="Compile to JSON", command=lambda blocks=blocks: file_worker.write(blocks))
sourcemenu.add_command(label="Run on RPI")

mainmenu.add_cascade(label="File",
                     menu=filemenu)

mainmenu.add_cascade(label="Source",
                     menu=sourcemenu)



root.geometry("800x400")
root.title(f"Robo Scratch {VERSION}")
action_line_title = tk.Label(text="Actions chain", font="Arial 16 bold").grid(column=0, row=0)
action_chain_objects_frame = tk.Frame(height=200)
action_chain_objects_frame.grid(row=1)
avaliable_obj_title = tk.Label(text="Available actions", font="Arial 16 bold").grid(row=1)
spawn_obj()
#spawn_obj(1)
root.mainloop()