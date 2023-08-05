from PyQt6.QtWidgets import (
    QHBoxLayout,
)

class LayoutHandler:
    # Loops through all the widgets and adds them 
    # To the layout
    def createHBox(parent, widgets):
        horLayout = QHBoxLayout(parent)

        for w in widgets:
                horLayout.addWidget(w)

        return horLayout
