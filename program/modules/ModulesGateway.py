import importlib
import os

namespace = "program.modules.Classes"

class ModulesGateway:
    __instance = None   #<--WHY CAN'T THIS BE PRIVATE???????????????? REEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE

    def __init__(self):
        if ModulesGateway.__instance == None:

            classesDirectory = os.path.dirname(__file__) + "/Classes/"

            for fileNameFull in os.listdir(classesDirectory):
                if os.path.isfile(classesDirectory + fileNameFull):
                    try:
                        fileName = os.path.splitext(fileNameFull)[0]
                        module = importlib.import_module(namespace + "." + fileName)
                        self.__setattr__(fileName, getattr(module, fileName))


                    except Exception:
                        print("ERROR: Couldn't load module " + fileNameFull + ".")

            ModulesGateway.__instance = self

        else:
            self = ModulesGateway.__instance
