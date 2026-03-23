from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QPen, QBrush, QColor, QPolygonF, QLinearGradient
from PySide6.QtCore import Qt, QPoint, QPointF
from math_utils import Vector3D, Matrix4x4
from letter3d import Letter3D
from enums import DisplayMode, ShadingMode


class SceneWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), QColor(50, 50, 50))
        self.setPalette(p)
        self.d_letter = Letter3D(100, 60, 30, offset_x=60, letter_type="D")
        self.b_letter = Letter3D(100, 60, 30, offset_x=-60, letter_type="B")
        self.camera_pos = Vector3D(0, 0, -400)
        self.camera_rot = [0, 0, 0]
        self.object_transform = Matrix4x4.rotation_z(180)
        self.scale = 1.0
        self.base_scale = 1.4
        self.auto_scale = True
        self.light_dir = Vector3D(0.5, 0.5, -1).normalized()
        self.light_pos = self.light_dir * 150
        self.display_mode = DisplayMode.FILLED
        self.shading_mode = ShadingMode.MONOTONE
        self.mirror_x = False
        self.mirror_y = False
        self.mirror_z = False
        self.last_mouse_pos = None
        self.is_rotating = False
        self.rotation_speed = 0.5

    def compute_phong_lighting(self, normal, position):
        ambient_strength = 0.2
        diffuse_strength = 0.8
        specular_strength = 0.5
        shininess = 32

        light_dir = self.light_dir
        view_dir = (self.camera_pos - position).normalized()

        world_normal = self.object_transform * normal
        world_normal = world_normal.normalized()

        cos_theta = world_normal.dot(light_dir)

        if cos_theta < 0:
            return ambient_strength

        diffuse = diffuse_strength * cos_theta

        reflect_dir = (
            light_dir - world_normal * (2 * world_normal.dot(light_dir))
        ).normalized()

        specular = specular_strength * max(0, reflect_dir.dot(view_dir)) ** shininess

        intensity = ambient_strength + diffuse + specular

        return min(1.0, max(0.2, intensity))

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), QColor(50, 50, 50))
        # self.draw_axes(painter)

        all_faces = []

        t_faces = self._prepare_letter_faces(self.b_letter)
        all_faces.extend(t_faces)

        v_faces = self._prepare_letter_faces(self.d_letter)
        all_faces.extend(v_faces)

        all_faces.sort(reverse=True, key=lambda x: x[0])

        for (
            depth,
            face,
            screen_points,
            intensities,
            positions,
            face_normals,
        ) in all_faces:
            if len(screen_points) >= 3:
                if self.display_mode == DisplayMode.POINTS:
                    painter.setPen(QPen(face.color, 5))
                    for point in screen_points:
                        if point.x() != -1000 and point.y() != -1000:
                            painter.drawPoint(point)
                elif self.display_mode == DisplayMode.WIREFRAME:
                    polygon = QPolygonF(screen_points)
                    painter.setPen(QPen(face.color, 2))
                    painter.setBrush(Qt.NoBrush)
                    painter.drawPolygon(polygon)
                elif self.display_mode == DisplayMode.FILLED:
                    self._draw_filled_face(
                        painter,
                        face,
                        screen_points,
                        intensities,
                        positions,
                        face_normals,
                    )

        self.draw_light_source(painter)

    def _prepare_letter_faces(self, letter):
        faces_with_depth = []
        transformed_vertices = []
        vertex_normals = []

        mirror_matrix = Matrix4x4.scaling(
            -1 if self.mirror_x else 1,
            -1 if self.mirror_y else 1,
            -1 if self.mirror_z else 1,
        )

        for v in letter.vertices:
            v_mirrored = mirror_matrix * v
            v_transformed = self.object_transform * v_mirrored
            v_camera = self.apply_camera_transform(v_transformed)
            transformed_vertices.append(v_camera)

            normal_sum = Vector3D(0, 0, 0)
            count = 0
            for face in letter.faces:
                if v in face.vertices:
                    normal_sum = normal_sum + face.normal
                    count += 1
            vertex_normals.append(
                normal_sum.normalized() if count > 0 else Vector3D(0, 0, 1)
            )

        for face in letter.faces:
            face_vertices = [
                transformed_vertices[letter.vertices.index(v)] for v in face.vertices
            ]
            face_normals = [
                vertex_normals[letter.vertices.index(v)] for v in face.vertices
            ]

            avg_depth = sum(v.z for v in face_vertices) / len(face_vertices)

            screen_points = []
            intensities = []
            positions = []

            for i, v in enumerate(face_vertices):
                if v.z > 0:
                    factor = 300 / v.z
                    aspect_ratio = self.width() / self.height()
                    px = (
                        v.x
                        * factor
                        * self.base_scale
                        * (1 / aspect_ratio if aspect_ratio > 1 else 1)
                        + self.width() / 2
                    )
                    py = (
                        v.y
                        * factor
                        * self.base_scale
                        * (1 if aspect_ratio > 1 else aspect_ratio)
                        + self.height() / 2
                    )
                    screen_points.append(QPointF(px, py))
                    intensity = self.compute_phong_lighting(face_normals[i], v)
                    intensities.append(intensity)
                    positions.append(v)
                else:
                    screen_points.append(QPointF(-1000, -1000))
                    intensities.append(0)
                    positions.append(Vector3D(0, 0, 0))

            faces_with_depth.append(
                (avg_depth, face, screen_points, intensities, positions, face_normals)
            )

        return faces_with_depth

    def _draw_filled_face(
        self, painter, face, screen_points, intensities, positions, face_normals
    ):
        if len(screen_points) < 3:
            return

        if self.shading_mode == ShadingMode.MONOTONE:
            world_normal = self.object_transform * face.normal
            world_normal = world_normal.normalized()
            intensity = max(0.3, world_normal.dot(self.light_dir))
            color = QColor(
                min(255, int(face.color.red() * intensity)),
                min(255, int(face.color.green() * intensity)),
                min(255, int(face.color.blue() * intensity)),
            )
            painter.setPen(QPen(Qt.black, 1))
            painter.setBrush(QBrush(color))
            painter.drawPolygon(QPolygonF(screen_points))

    def draw_axes(self, painter):
        origin = self.project_point(Vector3D(0, 0, 0))
        x_end = self.project_point(Vector3D(150, 0, 0))
        y_end = self.project_point(Vector3D(0, 150, 0))
        z_end = self.project_point(Vector3D(0, 0, 150))
        painter.setPen(QPen(Qt.red, 2))
        painter.drawLine(origin, x_end)
        painter.drawText(x_end + QPoint(5, 5), "X")
        painter.setPen(QPen(Qt.green, 2))
        painter.drawLine(origin, y_end)
        painter.drawText(y_end + QPoint(5, 5), "Y")
        painter.setPen(QPen(Qt.blue, 2))
        painter.drawLine(origin, z_end)
        painter.drawText(z_end + QPoint(5, 5), "Z")

    def draw_light_source(self, painter):
        light_pos = self.light_pos
        screen_pos = self.project_point(light_pos)
        if screen_pos.x() != -1000 and screen_pos.y() != -1000:
            painter.setPen(QPen(Qt.white, 1))
            painter.setBrush(QBrush(Qt.white))
            painter.drawEllipse(screen_pos, 5, 5)

    def project_point(self, point):
        v_transformed = self.object_transform * point
        v_camera = self.apply_camera_transform(v_transformed)
        if v_camera.z > 0:
            factor = 300 / v_camera.z
            aspect_ratio = self.width() / self.height()
            px = (
                v_camera.x
                * factor
                * self.base_scale
                * (1 / aspect_ratio if aspect_ratio > 1 else 1)
                + self.width() / 2
            )
            py = (
                v_camera.y
                * factor
                * self.base_scale
                * (1 if aspect_ratio > 1 else aspect_ratio)
                + self.height() / 2
            )
            return QPoint(int(px), int(py))
        return QPoint(-1000, -1000)

    def apply_camera_transform(self, v):
        rot_x = Matrix4x4.rotation_x(self.camera_rot[0])
        rot_y = Matrix4x4.rotation_y(self.camera_rot[1])
        rot_z = Matrix4x4.rotation_z(self.camera_rot[2])
        rotation = rot_x * rot_y * rot_z
        translation = Matrix4x4.translation(
            -self.camera_pos.x, -self.camera_pos.y, -self.camera_pos.z
        )
        camera_transform = rotation * translation
        return camera_transform * v

    def auto_scale_view(self):
        if self.auto_scale:
            self.base_scale = min(self.width(), self.height()) / 600.0

    def resizeEvent(self, event):
        self.auto_scale_view()
        super().resizeEvent(event)

    def set_mirror(self, axis):
        if axis == 0:
            self.mirror_x = not self.mirror_x
        elif axis == 1:
            self.mirror_y = not self.mirror_y
        else:
            self.mirror_z = not self.mirror_z
        self.update()

    def set_light_direction(self, x, y, z):
        self.light_dir = Vector3D(x, y, z).normalized()
        self.light_pos = self.light_dir * 150
        self.update()

    def set_display_mode(self, mode):
        self.display_mode = mode
        self.update()

    def set_shading_mode(self, mode):
        self.shading_mode = mode
        self.update()

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            self.is_rotating = True
            self.last_mouse_pos = event.position()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.RightButton:
            self.is_rotating = False
            self.last_mouse_pos = None

    def mouseMoveEvent(self, event):
        if self.is_rotating and self.last_mouse_pos:
            delta = -(event.position() - self.last_mouse_pos)
            rot_x = Matrix4x4.rotation_x(-delta.y() * self.rotation_speed)
            rot_y = Matrix4x4.rotation_y(delta.x() * self.rotation_speed)
            self.object_transform = rot_y * rot_x * self.object_transform
            self.last_mouse_pos = event.position()
            self.update()

    def wheelEvent(self, event):
        delta = event.angleDelta().y()
        if delta > 0:
            self.base_scale *= 1.1
        else:
            self.base_scale /= 1.1
        self.update()
