import json, time, os
import tkinter as tk

def write(data, path=None):
    data = list(data.values())
    
    if not path:
        path = f"{time.strftime('%Y%m%d-%H%M%S')}.json"
    print(path)
    with open(path, "w") as file:
        json.dump(data, file)

def write_project(data, path_folder=None):
    project_folder = path_folder
    if not path_folder:
        project_folder = time.strftime('%Y%m%d-%H%M%S')
        os.makedirs(os.path.join("projects/", project_folder))
    write(data, path=f"projects/{project_folder}/compiled.json")
    ui_data = [] #[[x, y], [x, y]...]
    for block in list(data.items()):
        print(block)
        ui_data.append([block[0].winfo_rootx(), block[0].winfo_rooty()])
    print(ui_data)

    project_settings = {
        "compiled_json": "compiled.json",
        "blocks": ui_data
    }
    with open(os.path.join("projects/", project_folder, "project_settings.json"), "w") as file:
        json.dump(project_settings, file)
    
    
    #list(data.items())[0][0].place(x=0, y=10)

def read_project(path, master):
    # Read project settings
    with open(os.path.join(path, "project_settings.json"), "r") as file:
        project_settings = json.load(file)

    #Read compiled blocks data
    with open(os.path.join(path, "compiled.json"), "r") as file:
        compiled_blocks = json.load(file)
    #print(project_settings)
    #print(compiled_blocks)
    for obj in zip(project_settings["blocks"], compiled_blocks):
        print(obj)
        button = tk.Button(master, bd=0)
        if obj[1]["action"] == 0:
            button.place(x=obj[0][0], y=obj[0][1])
            button["text"] = f"Motors\nType: {obj[1]['type']}\nData: {obj[1]['steps_cnt']}\nDirection:{obj[1]['direction']}"
            button["bg"] = "lightblue"
if __name__ == "__main__":
    read_project("projects/20220427-191902/")