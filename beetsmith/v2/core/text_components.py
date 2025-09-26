import json
from typing import Any

class TextComponent():
    "Utility class for working with text components."

    @staticmethod
    def normalize(obj: Any) -> list[list[dict]]:
        """Brings a text component object to a completely not-shorthanded format of a list of lists (the lines) of dicts (segments in a line)

        #### Additional use:
            - [0]: if only one line is allowed in the field
        """
        newLines = []

        if type(obj) == list:                       # obj ist Line oder Multiline
            if list in [type(e) for e in obj]:      # obj ist Multiline
                for line in obj:
                    if type(line) == str:                   # line ist str
                        newLines.append([{"text": line}])
                    elif type(line) == dict:                # line ist dict
                        newLines.append([line])
                    elif type(line) == list:                # line ist list
                        newLine = []
                        for part in line:
                            if type(part) == str:               # part ist str
                                newLine.append({"text": part})
                            elif type(part) == dict:            # part ist dict
                                newLine.append(part)
                            else:
                                print(type(part)) # Debug
                                print(part)
                                raise ValueError("Every part in a line in the object has to be a dictionary or a string")
                        newLines.append(newLine)
                    else:                                   # line ist nicht str, dict oder list
                        raise ValueError("Every line in the object has to be a list, a dictionary or a string")
            else:                                   # obj ist line mit parts
                newLine = []
                for part in obj:
                    if type(part) == str:                   # part ist str
                        newLine.append({"text": part})
                    elif type(part) == dict:                # part ist dict
                        newLine.append(part)
                newLines.append(newLine)
        elif type(obj) == dict:
            newLines.append([obj])
        elif type(obj) == str:
            newLines.append([{"text": obj}])
        else:
            ValueError("Object has to be a list, a dictionary or a string")

        return newLines
    
    @staticmethod
    def from_json(stringified_json: str) -> list[list[dict]]:
        data = json.load(stringified_json)
        return TextComponent.normalize(data)

    @staticmethod
    def get_plain_text(textcomponent: str | dict | list) -> str:
        "Returns a unformatted (and if the case multiline) string of a text component"
        textcomponent: list[list[dict]] = TextComponent.normalize(textcomponent)

        result = ""
        for line in textcomponent:
            for segment in line:
                for key, value in segment.items():
                    if key == "text":
                        result += value
                    elif key in ["translate", "keybind"]:
                        result += f"<{value}>"
            if len(textcomponent) > 1:
                result += "\n"
        
        return result