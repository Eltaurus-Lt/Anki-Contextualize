from aqt.qt import *

def is_sentence_string(string):
    return ("sentence" in string or "Sentence" in string)

def sentence_field_index(array):
    for i, string in enumerate(array):
        if is_sentence_string(string):
            return i
    return len(array)-1

class FillChoices(QDialog):
    def __init__(self, notes_fields):
        super().__init__()

        # Create widgets
        self.sentence_label = QLabel("Sample Sentence field")
        self.sentence_field = QComboBox()
        self.sentence_field.addItems(notes_fields)
        self.sentence_field.setCurrentIndex(sentence_field_index(notes_fields))

        self.screenshot_label = QLabel("Screenshot field")
        self.screenshot_field = QComboBox()
        self.screenshot_field.addItems(notes_fields)
        # self.screenshot_field.setCurrentIndex(sentence_field_index(notes_fields))

        self.source_field_label = QLabel("Source field")
        self.source_field = QComboBox()
        self.source_field.addItems(notes_fields)

        self.source_label = QLabel("Source")
        self.source_text = QLineEdit()
        self.source_text.setMaxLength(255)

        self.button_ok = QPushButton("OK")
        self.button_cancel = QPushButton("Cancel")

        # Create layout
        font_size = int(self.source_label.font().pointSize())

        layout = QVBoxLayout()
        layout.addWidget(self.sentence_label)
        layout.addWidget(self.sentence_field)
        layout.addWidget(self.screenshot_label)
        layout.addWidget(self.screenshot_field)
        layout.addWidget(self.source_field_label)
        layout.addWidget(self.source_field)
        layout.addWidget(self.source_label)
        layout.addWidget(self.source_text)

        layout.addSpacing(2 * font_size)
        layout.addStretch()
  
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.button_ok)
        button_layout.addWidget(self.button_cancel)
        layout.addLayout(button_layout)

        # Set size limits
        self.setMinimumWidth(30 * font_size)
        self.setMaximumHeight(25 * font_size)
        self.setMaximumWidth(45 * font_size)

        # Set layout
        self.setLayout(layout)

        # Connect signals
        self.button_ok.clicked.connect(self.accept)
        self.button_cancel.clicked.connect(self.reject)

    def get_selected_options(self):
        return self.sentence_field.currentText(), self.screenshot_field.currentText(), self.source_field.currentText(), self.source_text.text()