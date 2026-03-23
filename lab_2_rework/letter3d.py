from math_utils import Vector3D
from face import Face
from PySide6.QtGui import QColor


class Letter3D:
    def __init__(self, height, width, depth, offset_x, letter_type):
        self.height = height
        self.width = width
        self.depth = depth
        self.offset_x = offset_x
        self.letter_type = letter_type
        self.vertices = []
        self.faces = []
        self.update_geometry()

    def update_geometry(self):
        self.vertices = []
        self.faces = []
        h, w, d, ox = self.height, self.width, self.depth, self.offset_x
        bar_thickness = h * 0.2

        if self.letter_type == "D":
            self._create_letter_D(h, w, d, ox, bar_thickness)
        elif self.letter_type == "B":
            self._create_letter_B(h, w, d, ox, bar_thickness)

    def _create_letter_T1(self, h, w, d, ox, bar_thickness):
        hw = w / 2
        hd = d / 2
        vw = w / 6
        front_top = [
            Vector3D(ox - hw, h, -hd),
            Vector3D(ox + hw, h, -hd),
            Vector3D(ox + hw, h - bar_thickness, -hd),
            Vector3D(ox - hw, h - bar_thickness, -hd),
        ]
        back_top = [
            Vector3D(ox - hw, h, hd),
            Vector3D(ox + hw, h, hd),
            Vector3D(ox + hw, h - bar_thickness, hd),
            Vector3D(ox - hw, h - bar_thickness, hd),
        ]
        front_vert = [
            Vector3D(ox - vw, h - bar_thickness, -hd),
            Vector3D(ox + vw, h - bar_thickness, -hd),
            Vector3D(ox + vw, 0, -hd),
            Vector3D(ox - vw, 0, -hd),
        ]
        back_vert = [
            Vector3D(ox - vw, h - bar_thickness, hd),
            Vector3D(ox + vw, h - bar_thickness, hd),
            Vector3D(ox + vw, 0, hd),
            Vector3D(ox - vw, 0, hd),
        ]
        self.vertices = front_top + back_top + front_vert + back_vert
        colors = [QColor(255, 140, 0), QColor(255, 165, 0), QColor(255, 127, 80)]
        self._create_faces_for_part(front_top, back_top, colors)
        self._create_faces_for_part(front_vert, back_vert, colors)
        self.faces.append(
            Face([front_top[2], front_top[3], front_vert[0], front_vert[1]], colors[1])
        )
        self.faces.append(
            Face([back_top[2], back_top[3], back_vert[0], back_vert[1]], colors[1])
        )

    def _create_letter_B(self, h, w, d, ox, bar_thickness):
        hw = w / 2
        hd = d / 2
        mid_y = h / 2
        bar = bar_thickness

        # 1. Зеркальная Вертикальная "спина" (теперь справа в коде)
        f_spine = [
            Vector3D(ox + hw - bar, h, -hd),
            Vector3D(ox + hw, h, -hd),
            Vector3D(ox + hw, 0, -hd),
            Vector3D(ox + hw - bar, 0, -hd),
        ]
        b_spine = [Vector3D(v.x, v.y, hd) for v in f_spine]

        # 2. Зеркальная Верхняя горизонтальная полка (выступает влево)
        f_top = [
            Vector3D(ox - hw, h, -hd),
            Vector3D(ox + hw - bar, h, -hd),
            Vector3D(ox + hw - bar, h - bar, -hd),
            Vector3D(ox - hw, h - bar, -hd),
        ]
        b_top = [Vector3D(v.x, v.y, hd) for v in f_top]

        # 3. Зеркальное Нижнее "пузо" (Горизонтальный низ, выступает влево)
        f_bottom = [
            Vector3D(ox - hw, bar, -hd),
            Vector3D(ox + hw - bar, bar, -hd),
            Vector3D(ox + hw - bar, 0, -hd),
            Vector3D(ox - hw, 0, -hd),
        ]
        b_bottom = [Vector3D(v.x, v.y, hd) for v in f_bottom]

        # 4. Зеркальная Правая стенка "пуза" (теперь слева в коде)
        f_right = [
            Vector3D(ox - hw, mid_y, -hd),
            Vector3D(ox - hw + bar, mid_y, -hd),
            Vector3D(ox - hw + bar, bar, -hd),
            Vector3D(ox - hw, bar, -hd),
        ]
        b_right = [Vector3D(v.x, v.y, hd) for v in f_right]

        # 5. Зеркальная Средняя перекладина (крышка пуза)
        f_mid = [
            Vector3D(ox - hw + bar, mid_y, -hd),
            Vector3D(ox + hw - bar, mid_y, -hd),
            Vector3D(ox + hw - bar, mid_y - bar, -hd),
            Vector3D(ox - hw + bar, mid_y - bar, -hd),
        ]
        b_mid = [Vector3D(v.x, v.y, hd) for v in f_mid]

        self.vertices += (
            f_spine
            + b_spine
            + f_top
            + b_top
            + f_bottom
            + b_bottom
            + f_right
            + b_right
            + f_mid
            + b_mid
        )
        colors = [
            QColor(0, 102, 204),
            QColor(0, 82, 163),
            QColor(0, 61, 122),
        ]  # Все грани синие

        self._create_faces_for_part(f_spine, b_spine, colors)
        self._create_faces_for_part(f_top, b_top, colors)
        self._create_faces_for_part(f_bottom, b_bottom, colors)
        self._create_faces_for_part(f_right, b_right, colors)
        self._create_faces_for_part(f_mid, b_mid, colors)

    def _create_letter_D(self, h, w, d, ox, bar_thickness):
        hw = w / 2
        hd = d / 2
        bar = bar_thickness

        # Base height is 20% of total height
        base_h = h * 0.2

        # 1. Extended Bottom Base Bar
        # The x-coordinates are shifted by +/- bar to make it wider
        f_base = [
            Vector3D(ox - hw - bar, base_h, -hd),  # Left extension
            Vector3D(ox + hw + bar, base_h, -hd),  # Right extension
            Vector3D(ox + hw + bar, 0, -hd),
            Vector3D(ox - hw - bar, 0, -hd),
        ]
        b_base = [Vector3D(v.x, v.y, hd) for v in f_base]

        # 2. Left Vertical Leg (Stands on the base)
        f_left_leg = [
            Vector3D(ox - hw, h, -hd),
            Vector3D(ox - hw + bar, h, -hd),
            Vector3D(ox - hw + bar, base_h, -hd),
            Vector3D(ox - hw, base_h, -hd),
        ]
        b_left_leg = [Vector3D(v.x, v.y, hd) for v in f_left_leg]

        # 3. Right Vertical Leg (Stands on the base)
        f_right_leg = [
            Vector3D(ox + hw - bar, h, -hd),
            Vector3D(ox + hw, h, -hd),
            Vector3D(ox + hw, base_h, -hd),
            Vector3D(ox + hw - bar, base_h, -hd),
        ]
        b_right_leg = [Vector3D(v.x, v.y, hd) for v in f_right_leg]

        # 4. Top Horizontal Bar
        f_top_bar = [
            Vector3D(ox - hw + bar, h, -hd),
            Vector3D(ox + hw - bar, h, -hd),
            Vector3D(ox + hw - bar, h - bar, -hd),
            Vector3D(ox - hw + bar, h - bar, -hd),
        ]
        b_top_bar = [Vector3D(v.x, v.y, hd) for v in f_top_bar]

        # Update vertices list
        self.vertices = (
            f_base
            + b_base
            + f_left_leg
            + b_left_leg
            + f_right_leg
            + b_right_leg
            + f_top_bar
            + b_top_bar
        )

        colors = [QColor(0, 102, 204), QColor(0, 82, 163), QColor(0, 61, 122)]

        # Rendering segments
        self._create_faces_for_part(f_base, b_base, colors)
        self._create_faces_for_part(f_left_leg, b_left_leg, colors)
        self._create_faces_for_part(f_right_leg, b_right_leg, colors)
        self._create_faces_for_part(f_top_bar, b_top_bar, colors)

    def _create_letter_V1(self, h, w, d, ox, bar_thickness):
        hw = w / 2
        hd = d / 2
        front_left = [
            Vector3D(ox - hw, h, -hd),
            Vector3D(ox - hw + bar_thickness, h, -hd),
            Vector3D(ox, 0, -hd),
            Vector3D(ox - bar_thickness, 0, -hd),
        ]
        back_left = [
            Vector3D(ox - hw, h, hd),
            Vector3D(ox - hw + bar_thickness, h, hd),
            Vector3D(ox, 0, hd),
            Vector3D(ox - bar_thickness, 0, hd),
        ]
        front_right = [
            Vector3D(ox + hw - bar_thickness, h, -hd),
            Vector3D(ox + hw, h, -hd),
            Vector3D(ox + bar_thickness, 0, -hd),
            Vector3D(ox, 0, -hd),
        ]
        back_right = [
            Vector3D(ox + hw - bar_thickness, h, hd),
            Vector3D(ox + hw, h, hd),
            Vector3D(ox + bar_thickness, 0, hd),
            Vector3D(ox, 0, hd),
        ]
        self.vertices = front_left + back_left + front_right + back_right
        colors = [QColor(255, 140, 0), QColor(255, 165, 0), QColor(255, 127, 80)]
        self._create_faces_for_part(front_left, back_left, colors)
        self._create_faces_for_part(front_right, back_right, colors)

    def _create_faces_for_part(self, front_vertices, back_vertices, colors):
        self.faces.append(Face(front_vertices, colors[0]))
        self.faces.append(Face(back_vertices, colors[0]))
        for i in range(len(front_vertices)):
            next_i = (i + 1) % len(front_vertices)
            side_face = [
                front_vertices[i],
                front_vertices[next_i],
                back_vertices[next_i],
                back_vertices[i],
            ]
            self.faces.append(Face(side_face, colors[1]))
        if len(front_vertices) >= 4:
            top_face = [
                front_vertices[0],
                front_vertices[1],
                back_vertices[1],
                back_vertices[0],
            ]
            bottom_face = [
                front_vertices[2],
                front_vertices[3],
                back_vertices[3],
                back_vertices[2],
            ]
            self.faces.append(Face(top_face, colors[2]))
            self.faces.append(Face(bottom_face, colors[2]))
