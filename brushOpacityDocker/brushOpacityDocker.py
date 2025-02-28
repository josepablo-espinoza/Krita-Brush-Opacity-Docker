from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLineEdit, QToolButton,
    QComboBox, QSlider, QSpacerItem, QSizePolicy,
    QSizePolicy, QApplication, QCheckBox, QListView,
    QFrame
)
from PyQt5.QtCore import (Qt, QSize,  QTimer, QItemSelectionModel )

from krita import DockWidget, Krita
from math import floor
from .settingsService import *
from .settingsUI import *
from .qtExtras import *
from .brushOpacityDockerExtension import *

import xml.etree.ElementTree as ET

DOCKER_NAME = 'Brush Opacity Docker '

class BrushOpacityDocker(DockWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(DOCKER_NAME)
        self.sv = SettingsService()
        self.setting_dialog = None
        self.setUI()
        self.currentOpacityIndex = 2 # i.e. opacity 3
        self.setExtension()
        self.previousBlendingMode = "normal"

    def setUI(self):

        #for minimize
        # Create the main widget for the docker
        self.rootWidget = QWidget()


        self.bodyContainer = QVBoxLayout()
        self.bodyContainer.setContentsMargins(0,0,0,0)
        self.bodyContainer.setSpacing(0)

        self.rootWidget.setLayout(self.bodyContainer)
        self.setWidget(self.rootWidget)

        self.rootWidget.setMinimumSize(QSize(30,30))

        #minimize docker
        self.minimizeButton = QPushButton()
        self.minimizeButton.setIcon( Krita.instance().icon("visible") ) 
        self.minimizeButton.setCheckable(True)  # Make it toggleable
        self.minimizeButton.setChecked(False)    # Initially checked (visible)
        self.minimizeButton.clicked.connect(self.toggleDockerVisibility)
        self.bodyContainer.addWidget(self.minimizeButton)

        #main widget
        self.widget = QWidget(self)
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 15, 0, 0)  # Reduce the margins around the layout

        self.opacity_inputs = []
        self.opacity_sliders = []
        
        # used to not update the brush opacity when changing presets
        # TODO: change this abomination
        self.presetChange = False
        
        # dropdown
        self.preset_selector = QComboBox(self)
        self.preset_selector.addItems(self.sv.getModes())
        self.preset_selector.setCurrentIndex(self.sv.getDefaultModeInt())
        self.preset_selector.currentIndexChanged.connect(self.update_preset)

        self.button_configure =  QToolButton() 
        self.button_configure.setIcon( Krita.instance().icon("configure-shortcuts") )
        self.button_configure.clicked.connect(self.openDialog)
        
        self.top_widget = QWidget()
        self.top_layout = QHBoxLayout() 
        self.top_layout.setContentsMargins(4, 0, 4, 0)

        self.top_layout.addWidget(self.preset_selector)
        self.top_layout.addWidget(self.button_configure)

        self.top_widget.setLayout(self.top_layout)
        self.layout.addWidget(self.top_widget)

        for i in range(4):
            row_layout = QHBoxLayout()

            button = QPushButton(f"Opacity {i+1}", self)
            button.setFixedWidth(60)  # Set fixed width for buttons
            button.clicked.connect(lambda checked, index=i: self.set_brush_opacity(index))

            input_field = QLineEdit(self)
            input_field.setFixedWidth(35)  # Set fixed width for input fields
            input_field.setValidator(FloatValidator())
            self.opacity_inputs.append(input_field)

            slider = QSlider(Qt.Horizontal, self)
            slider.valueChanged.connect(lambda value, index=i: self.update_input_from_slider(value, index))
            self.opacity_sliders.append(slider)

            row_layout.addWidget(button)
            row_layout.addWidget(input_field)
            row_layout.addWidget(slider)

            self.layout.addLayout(row_layout)

        self.recalculate_button = QPushButton("Recalculate", self)
        self.recalculate_button.clicked.connect(self.update_preset)
        self.recalculate_button.setVisible(False)
        self.layout.addWidget(self.recalculate_button)

        self.pressure_button = QPushButton("toggle pressure", self)
        self.pressure_button.clicked.connect(self.toggle_opacity_pressure)
        self.layout.addWidget(self.pressure_button)

        self.greater_button = QPushButton("set to greater mode", self)
        self.greater_button.clicked.connect(self.toggleGreater)
        self.layout.addWidget(self.greater_button)

        # Spacer to push the content to the top
        self.layout.addSpacerItem(QSpacerItem(150, 300, QSizePolicy.Minimum, QSizePolicy.Expanding))
        # Spacer for minimize
        self.spacer = QSpacerItem(1, 3, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.widget.setLayout(self.layout)
        
        self.bodyContainer.addWidget(self.widget,10)  
        self.setWidget(self.rootWidget)

        # Set initial preset to "Medium"
        self.update_preset()

    def setExtension(self):
        extension = BrushOpacityDockerExtension( parent = Krita.instance() )
        Krita.instance().addExtension( extension )

        extension.SIGNAL_CYCLE.connect( self.nextBrushOpacity )

    def openDialog(self):
        if self.setting_dialog == None:
            self.setting_dialog = SettingsUI(self.sv, self)
            self.setting_dialog.show() 
        elif self.setting_dialog.isVisible() == False : 
            self.setting_dialog.show() 
            #self.setting_dialog.loadDefault()
        else:
            pass
    
    def closeDialog(self):
        self.update_preset()


    def update_preset(self):
        self.presetChange = True
        preset = self.preset_selector.currentText().lower()
        if preset == "small":
            opacities = self.sv.getSmallOpacities()
            self.recalculate_button.setVisible(False)
        elif preset == "medium":
            opacities = self.sv.getMediumOpacities()
            self.recalculate_button.setVisible(False)
        elif preset == "large":
            opacities = self.sv.getLargeOpacities()
            self.recalculate_button.setVisible(False)
        elif preset == "current brush":
            opacities = self.calculate_current_brush_opacities()
            self.recalculate_button.setVisible(True)
        elif preset == "custom":
            opacities = self.sv.getCustomOpacities()
            self.recalculate_button.setVisible(False)
        
        
        for i, opacity in enumerate(opacities):
            self.set_slider_range(i, opacity, preset)
            self.opacity_inputs[i].setText(str(opacity))
            self.opacity_sliders[i].setValue(int(opacity))
            
        self.presetChange = False

    def toggleGreater(self):
        window = Krita.instance().activeWindow()
        if window and window.views():
            view = window.views()[0]
            currentBlendingMode = view.currentBlendingMode()
            if currentBlendingMode != "greater":
                self.previousBlendingMode = currentBlendingMode
                view.setCurrentBlendingMode("greater")
                self.greater_button.setText(f"set to {self.previousBlendingMode} mode")
            else:
                view.setCurrentBlendingMode(self.previousBlendingMode)
                self.greater_button.setText(f"set to greater mode")

    '''
        this avoids any problem due to race condition, dirty and ugly
    '''
    def avoidLockingMinSize(self):
        self.rootWidget.setMinimumSize(30, 30)

    # Function to toggle the visibility of the main components of docker
    def toggleDockerVisibility(self):
        if not self.minimizeButton.isChecked():
            self.widget.setVisible(True)
            
            self.minimizeButton.setIcon( Krita.instance().icon("visible") ) 
            self.bodyContainer.removeItem(self.spacer)
            if self.currentDockerHeight > 40:
                self.rootWidget.setMinimumSize(self.currentDockerWidth, self.currentDockerHeight)
            else:
                # self.widget.setMinimumSize(self.currentDockerWidth, 350)
                self.rootWidget.setMinimumSize(350, 275)
            QTimer.singleShot(50, self.avoidLockingMinSize)
            self.rootWidget.setMaximumSize(1000, 1000)
        else:
            self.widget.setVisible(False)
            self.minimizeButton.setIcon( Krita.instance().icon("novisible") ) 
            self.currentDockerWidth = self.rootWidget.size().width()
            self.currentDockerHeight = self.rootWidget.size().height()
                
            # self.widget.setMaximumSize(self.currentDockerWidth, 25)    
            self.rootWidget.setMaximumSize(60, 25)
            
            self.bodyContainer.addSpacerItem(self.spacer)
            
    def set_slider_range(self, index, preset_value, preset):
        if preset != "custom":
            if index == 0:
                min_val, max_val = max(1, preset_value - 30), min(100, preset_value + 30)
            elif index == 1:
                min_val, max_val = max(1, preset_value - 40), min(100, preset_value + 40)
            elif index == 2:
                min_val, max_val = max(1, preset_value - 100), min(100, preset_value + 100)
            elif index == 3:
                min_val, max_val = max(1, preset_value - 100), min(100, preset_value + 100)
        else:
            min_val, max_val = self.sv.getCustomRange(index)

        self.opacity_sliders[index].setRange(int(min_val), int(max_val))


    def calculate_current_brush_opacities(self):
        current_opacity = self.get_current_brush_opacity()
        if current_opacity is None:
            current_opacity = self.sv.getMediumOpacities()[2]  # Default to medium opacity if current opacity is not available

        opacity1 = max(1, min(100, floor(current_opacity / 5)))
        opacity2 = max(1, min(100, floor(current_opacity / 2)))
        opacity3 = current_opacity
        opacity4 = max(1, min(100, floor(current_opacity * 5 / 3)))

        return [int(opacity1), int(opacity2), int(opacity3), int(opacity4)]

    def get_current_brush_opacity(self):
        window = Krita.instance().activeWindow()
        if window and window.views():
            view = window.views()[0]
            return view.paintingOpacity() * 100
        return None
    
    def set_brush_opacity(self, index):
        input_value = self.opacity_inputs[index].text()
        if input_value:
            try:
                opacity = float(input_value)/100
                self.change_brush_opacity(opacity)
            except ValueError:
                pass  # Handle the error as needed

    def change_brush_opacity(self, opacity):
        window = Krita.instance().activeWindow()
        if window and window.views():
            window.views()[0].setPaintingOpacity(opacity)

    def update_input_from_slider(self, value, index):
        self.opacity_inputs[index].setText(str(value))
        if not self.presetChange:
            self.currentOpacityIndex = index
            self.set_brush_opacity(index)

    def nextBrushOpacity(self):
        brushQuantity = 4 # not as elegant but good enough TODO use the length of some of the opacities array...
        print(self.sv.getCycleOrientation())
        orientation = -1 if self.sv.getCycleOrientation() else 1
        self.currentOpacityIndex =  (brushQuantity + (self.currentOpacityIndex - orientation)) % brushQuantity
        self.set_brush_opacity(self.currentOpacityIndex)

    
    def canvasChanged(self, canvas):
        pass

    def toggle_opacity_pressure(self):
        """
        Toggle the opacity setting in the current brush preset.
        
        This function retrieves the current brush preset from Krita, parses its XML,
        toggles the "OpacityUseCurve" parameter (and its sub-parameter if defined),
        updates the pressure button text accordingly, and then writes the updated preset back.
        
        Parameters:
            pressure_button: An object with a setText method, used to update the UI button.
        """
        # Get the active view and current brush preset from Krita
        view = Krita.instance().activeWindow().activeView()
        preset = Preset(view.currentBrushPreset())

        # Convert the preset to XML and parse it into an ElementTree
        preset_xml_string = preset.toXML()
        preset_tree = ET.fromstring(preset_xml_string)

        # Define the brush setting for opacity as a dictionary
        brush_property = {
            "name": "OpacityUseCurve",
            "value": False,
            "is_available": False,
            "sub_name": ""  # Change this if a sub-parameter should be toggled
        }

        # Loop through the 'param' elements to find the one matching our setting
        for param in preset_tree.findall('param'):
            if param.get('name') == brush_property["name"]:
                if param.text == "true":
                    param.text = "false"
                    self.pressure_button.setText("enable pressure")
                else:
                    param.text = "true"
                    self.pressure_button.setText("disable pressure")

                # # If a sub-parameter is defined, toggle its value as well
                # if brush_property["sub_name"]:
                #     for sub_param in preset_tree.findall('param'):
                #         if sub_param.get('name') == brush_property["sub_name"]:
                #             sub_param.text = "false" if sub_param.text == "true" else "true"

        # Convert the modified XML tree back to a string and update the preset
        preset_xml_string = ET.tostring(preset_tree, encoding="unicode")
        preset.fromXML(preset_xml_string)