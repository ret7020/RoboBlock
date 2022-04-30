import json

'''
Way format:
{
    {left stepper; right stepper; 1; 0} //Current
}
'''

def convert(data=None, file=None):
    tab = " " * 4
    string_format = "int steps_match_blue[{}][4] = {{"
    if file:
        with open(file) as data_file:
            data = json.load(data_file)
    string_format = string_format.format(len(data))
    for step in data:
        if step["action"] == 0:
            if step["type"] == 0: #Supported only counter type
                if step["direction"] == '↑':
                    stepper_left = stepper_right = step['steps_cnt']
                elif step["direction"] == '←':
                    stepper_left, stepper_right = -int(step['steps_cnt']), step['steps_cnt']
                elif step["direction"] == '→':
                    stepper_left, stepper_right = int(step['steps_cnt']), -int(step['steps_cnt'])
                else:
                    stepper_left = stepper_right = -int(step['steps_cnt'])
                string_format += f"\n{tab}{{{stepper_left}, {stepper_right}, 1, 0}}"
    return string_format


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        path = sys.argv[1]    
        arduino_code = convert(file=path)
        
        print(f"Arduino ready array:\n{arduino_code}")
    else:
        print("Usage: python3 arduino_converter.py path/to/compiled.json")
    