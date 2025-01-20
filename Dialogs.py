import os
from aqt.qt import *
Sentence_candidates = {"sentence", "sample sentence", "source sentence", "例文"}
Screenshot_candidates = {"screenshot", "image", "絵"}
Sub_exts = ["srt", "sub", "ass", "stl"]
Video_exts = ["mkv", "mp4", "avi"]
Text_exts = ["txt"]

def extFilter(extensions):
    return " ".join([f"*.{s}" for s in extensions])

def indexFromCandidates(fields, candidates):
    for i, field in enumerate(fields):
        if field.lower() in candidates:
            return i
    return len(fields)-1

def conjugationPacks():
    files = os.listdir(os.path.join(os.path.dirname(__file__), 'ConjugationPacks'))
    return [os.path.splitext(file)[0] for file in files if file.endswith('.json')]

class FillContext(QDialog):
    def __init__(self, notes_fields):
        super().__init__()

        notes_fields_ = ['—'] + notes_fields

        # Create widgets
        self.word_label = QLabel("Word field")
        self.word_field = QComboBox()
        self.word_field.addItems(notes_fields)

        self.lang_label = QLabel("Conjugation Pack")
        self.lang_pack = QComboBox()
        self.lang_pack.addItems(['—'] + conjugationPacks())

        self.sentence_label = QLabel("Sample Sentence field")
        self.sentence_field = QComboBox()
        self.sentence_field.addItems(notes_fields_)
        self.sentence_field.setCurrentIndex(indexFromCandidates(notes_fields_, Sentence_candidates))

        self.screenshot_label = QLabel("Screenshot field")
        self.screenshot_field = QComboBox()
        self.screenshot_field.addItems(notes_fields_)
        self.screenshot_field.setCurrentIndex(indexFromCandidates(notes_fields_, Screenshot_candidates))

        self.source_field_label = QLabel("Source field")
        self.source_field = QComboBox()
        self.source_field.addItems(notes_fields_)

        self.source_label = QLabel("Source")
        self.source_text = QLineEdit()
        self.source_text.setMaxLength(255)

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
        layout.addWidget(self.word_label)
        layout.addWidget(self.word_field)
        layout.addWidget(self.lang_label)
        layout.addWidget(self.lang_pack)
        layout.addWidget(self.sentence_label)
        layout.addWidget(self.sentence_field)
        layout.addWidget(self.screenshot_label)
        layout.addWidget(self.screenshot_field)
        layout.addWidget(self.source_field_label)
        layout.addWidget(self.source_field)
        layout.addWidget(self.source_label)
        layout.addWidget(self.source_text)

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
        return self.word_field.currentText(), self.lang_pack.currentText(), self.sentence_field.currentText(), self.screenshot_field.currentText(), self.source_field.currentText(), self.source_text.text(), self.videoFile_path.text(), self.subtitleFile_path.text()

    def selectVideoFile(self):
        file_dialog = QFileDialog(self)
        file_dialog.setWindowTitle("Select the video file")
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        file_dialog.setNameFilter(f"Video Files ({extFilter(Video_exts)});;All Files (*)")

        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                file_name = os.path.normpath(selected_files[0])
                self.videoFile_path.setText(file_name)

                # autoselect matching subtitle file
                directory = os.path.dirname(file_name)
                basename = os.path.splitext(os.path.basename(file_name))[0]
                files = os.listdir(directory)

                file_name = ""
                for ext in Sub_exts:
                    if f"{basename}.{ext}" in files:
                        file_name = os.path.join(directory, f"{basename}.{ext}")
                        break
                if file_name:
                    self.subtitleFile_path.setText(file_name)



    def selectSubtitleFile(self):
        file_dialog = QFileDialog(self)
        file_dialog.setWindowTitle("Select the file with subtitles")
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        file_dialog.setNameFilter(f"Subtitles ({extFilter(Sub_exts)});;Video Files ({extFilter(Video_exts)});;Text ({extFilter(Text_exts)});;All Files (*)")

        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                file_name = os.path.normpath(selected_files[0])
                self.subtitleFile_path.setText(file_name)