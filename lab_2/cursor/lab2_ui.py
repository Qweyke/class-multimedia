from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QSlider,
    QLabel,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QGroupBox,
)
from PySide6.QtCore import Qt
from lab2_scene import SceneWidget, DisplayMode, ShadingMode
from lab2_letters import Letter3D


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("3D-letters renderer")
        self.setGeometry(100, 100, 1000, 800)

        # Main window
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QHBoxLayout(main_widget)

        # Scene
        self.scene = SceneWidget()
        layout.addWidget(self.scene, stretch=3)

        # Control-box
        control_widget = QWidget()
        control_layout = QVBoxLayout(control_widget)
        control_layout.setContentsMargins(5, 5, 5, 5)
        control_layout.setSpacing(10)
        control_widget.setSizePolicy(
            QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding
        )

        letters_to_setup = [
            self.scene.d_letter,
            self.scene.b_letter,
        ]

        # Letters controls
        for letter_obj in letters_to_setup:
            self.create_letter_controls(control_layout, letter_obj)
            self.create_rotation_controls(control_layout, letter_obj)

        # Camera controls
        self.create_transform_controls(
            control_layout, "Camera controls:", self.rotate_camera, self.zoom_camera
        )
        self.create_camera_move_controls(control_layout)
        self.create_mirror_controls(control_layout)
        self.create_display_controls(control_layout)
        self.create_shading_controls(control_layout)
        self.create_light_controls(control_layout)

        # Reset
        reset_btn = QPushButton("Reset view")
        reset_btn.setMinimumHeight(40)
        reset_btn.clicked.connect(self.reset_view)
        control_layout.addWidget(reset_btn)
        control_layout.addStretch()

        scroll_area = QScrollArea()
        scroll_area.setWidget(control_widget)
        scroll_area.setWidgetResizable(True)
        scroll_area.setMinimumWidth(350)
        scroll_area.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Expanding)
        layout.addWidget(scroll_area, stretch=1)

    def create_letter_controls(self, layout, letter_obj: Letter3D):
        group = QGroupBox(letter_obj.letter_type)
        group_layout = QVBoxLayout(group)
        group_layout.setSpacing(5)

        for param in [
            "height",
            "width",
            "depth",
        ]:
            slider = QSlider(Qt.Horizontal)
            slider.setRange(10, 200)
            slider.setValue(getattr(letter_obj, param))
            slider.valueChanged.connect(
                lambda v, p=param, obj=letter_obj: self.update_letter_param(obj, p, v)
            )

            label = QLabel(param.capitalize())
            label.setAlignment(Qt.AlignCenter)

            group_layout.addWidget(label)
            group_layout.addWidget(slider)

        scale_label = QLabel("Scale")
        scale_label.setAlignment(Qt.AlignCenter)
        scale_slider = QSlider(Qt.Horizontal)
        scale_slider.setRange(50, 200)
        scale_slider.setValue(int(letter_obj.scale * 100))
        scale_slider.valueChanged.connect(
            lambda v, obj=letter_obj: self.update_letter_scale(obj, v)
        )

        group_layout.addWidget(scale_label)
        group_layout.addWidget(scale_slider)

        layout.addWidget(group)

    def create_rotation_controls(self, layout, letter_obj: Letter3D):
        group = QGroupBox("Rotation")
        group_layout = QHBoxLayout(group)
        group_layout.setSpacing(5)

        for axis, text in [(0, "X"), (1, "Y"), (2, "Z")]:
            btn_layout = QVBoxLayout()
            btn_layout.setSpacing(5)

            label = QLabel(text)
            label.setAlignment(Qt.AlignCenter)
            btn_layout.addWidget(label)

            btn_plus = QPushButton("+")
            btn_plus.setMinimumSize(50, 30)
            btn_plus.clicked.connect(
                lambda _, a=axis, obj=letter_obj: self.rotate_letter(obj, a, 10)
            )
            btn_layout.addWidget(btn_plus)

            btn_minus = QPushButton("-")
            btn_minus.setMinimumSize(50, 30)
            btn_minus.clicked.connect(
                lambda _, a=axis, obj=letter_obj: self.rotate_letter(obj, a, -10)
            )
            btn_layout.addWidget(btn_minus)

            group_layout.addLayout(btn_layout)

        layout.addWidget(group)

    def create_transform_controls(self, layout, title, rotate_cb, scale_cb):
        group = QGroupBox(title)
        group_layout = QVBoxLayout(group)
        group_layout.setSpacing(10)

        if rotate_cb:
            rot_group = QWidget()
            rot_layout = QHBoxLayout(rot_group)
            rot_layout.setSpacing(5)

            for axis, text in [(0, "X"), (1, "Y"), (2, "Z")]:
                btn_layout = QVBoxLayout()
                btn_layout.setSpacing(5)

                label = QLabel(text)
                label.setAlignment(Qt.AlignCenter)
                btn_layout.addWidget(label)

                btn_plus = QPushButton("+")
                btn_plus.setMinimumSize(50, 30)
                btn_plus.clicked.connect(lambda _, a=axis: rotate_cb(a, 10))
                btn_layout.addWidget(btn_plus)

                btn_minus = QPushButton("-")
                btn_minus.setMinimumSize(50, 30)
                btn_minus.clicked.connect(lambda _, a=axis: rotate_cb(a, -10))
                btn_layout.addWidget(btn_minus)

                rot_layout.addLayout(btn_layout)

            group_layout.addWidget(rot_group)

        if scale_cb:
            scale_slider = QSlider(Qt.Horizontal)
            scale_slider.setRange(50, 200)
            scale_slider.setValue(100)
            scale_slider.valueChanged.connect(scale_cb)

            label = QLabel("Zoom:")
            label.setAlignment(Qt.AlignCenter)

            group_layout.addWidget(label)
            group_layout.addWidget(scale_slider)

        layout.addWidget(group)

    def create_camera_move_controls(self, layout):
        group = QGroupBox("Camera move-controls")
        group_layout = QVBoxLayout(group)

        btn_up = QPushButton("Up")
        btn_down = QPushButton("Down")
        btn_left = QPushButton("Left")
        btn_right = QPushButton("Right")

        btn_up.clicked.connect(lambda: self.translate_camera(0, 20))
        btn_down.clicked.connect(lambda: self.translate_camera(0, -20))
        btn_left.clicked.connect(lambda: self.translate_camera(-20, 0))
        btn_right.clicked.connect(lambda: self.translate_camera(20, 0))

        row1 = QHBoxLayout()
        row1.addStretch()
        row1.addWidget(btn_up)
        row1.addStretch()

        row2 = QHBoxLayout()
        row2.addWidget(btn_left)
        row2.addWidget(btn_down)
        row2.addWidget(btn_right)

        group_layout.addLayout(row1)
        group_layout.addLayout(row2)

        layout.addWidget(group)

    def create_mirror_controls(self, layout):
        group = QGroupBox("Mirror view")
        group_layout = QHBoxLayout(group)
        group_layout.setSpacing(10)

        for axis, text in [(0, "X"), (1, "Y")]:
            btn = QPushButton(f"{text}")
            btn.setCheckable(True)
            btn.setMinimumSize(80, 30)
            btn.clicked.connect(lambda _, a=axis: self.scene.set_mirror(a))
            group_layout.addWidget(btn)

        layout.addWidget(group)

    def create_display_controls(self, layout):
        group = QGroupBox("Display mode")
        group_layout = QVBoxLayout(group)
        group_layout.setSpacing(5)

        for mode in DisplayMode:
            btn = QPushButton(mode.value)
            btn.setCheckable(True)
            btn.setMinimumHeight(30)
            btn.setChecked(mode == DisplayMode.FILLED)
            btn.clicked.connect(lambda _, m=mode: self.update_display(m))
            group_layout.addWidget(btn)

        layout.addWidget(group)

    def create_shading_controls(self, layout):
        group = QGroupBox("Shading")
        group_layout = QVBoxLayout(group)
        group_layout.setSpacing(5)

        for mode in ShadingMode:
            btn = QPushButton(mode.value)
            btn.setCheckable(True)
            btn.setMinimumHeight(30)
            btn.setChecked(mode == ShadingMode.MONO)
            btn.clicked.connect(lambda _, m=mode: self.update_shading(m))
            group_layout.addWidget(btn)

        layout.addWidget(group)

    def create_light_controls(self, layout):
        group = QGroupBox("Light source")
        group_layout = QVBoxLayout(group)
        group_layout.setSpacing(5)

        axes = [("x", "X"), ("y", "Y"), ("z", "Z")]
        ranges = {
            "x": (-300, 300),
            "y": (-300, 300),
            "z": (-500, 0),
        }

        for axis_key, axis_label in axes:
            slider = QSlider(Qt.Horizontal)
            mn, mx = ranges[axis_key]
            slider.setRange(mn, mx)
            current = getattr(self.scene.light_pos, axis_key)
            slider.setValue(int(current))
            slider.valueChanged.connect(
                lambda v, ax=axis_key: self.update_light_position(ax, v)
            )

            label = QLabel(f"Offset {axis_label}")
            label.setAlignment(Qt.AlignCenter)

            group_layout.addWidget(label)
            group_layout.addWidget(slider)

        layout.addWidget(group)

    def rotate_camera(self, axis, angle):
        self.scene.camera_rot[axis] += angle
        self.scene.invalidate_cache()
        self.scene.update()

    def zoom_camera(self, value):
        t = (value - 50) / 150.0
        self.scene.camera_pos.z = -(800 - 600 * t)
        self.scene.invalidate_cache()
        self.scene.update()

    def translate_camera(self, dx, dy):
        self.scene.camera_pos.x += dx
        self.scene.camera_pos.y += dy
        self.scene.invalidate_cache()
        self.scene.update()

    def rotate_letter(self, letter_obj, axis, angle):
        self.scene.rotate_letter(letter_obj, axis, angle)

    def update_letter_scale(self, letter_obj, value):
        scale_factor = value / 100.0
        self.scene.scale_letter(letter_obj, scale_factor)

    def update_letter_param(self, letter_obj, param, value):
        setattr(letter_obj, param, value)
        letter_obj.update_geometry()
        self.scene.invalidate_cache()
        self.scene.update()

    def update_display(self, mode):
        self.scene.set_display_mode(mode)
        for btn in self.findChildren(QPushButton):
            if btn.text() in [m.value for m in DisplayMode]:
                btn.setChecked(btn.text() == mode.value)

    def update_shading(self, mode):
        self.scene.set_shading_mode(mode)
        for btn in self.findChildren(QPushButton):
            if btn.text() in [m.value for m in ShadingMode]:
                btn.setChecked(btn.text() == mode.value)

    def update_light_position(self, axis, value):
        setattr(self.scene.light_pos, axis, float(value))
        self.scene.invalidate_cache()
        self.scene.update()

    def reset_view(self):
        self.scene.reset_view()
