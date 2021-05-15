from scripts.suport.creatingTextFile import returnFilename

filename = returnFilename()


def convertTxtToJson(filename=filename):
    dict_def = {}
    with open(filename) as f:
        for line in f:
            command, description = line.strip().split(None, 1)
            dict_def[command] = description.strip()
    return dict_def


convertTxtToJson()
