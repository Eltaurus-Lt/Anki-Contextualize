import os
from . import Conjugations
from aqt.qt import *
from aqt import mw

config = mw.addonManager.getConfig(__name__)

Sub_exts = ["srt", "sub", "ass"]
Video_exts = ["mkv", "mp4", "avi"]
Text_exts = ["txt"]

def extFilter(extensions):
    return " ".join([f"*.{s}" for s in extensions])

def indexFromCandidates(fields, candidates):
    fields = [field.lower() for field in fields]
    for candidate in candidates:
        if candidate in fields:
            return fields.index(candidate)
            
    return 0

class FillContext(QDialog):
    def __init__(self, notes_fields):
        super().__init__()

        notes_fields_ = ['—'] + notes_fields

        # Create widgets
        self.word_field = QComboBox()
        self.word_field.addItems(notes_fields)

        self.alts_field = QComboBox()
        self.alts_field.addItems(notes_fields_)

        self.lang_pack = QComboBox()
        self.lang_pack.addItems(['—'] + Conjugations.installedPacks())

        self.sentence_field = QComboBox()
        self.sentence_field.addItems(notes_fields_)
        self.sentence_field.setCurrentIndex(indexFromCandidates(notes_fields_, config["sentence candidates"]))

        self.screenshot_field = QComboBox()
        self.screenshot_field.addItems(notes_fields_)
        self.screenshot_field.setCurrentIndex(indexFromCandidates(notes_fields_, config["screenshot candidates"]))

        self.source_field = QComboBox()
        self.source_field.addItems(notes_fields_)
        self.source_field.setCurrentIndex(indexFromCandidates(notes_fields_, config["source candidates"]))

        self.videoFile_path = QLineEdit("")
        # self.videoFile_path.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.videoFile_button = QPushButton("Select File", self)
        self.videoFile_button.clicked.connect(self.selectVideoFile)

        self.subtitleFile_path = QLineEdit("")
        # self.subtitleFile_path.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.subtitleFile_button = QPushButton("Select File", self)
        self.subtitleFile_button.clicked.connect(self.selectSubtitleFile)

        self.source_text = QTextEdit()
        font_metrics = QFontMetrics(self.source_text.font())
        line_height = font_metrics.lineSpacing()
        self.source_text.setFixedHeight(5 * line_height)
        # self.source_text.setMinimumHeight(line_height)
        # self.source_text.setMaximumHeight(5 * line_height)
        # self.source_text.resize(self.source_text.width(), 3 * line_height)
        # self.source_text.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.MinimumExpanding))
        # self.source_text.setMaxLength(255)

        self.tag_string = QLineEdit("")

        self.button_ok = QPushButton("OK")
        self.button_cancel = QPushButton("Cancel")


        # Create layout
        layout = QVBoxLayout()

        word_group = QGroupBox("Word")
        word_layout = QVBoxLayout()
        word_group.setLayout(word_layout)
        layout.addWidget(word_group)

        word_layout.addWidget(QLabel("Main field"))
        word_layout.addWidget(self.word_field)
        word_layout.addWidget(QLabel("Alts field"))
        word_layout.addWidget(self.alts_field)
        word_layout.addWidget(QLabel("Conjugation Pack"))
        word_layout.addWidget(self.lang_pack)


        context_group = QGroupBox("Contextualize fields")
        context_layout = QVBoxLayout()
        context_group.setLayout(context_layout)
        layout.addWidget(context_group)

        context_layout.addWidget(QLabel("Sample Sentence"))
        context_layout.addWidget(self.sentence_field)
        context_layout.addWidget(QLabel("Screenshot"))
        context_layout.addWidget(self.screenshot_field)
        context_layout.addWidget(QLabel("Source"))
        context_layout.addWidget(self.source_field)


        source_group = QGroupBox("Source")
        source_layout = QVBoxLayout()
        source_group.setLayout(source_layout)
        layout.addWidget(source_group)

        source_layout.addWidget(QLabel("Video"))
        videoFile_layout = QHBoxLayout()
        videoFile_layout.addWidget(self.videoFile_path)
        videoFile_layout.addWidget(self.videoFile_button)
        source_layout.addLayout(videoFile_layout)

        source_layout.addWidget(QLabel("Subtitles"))
        subtitleFile_layout = QHBoxLayout()
        subtitleFile_layout.addWidget(self.subtitleFile_path)
        subtitleFile_layout.addWidget(self.subtitleFile_button)
        source_layout.addLayout(subtitleFile_layout)

        source_layout.addWidget(QLabel("Text description"))
        source_layout.addWidget(self.source_text)

        source_layout.addWidget(QLabel("Tags"))
        source_layout.addWidget(self.tag_string)

        layout.addSpacing(2 * line_height)
        layout.addStretch()
  
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.button_ok)
        button_layout.addWidget(self.button_cancel)
        layout.addLayout(button_layout)

        # Set size limits
        self.setMinimumWidth(30 * line_height)
        self.setMaximumHeight(25 * line_height)
        self.setMaximumWidth(45 * line_height)

        # Set layout
        self.setLayout(layout)

        # Connect signals
        self.button_ok.clicked.connect(self.accept)
        self.button_cancel.clicked.connect(self.reject)

    def get_selected_options(self):
        return (
            self.word_field.currentText(), self.alts_field.currentText(), self.lang_pack.currentText(), 
            self.sentence_field.currentText(), self.screenshot_field.currentText(), self.source_field.currentText(), 
            self.videoFile_path.text(), self.subtitleFile_path.text(), self.source_text.toPlainText(), self.tag_string.text()
        )

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