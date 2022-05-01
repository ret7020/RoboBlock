import json, time, os
import tkinter as tk

def write(data, path=None):
    #data = list(data.values())
    data_temp = {}
    for block in data:
        data_temp[int(block.place_info()['x'])] = data[block]
    data = [data_temp[k] for k in sorted(data_temp)]
    
    if not path:
        path = f"ways/{time.strftime('%Y%m%d-%H%M%S')}.json"
    print(path)
    with open(path, "w") as file:
        json.dump(data, file)

def write_project(data, path_folder=None):
    project_folder = path_folder

    write(data, path=os.path.join(project_folder, "compiled.json"))
    ui_data = [] #[[x, y], [x, y]...]; sorted by x; from lower to upper
    for block in list(data.items()):
        ui_data.append([block[0].place_info()['x'], block[0].place_info()['y']])
    ui_data = sorted(ui_data, key=lambda x: int(x[0]))

    project_settings = {
        "compiled_json": "compiled.json",
        "blocks": ui_data
    }
    with open(os.path.join("projects/", project_folder, "project_settings.json"), "w") as file:
        json.dump(project_settings, file)
    
    
    #list(data.items())[0][0].place(x=0, y=10)

def read_project(path):
    # Read project settings
    with open(os.path.join(path, "project_settings.json"), "r") as file:
        project_settings = json.load(file)

    #Read compiled blocks data
    with open(os.path.join(path, "compiled.json"), "r") as file:
        compiled_blocks = json.load(file)
    #print(project_settings)
    #print(compiled_blocks)
    return project_settings["blocks"], compiled_blocks
if __name__ == "__main__":
    read_project("projects/20220427-191902/")