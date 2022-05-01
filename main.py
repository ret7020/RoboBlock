import tkinter as tk
import tkinter_dndr
import file_worker
from tkinter import filedialog
from idlelib.tooltip import Hovertip
import time
import os
from pathlib import Path
import interpreter.arduino_converter as ardconvert

VERSION = "1.0.0 [dev]"
DARKTHEME = True

class Logger():
    def __init__(self, log_level=1):
        Path("logs").mkdir(parents=True, exist_ok=True)
        self.logger_path = f"logs/{time.strftime('%Y%m%d-%H%M%S')}.log"
        open(self.logger_path, "w").close()
        self.write(f"App {VERSION} started!")
    def write(self, data):
        with open(self.logger_path, "a") as file:
            file.write(f"[LOG] {time.strftime('%Y-%m-%d-%H:%M:%S')} {data}\n")



class App():
    def __init__(self, master):
        self.root = master
        self.root.geometry("800x400")
        if DARKTHEME:
            self.root.configure(background='#121212')
        self.root.title(f"RoboBlock {VERSION}")
        self.blocks = {}
        self.project_settings = {
            "name": time.strftime('%Y%m%d-%H%M%S')
        }

        self.draw_ui()
        self.spawn_obj()

    def draw_ui(self):
        mainmenu = tk.Menu(self.root)
        
        self.root.config(menu=mainmenu)
        filemenu = tk.Menu(mainmenu, tearoff=0)
        filemenu.add_command(label="Open project",
                             command=self.project_select_dialog)
        filemenu.add_command(label="New project")
        filemenu.add_command(label="Save project",
                             command=self.project_save_dir_dialog)
        filemenu.add_command(label="Exit")

        sourcemenu = tk.Menu(mainmenu, tearoff=0)
        sourcemenu.add_command(label="Compile to JSON",
                               command=lambda blocks=self.blocks: file_worker.write(blocks))
        sourcemenu.add_command(label="Compile to Arduino array",
                               command=lambda blocks=self.blocks: print(ardconvert.convert(data=blocks)))
        sourcemenu.add_command(label="Run on RPI")
        sourcemenu.add_command(label="Step by step evalution")
        sourcemenu.add_command(label="Change start step")

        projectmenu = tk.Menu(mainmenu, tearoff=0)
        projectmenu.add_command(label="Settings")

        mainmenu.add_cascade(label="File",
                             menu=filemenu)

        mainmenu.add_cascade(label="Project",
                             menu=projectmenu)

        mainmenu.add_cascade(label="Source",
                             menu=sourcemenu)

        

        action_line_title = tk.Label(self.root,
                                     text="Actions chain", font="Arial 16 bold")
        action_line_title.grid(column=0, row=0)
        action_chain_objects_frame = tk.Frame(self.root, height=200, bd=0)
        action_chain_objects_frame.grid(row=1)
        avaliable_obj_title = tk.Label(self.root, 
            text="Available actions", font="Arial 16 bold")
        avaliable_obj_title.grid(row=1)

        physical_actions_title = tk.Label(self.root, 
            text="Physical actions", font="Arial 14 bold", fg="blue")
        physical_actions_title.place(x=6, y=180)

        struct_actions_title = tk.Label(self.root, 
            text="Structs", font="Arial 14 bold", fg="red")
        struct_actions_title.place(x=300, y=180)

        math_actions_title = tk.Label(self.root, 
            text="Maths", font="Arial 14 bold", fg="orange")
        math_actions_title.place(x=550, y=180)

        if DARKTHEME:
            mainmenu.configure(background='#121212', foreground='white')
            filemenu.configure(background='#121212', foreground='white')
            sourcemenu.configure(background='#121212', foreground='white')
            projectmenu.configure(background='#121212', foreground='white')
            action_line_title.configure(background='#121212', foreground='white')
            action_chain_objects_frame.configure(background="#121212")
            avaliable_obj_title.configure(background='#121212', foreground='white')
            physical_actions_title.configure(background='#121212')
            struct_actions_title.configure(background='#121212')
            math_actions_title.configure(background='#121212')
            
    def project_select_dialog(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            print(folder_selected)
            self.render_project(folder_selected)

    def project_save_dir_dialog(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            os.makedirs(os.path.join(folder_selected,
                        self.project_settings["name"]))
            file_worker.write_project(self.blocks, os.path.join(
                folder_selected, self.project_settings["name"]))

    def render_project(self, path):
        # Clear current blocks
        for block in self.blocks:
            block.place_forget()  # Loaded blocks
        self.blocks.clear()

        project_settings, compiled_blocks = file_worker.read_project(
            path)
        for obj in zip(project_settings, compiled_blocks):
            button = tk.Button(root, bd=0)
            if obj[1]["action"] == 0:
                button["text"] = f"Motors\nType: {obj[1]['type']}\nData: {obj[1]['steps_cnt']}\nDirection:{obj[1]['direction']}"
                button["bg"] = "lightblue"
                button.place(x=obj[0][0], y=obj[0][1])
                print(obj[1])
                self.blocks[button] = {"action": 0,
                                       "type": obj[1]['type'],
                                       "steps_cnt": obj[1]['steps_cnt'],
                                       "direction": obj[1]['direction'],
                                       "comment": obj[1]['comment']}
                if obj[1]['comment'] and len(obj[1]['comment']) > 0:
                    tooltip = Hovertip(button, obj[1]['comment'])
            dndr_button = tkinter_dndr.DragDropResizeWidget(button)
            dndr_button.make_draggable()
            button.bind('<Double-Button-1>', lambda x=0: self.spawn_obj(0))
            button.bind(
                "<Button-3>", lambda event: self.configure_block(0, event))

        print(self.blocks)

    def spawn_obj(self, type=0):
        if type == 0:
            print("Spawn block motors")
            button = tk.Button(
                text="Motors\nType: None\nData:None\nDirection:None", bd=0, bg="lightblue")
            self.blocks[button] = {"action": type,
                                   "type": None,
                                   "steps_cnt": None,
                                   "direction": None,
                                   "comment": None}
            button.bind("<Button-3>", lambda event,
                        block_ui=button: self.configure_block(0, event))
            button.place(x=10, y=220)
            dndr_button = tkinter_dndr.DragDropResizeWidget(button)
            dndr_button.make_draggable()
            button.bind('<Double-Button-1>', lambda x=0: self.spawn_obj(0))

    def save(self, block_ui, type_action, type_data, direction_data, comment_entry):
        block_ui["text"] = f"Motors\nType: {type_action}\nData:{type_data.get()}\nDirection:{direction_data.get()[0]}"
        self.blocks[block_ui] = {"action": 0,
                                 "type": type_action,
                                 "steps_cnt": type_data.get(),
                                 "direction": direction_data.get()[0],
                                 "comment": comment_entry.get("1.0", tk.END)}
        print(self.blocks[block_ui])

    def configure_block(self, block_type, event):
        block_ui = event.widget
        if block_type == 0:
            configure_window = tk.Toplevel(root)
            configure_window.title("Configure block")
            configure_window.geometry("500x300")
            counter_type_label = tk.Label(configure_window, text="Counter type",
                     font="Arial 13 bold")
            counter_type_label.pack()

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
            counter_type_chooser = tk.OptionMenu(
                configure_window, choose_var, *options)
            counter_type_chooser.pack()
            steps_counter_label = tk.Label(configure_window, text="Steps count",
                     font="Arial 13 bold")
            steps_counter_label.pack()
            saved_data_var = ""
            if block_ui in self.blocks:
                saved_data_var = self.blocks[block_ui]["steps_cnt"]
            data_var = tk.StringVar(value=saved_data_var)

            action_data = tk.Entry(configure_window, textvariable=data_var)
            action_data.pack()

            direction_label = tk.Label(configure_window, text="Direction",
                     font="Arial 13 bold")
            direction_label.pack()
            choose_direction_var = tk.StringVar(
                configure_window, value=directions_options[0])
            direction_chooser = tk.OptionMenu(
                configure_window, choose_direction_var, *directions_options)
            direction_chooser.pack()

            comment_label = tk.Label(configure_window, text="Comment",
                     font="Arial 13 bold")
            comment_label.pack()
            comment_entry = tk.Text(configure_window, width=40, height=5)
            comment_entry.pack()
            if block_ui in self.blocks and self.blocks[block_ui]["comment"]:
                comment_entry.insert(tk.END, self.blocks[block_ui]["comment"])

            save_btn = tk.Button(configure_window, text="Save", command=lambda a=block_ui, b=options.index(
                choose_var.get()), c=data_var, d=choose_direction_var, e=comment_entry: self.save(a, b, c, d, e))
            save_btn.pack(pady=10)

            if DARKTHEME:
                configure_window.configure(background="#121212")
                counter_type_label.configure(background='#121212', foreground='white')
                counter_type_chooser.configure(highlightbackground = "#121212", highlightcolor= "#121212", background='#121212', foreground='white', bg="#121212", activebackground="#121212", activeforeground="red")
                steps_counter_label.configure(background='#121212', foreground='white')
                direction_label.configure(background='#121212', foreground='white')
                action_data.configure(highlightcolor="white", background="#1a1919", foreground="white", insertbackground="red")
                direction_chooser.configure(highlightbackground = "#121212", highlightcolor= "#121212", background='#121212', foreground='white', bg="#121212", activebackground="#121212", activeforeground="red")
                comment_label.configure(background='#121212', foreground='white')
                comment_entry.configure(highlightcolor="white", background="#1a1919", foreground="white", insertbackground="red")
                save_btn.configure(background="black", foreground="white", borderwidth=0, highlightcolor="black")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    logger = Logger()
    root.mainloop()
