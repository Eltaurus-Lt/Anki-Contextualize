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
        self.sample_label = QLabel("Sample Sentence")
        self.sample_field = QComboBox()
        self.sample_field.addItems(notes_fields)
        self.sample_field.setCurrentIndex(sentence_field_index(notes_fields))

        self.screen_label = QLabel("Screenshot")
        self.screen_field = QComboBox()
        self.screen_field.addItems(notes_fields)
        # self.screen_field.setCurrentIndex(sentence_field_index(notes_fields))

        self.source_label = QLabel("Source")
        self.source_field = QLineEdit()
        self.source_field.setMaxLength(255)
        self.source_field.setPlaceholderText("Enter source name")

        self.button_ok = QPushButton("OK")
        self.button_cancel = QPushButton("Cancel")

        # Create layout
        font_size = int(self.source_label.font().pointSize())

        layout = QVBoxLayout()
        layout.addWidget(self.sample_label)
        layout.addWidget(self.sample_field)
        layout.addWidget(self.screen_label)
        layout.addWidget(self.screen_field)
        layout.addWidget(self.source_label)
        layout.addWidget(self.source_field)

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
        return self.sample_field.currentText(), self.screen_field.currentText(), self.source_field.text()