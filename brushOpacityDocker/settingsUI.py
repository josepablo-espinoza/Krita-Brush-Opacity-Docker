from PyQt5.QtWidgets import (
    QComboBox, QGridLayout, QLabel, QLineEdit, QFrame,
    QPushButton, QVBoxLayout, QDialog, QHBoxLayout, QCheckBox
)
from PyQt5.QtCore import Qt
from .settingsService import *
from .qtExtras import *

class SettingsUI(QDialog):
    
    def __init__(self, settingsService: SettingsService, parent=None) -> None:
        super().__init__(parent)
        self.sv = settingsService
        self.initUI()

    def initUI(self):
        # Main layout
        main_layout = QVBoxLayout()
        customValues = self.sv.getCustomSettings()

        # ComboBox
        combo_layout = QHBoxLayout()
        combo_label = QLabel("Default mode:")
        self.opacity_combobox = QComboBox()
        self.opacity_combobox.addItems(self.sv.getDropdown().keys())
        self.opacity_combobox.setCurrentIndex(self.sv.getDefaultModeInt())

        combo_layout.addWidget(combo_label, 0)
        combo_layout.addWidget(self.opacity_combobox, 2)
        main_layout.addLayout(combo_layout)

        main_layout.addWidget(self.opacity_combobox)

        #cycle orientation
        self.cycleOrientationCheckbox = QCheckBox("Cycle Forward?")
        self.cycleOrientationCheckbox.setCheckState(Qt.Checked if self.sv.getCycleOrientation() else Qt.Unchecked)
        main_layout.addWidget(self.cycleOrientationCheckbox)
        

        # Custom Opacities Label and Horizontal Line
        custom_opacities_layout = QVBoxLayout()
        custom_opacities_label = QLabel("Custom Opacities")
        horizontal_line = QFrame()
        horizontal_line.setFrameShape(QFrame.HLine)
        horizontal_line.setFrameShadow(QFrame.Sunken)
        
        custom_opacities_layout.addWidget(custom_opacities_label)
        custom_opacities_layout.addWidget(horizontal_line)

        main_layout.addLayout(custom_opacities_layout)

        # Table Layout
        table_layout = QGridLayout()

        # First row (headers)
        table_layout.addWidget(QLabel(''), 0, 0)
        table_layout.addWidget(QLabel('Opacity'), 0, 1)
        table_layout.addWidget(QLabel('Min Opacity'), 0, 2)
        table_layout.addWidget(QLabel('Max Opacity'), 0, 3)

        self.opacity_inputs = {}
        for i, key in enumerate(customValues.keys(), start=1):
            data = customValues[key]
            table_layout.addWidget(QLabel(f'Opacity {i}'), i, 0)
            
            opacity_input = QLineEdit(str(data['opacity']))
            min_input = QLineEdit(str(data['min']))
            max_input = QLineEdit(str(data['max']))
            
            opacity_input.setValidator(IntValidator())
            min_input.setValidator(IntValidator())
            max_input.setValidator(IntValidator())

            self.opacity_inputs[key] = {
                'opacity': opacity_input,
                'min': min_input,
                'max': max_input
            }

            table_layout.addWidget(opacity_input, i, 1)
            table_layout.addWidget(min_input, i, 2)
            table_layout.addWidget(max_input, i, 3)

        # Add table layout to the main layout
        main_layout.addLayout(table_layout)

        # Buttons
        button_layout = QGridLayout()
        self.save_button = QPushButton('Save')
        self.cancel_button = QPushButton('Cancel')
        button_layout.addWidget(self.save_button, 0, 0)
        button_layout.addWidget(self.cancel_button, 0, 1)

        # Add buttons to the main layout
        main_layout.addLayout(button_layout)


        # Set main layout
        self.setLayout(main_layout)

        # Connect the save button to a function to print the selected value
        self.save_button.clicked.connect(self.saveSettings)
        self.cancel_button.clicked.connect(self.cancelSettings)

    def emitCloseDialog(self):
        self.parent().closeDialog()
        self.done(0)

    def cancelSettings(self):
        self.emitCloseDialog()

    def saveSettings(self):
        
        defaultMode = self.sv.getDropdown()[self.opacity_combobox.currentText()]
        
        customSettings = {}
        for key, inputs in self.opacity_inputs.items():
            customSettings[key] = {
                'opacity': int(inputs['opacity'].text()),
                'min': int(inputs['min'].text()),
                'max': int(inputs['max'].text())
            }
        
        cycleOrientationState = (self.cycleOrientationCheckbox.checkState() == Qt.Checked)

        # save
        self.sv.saveSettings(defaultMode, customSettings, cycleOrientationState)
        
        self.emitCloseDialog()