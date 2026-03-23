from enum import Enum

from PySide6.QtCore import Qt, QPoint, QPointF
from PySide6.QtGui import QColor, QPainter, QPen, QBrush, QPolygonF
from PySide6.QtWidgets import QWidget

from lab2_math import Vector3D, Matrix4x4
from lab2_letters import Letter3D


class DisplayMode(Enum):
    POINTS = "Points"
    WIREFRAME = "Wire"
    FILLED = "Filled"


class ShadingMode(Enum):
    MONO = "Mono"
    GOURAUD = "Ghouraud"
    PHONG = "Phong"


class SceneWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), QColor(30, 30, 30))
        self.setPalette(p)

        self.d_letter = Letter3D(100, 60, 30, offset_x=-60, letter_type="Д")
        self.b_letter = Letter3D(100, 60, 30, offset_x=60, letter_type="Б")

        self.camera_pos = Vector3D(0, 0, -500, 1)
        self.camera_rot = [0, 0, 0]  # углы Эйлера
        self.light_pos = Vector3D(200, 200, -300, 1)

        self.display_mode = DisplayMode.FILLED
        self.shading_mode = ShadingMode.MONO
        self.cache_valid = False
        self.cached_faces = []

    def reset_view(self):
        self.camera_pos = Vector3D(0, 0, -500, 1)
        self.camera_rot = [0, 0, 0]

        self.d_letter.transform = Matrix4x4()
        self.b_letter.transform = Matrix4x4()
        self.d_letter.scale = 1.0
        self.b_letter.scale = 1.0

        self.light_pos = Vector3D(200, 200, -300, 1)

        self.set_display_mode(DisplayMode.FILLED)
        self.set_shading_mode(ShadingMode.MONO)

        self.invalidate_cache()
        self.update()

    def invalidate_cache(self):
        self.cache_valid = False

    def _camera_matrix(self):
        rot_x = Matrix4x4.rotation_x(self.camera_rot[0])
        rot_y = Matrix4x4.rotation_y(self.camera_rot[1])
        rot_z = Matrix4x4.rotation_z(self.camera_rot[2])
        rotation = rot_x * rot_y * rot_z
        translation = Matrix4x4.translation(
            -self.camera_pos.x, -self.camera_pos.y, -self.camera_pos.z
        )
        return rotation * translation

    def prepare_faces_cache(self):
        width, height = self.width(), self.height()
        self.cached_faces = []

        camera_mat = self._camera_matrix()
        aspect = width / height if height != 0 else 1

        for letter in [self.d_letter, self.b_letter]:
            faces = letter.get_transformed_faces()
            for face in faces:
                if not face.is_visible(self.camera_pos):
                    continue

                screen_points = []
                face_vertices = face.vertices
                face_vertices_cam = []

                for v in face_vertices:
                    v_cam = camera_mat * v
                    face_vertices_cam.append(v_cam)
                    if v_cam.z <= 0:
                        continue  # Отсекаем то, что за камерой

                    factor = 500 / v_cam.z
                    px = (v_cam.x * factor) / aspect + width / 2
                    # px = v_cam.x * factor + width / 2
                    py = -v_cam.y * factor + height / 2  # Инвертируем Y для экрана
                    screen_points.append(QPointF(px, py))

                if len(screen_points) < 3:
                    continue

                center_cam = Vector3D(0, 0, 0, 1)
                for v_cam in face_vertices_cam:
                    center_cam += v_cam
                center_cam = Vector3D(
                    center_cam.x / len(face_vertices_cam),
                    center_cam.y / len(face_vertices_cam),
                    center_cam.z / len(face_vertices_cam),
                    1,
                )
                avg_z = center_cam.z
                self.cached_faces.append(
                    {
                        "depth": avg_z,
                        "face": face,
                        "polygon": QPolygonF(screen_points),
                        "center": center_cam,
                    }
                )

        self.cached_faces.sort(key=lambda x: x["depth"])

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        painter.fillRect(self.rect(), QColor(30, 30, 30))

        if not self.cache_valid:
            self.prepare_faces_cache()
            self.cache_valid = True

        for item in self.cached_faces:
            face = item["face"]
            poly = item["polygon"]

            if self.display_mode == DisplayMode.POINTS:
                painter.setPen(QPen(face.color, 1))
                painter.setBrush(QBrush(face.color))

                for i in range(poly.count()):
                    point = poly.at(i)
                    painter.drawEllipse(point, 2, 2)

            elif self.display_mode == DisplayMode.WIREFRAME:
                painter.setPen(QPen(face.color, 1))
                painter.setBrush(Qt.NoBrush)
                painter.drawPolygon(poly)

            elif self.display_mode == DisplayMode.FILLED:
                normal = face.calculate_normal()
                light_dir = (self.light_pos - item["center"]).normalized()
                diffuse = max(0.2, normal.dot(light_dir))

                base = face.color
                if self.shading_mode == ShadingMode.MONO:
                    k = diffuse
                elif self.shading_mode == ShadingMode.GOURAUD:
                    k = 0.5 + 0.5 * diffuse
                else:  # PHONG
                    k = 0.3 + 0.7 * diffuse * diffuse

                k = max(0.0, min(1.0, k))
                bright_color = QColor(
                    int(base.red() * k),
                    int(base.green() * k),
                    int(base.blue() * k),
                )

                painter.setPen(QPen(bright_color, 1))
                painter.setBrush(QBrush(bright_color))
                painter.drawPolygon(poly)

    def rotate_scene(self, ax, angle):
        self.d_letter.rotate(ax, angle)
        self.b_letter.rotate(ax, angle)
        self.cache_valid = False
        self.update()

    def set_mirror(self, axis):
        if axis == 0:
            mirror = Matrix4x4.scaling(-1, 1, 1)
        else:
            mirror = Matrix4x4.scaling(1, -1, 1)
        self.d_letter.transform = mirror * self.d_letter.transform
        self.b_letter.transform = mirror * self.b_letter.transform
        self.invalidate_cache()
        self.update()

    def set_display_mode(self, mode):
        self.display_mode = mode
        self.update()

    def set_shading_mode(self, mode):
        self.shading_mode = mode
        self.update()

    def rotate_letter(self, letter_obj, axis, angle):
        letter_obj.rotate(axis, angle)
        self.invalidate_cache()
        self.update()

    def scale_letter(self, letter_obj, scale_factor):
        letter_obj.set_scale(scale_factor)
        self.invalidate_cache()
        self.update()
