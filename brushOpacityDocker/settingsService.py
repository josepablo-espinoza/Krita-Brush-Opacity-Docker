import os, json 

class SettingsService():
    
    def __init__(self) -> None:
        self.loadSettings()
        
    def loadSettings(self):
        json_setting = open(os.path.dirname(os.path.realpath(__file__)) + '/settings.json')
        self.setSettings(json.load(json_setting))
        json_setting.close()
        
    def setSettings(self, settings):
        self.settings = settings

    def getSettings(self):
        return self.settings
    
    def setCycleOrientation(self, orientation: bool):
        self.getSettings()["cycleOrientation"] = orientation
    
    '''
        if true cycles forward
    '''
    def getCycleOrientation(self) -> bool:
        return bool(self.settings["cycleOrientation"])

    def setDefaultMode(self, defaultMode: str):
        self.getSettings()["defaultMode"] = defaultMode

    def getDefaultMode(self) -> int:
        return int(self.settings["defaultMode"])

    def getModes(self) -> list[str]:
        modes =  [
            self.getSettings()["modes"]["small"]["label"],
            self.getSettings()["modes"]["medium"]["label"],
            self.getSettings()["modes"]["large"]["label"],
            self.getSettings()["modes"]["currentBrush"]["label"],
            self.getSettings()["modes"]["custom"]["label"]
        ]
        return modes
    
    def getDropdown(self) -> dict:
        modeMap = {
            self.getSettings()["modes"]["small"]["label"] : self.getSettings()["modes"]["small"]["key"],
            self.getSettings()["modes"]["medium"]["label"]: self.getSettings()["modes"]["medium"]["key"],
            self.getSettings()["modes"]["large"]["label"]: self.getSettings()["modes"]["large"]["key"],
            self.getSettings()["modes"]["currentBrush"]["label"]: self.getSettings()["modes"]["currentBrush"]["key"],
            self.getSettings()["modes"]["custom"]["label"]: self.getSettings()["modes"]["custom"]["key"]
        }
        return modeMap
    
    def getCustomSettings(self) -> dict:
        custom = self.getSettings()["modes"]["custom"]
        config = {
            "opacity1": {"opacity": custom["opacities"][0], "min": custom["ranges"][0]["min"], "max": custom["ranges"][0]["max"]},
            "opacity2": {"opacity": custom["opacities"][1], "min": custom["ranges"][1]["min"], "max": custom["ranges"][1]["max"]},
            "opacity3": {"opacity": custom["opacities"][2], "min": custom["ranges"][2]["min"], "max": custom["ranges"][2]["max"]},
            "opacity4": {"opacity": custom["opacities"][3], "min": custom["ranges"][3]["min"], "max": custom["ranges"][3]["max"]}
        }
        return config
    
    def getSmallOpacities(self) -> list[int]:
        return self.getOpacities("small")
    
    def getMediumOpacities(self) -> list[int]:
        return self.getOpacities("medium")
    
    def getLargeOpacities(self) -> list[int]:
        return self.getOpacities("large")
    
    def getCustomOpacities(self) -> list[int]:
        return self.getOpacities("custom")
    
    def getOpacities(self, mode: str) -> list[int]:
        return list(self.getSettings()["modes"][mode]["opacities"])
    
    def getCustomRange(self, index: int):
        ranges = self.getSettings()["modes"]["custom"]["ranges"]
        return (ranges[index]["min"], ranges[index]["max"])
    
    def getIndexByMode(self, mode: str) -> int:
        return int(self.getSettings()["modes"][mode]["index"])
    
    def getDefaultModeString(self) -> str:
        return self.getSettings()["defaultMode"]
    
    def getDefaultModeInt(self) -> int:
        return self.getIndexByMode(self.getDefaultModeString())

    def setCustomSettings(self, customSettings: dict):
        
        opacities = [
            int(customSettings["opacity1"]["opacity"]),
            int(customSettings["opacity2"]["opacity"]),
            int(customSettings["opacity3"]["opacity"]),
            int(customSettings["opacity4"]["opacity"])
        ]

        ranges = [
            {"min": int(customSettings["opacity1"]["min"]), "max": int(customSettings["opacity1"]["max"])},
            {"min": int(customSettings["opacity2"]["min"]), "max": int(customSettings["opacity2"]["max"])},
            {"min": int(customSettings["opacity3"]["min"]), "max": int(customSettings["opacity3"]["max"])},
            {"min": int(customSettings["opacity4"]["min"]), "max": int(customSettings["opacity4"]["max"])}
        ]

        self.getSettings()["modes"]["custom"]["opacities"] = opacities
        self.getSettings()["modes"]["custom"]["ranges"] = ranges


    def saveSettings(self, defaultMode: str, customSettings: dict, cycleOrientation: bool):
        self.setDefaultMode(defaultMode)
        self.setCustomSettings(customSettings)
        self.setCycleOrientation(cycleOrientation)
        json_setting = json.dumps(self.getSettings(), indent = 4)
        with open(os.path.dirname(os.path.realpath(__file__)) + '/settings.json', "w") as outfile:
            outfile.write(json_setting)

    def toString(self):
        print(f"Brush opacity docker settings: {self.getSettings()}")