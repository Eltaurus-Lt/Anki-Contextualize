from aqt.qt import *

def is_choice_string(string):
    return ("choice" in string or "Choice" in string)

def choices_field_index(array):
    for i, string in enumerate(array):
        if is_choice_string(string):
            return i
    return len(array)-1

class FillChoices(QDialog):
    def __init__(self, notes_fields):
        super().__init__()

        # Create widgets
        self.source_label = QLabel("Source Field")
        self.source_field = QComboBox()
        self.source_field.addItems([field for field in notes_fields if not is_choice_string(field)])

        self.choices_label = QLabel("Choices Field")
        self.choices_field = QComboBox()
        self.choices_field.addItems(notes_fields)
        self.choices_field.setCurrentIndex(choices_field_index(notes_fields))

        self.radio_label = QLabel("Action")
        self.radio_group = QButtonGroup()
        self.radio_append = QRadioButton("Append")
        self.radio_overwrite = QRadioButton("Overwrite")
        self.radio_group.addButton(self.radio_append)

        self.radio_group.addButton(self.radio_overwrite)
        self.radio_append.setChecked(True)

        self.button_ok = QPushButton("OK")
        self.button_cancel = QPushButton("Cancel")

        self.videoFile_label = QLabel("Video")
        self.videoFile_path = QLineEdit("")
        self.videoFile_path.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.videoFile_button = QPushButton("Select File", self)
        self.videoFile_button.clicked.connect(self.selectVideoFile)

        self.subtitleFile_label = QLabel("Subtitles")
        self.subtitleFile_path = QLineEdit("")
        self.subtitleFile_path.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.subtitleFile_button = QPushButton("Select File", self)
        self.subtitleFile_button.clicked.connect(self.selectSubtitleFile)


        # Create layout
        font_size = int(self.source_label.font().pointSize())

        layout = QVBoxLayout()
        layout.addWidget(self.source_label)
        layout.addWidget(self.source_field)
        layout.addWidget(self.choices_label)
        layout.addWidget(self.choices_field)

        layout.addWidget(self.radio_label)
        radio_layout = QHBoxLayout()
        radio_layout.addWidget(self.radio_append)
        radio_layout.addSpacing(1 * font_size)
        radio_layout.addWidget(self.radio_overwrite)
        radio_layout.addStretch()
        layout.addLayout(radio_layout)

        layout.addSpacing(2 * font_size)

        layout.addWidget(self.videoFile_label)
        videoFile_layout = QHBoxLayout()
        videoFile_layout.addWidget(self.videoFile_path)
        videoFile_layout.addWidget(self.videoFile_button)
        layout.addLayout(videoFile_layout)

        layout.addWidget(self.subtitleFile_label)
        subtitleFile_layout = QHBoxLayout()
        subtitleFile_layout.addWidget(self.subtitleFile_path)
        subtitleFile_layout.addWidget(self.subtitleFile_button)
        layout.addLayout(subtitleFile_layout)

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
        return self.source_field.currentText(), self.choices_field.currentText(), self.radio_append.isChecked()

    def selectVideoFile(self):
        file_dialog = QFileDialog(self)
        file_dialog.setWindowTitle("Select the video file")
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        file_dialog.setNameFilter("Video Files (*.mkv *.mp4 .*m2ts *.avi);;All Files (*)")

        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                file_name = selected_files[0]
                self.videoFile_path.setText(file_name)

    def selectSubtitleFile(self):
        file_dialog = QFileDialog(self)
        file_dialog.setWindowTitle("Select the file with subtitles")
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        file_dialog.setNameFilter("Subtitles (*.srt *.sub *.ass *.stl);;Text (*.txt);;All Files (*)")

        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                file_name = selected_files[0]
                self.subtitleFile_path.setText(file_name)