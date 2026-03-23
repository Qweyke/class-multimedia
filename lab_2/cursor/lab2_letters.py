from PySide6.QtGui import QColor
from lab2_math import Vector3D, Matrix4x4
from lab2_geometry import Face


class Letter3D:
    def __init__(self, height, width, depth, offset_x, letter_type):
        self.height = height
        self.width = width
        self.depth = depth
        self.offset_x = offset_x
        self.letter_type = letter_type

        self.faces = []  # Список граней в локальных координатах
        self.transform = Matrix4x4()  # Матрица поворота и положения
        self.scale = 1.0

        self.update_geometry()

    def update_geometry(self):
        """Создает каркас буквы в локальных координатах"""
        self.faces = []
        h, w, d, ox = self.height, self.width, self.depth, self.offset_x
        bar = h * 0.2  # Толщина линий буквы

        if self.letter_type == "Д":
            self.create_letter_D(h, w, d, ox, bar)
        elif self.letter_type == "Б":
            self.create_letter_B(h, w, d, ox, bar)

    def _create_faces_for_part(self, front, back, colors):
        """
        Создает 6 граней параллелепипеда по 4 передним и 4 задним точкам.
        Следит за порядком вершин, чтобы нормали смотрели НАРУЖУ.
        """
        # Передняя грань (против часовой стрелки)
        self.faces.append(Face([front[0], front[1], front[2], front[3]], colors[0]))
        # Задняя грань (по часовой стрелке, чтобы нормаль смотрела назад)
        self.faces.append(Face([back[0], back[3], back[2], back[1]], colors[0]))

        # Боковые грани
        for i in range(4):
            next_i = (i + 1) % 4
            # Соединяем ребра передней и задней части
            side = [front[i], back[i], back[next_i], front[next_i]]
            self.faces.append(Face(side, colors[1]))

    def create_letter_D(self, h, w, d, ox, bar_thickness):

        hw = w / 2
        hd = d / 2
        mid_y = h / 2
        extra = bar_thickness  # выступ средней линии за вертикальные линии

        # Верхняя часть левой вертикальной линии (до средней линии)
        front_left_top = [
            Vector3D(ox - hw, h, -hd),
            Vector3D(ox - hw + bar_thickness, h, -hd),
            Vector3D(ox - hw + bar_thickness, mid_y + bar_thickness / 2, -hd),
            Vector3D(ox - hw, mid_y + bar_thickness / 2, -hd),
        ]
        back_left_top = [
            Vector3D(ox - hw, h, hd),
            Vector3D(ox - hw + bar_thickness, h, hd),
            Vector3D(ox - hw + bar_thickness, mid_y + bar_thickness / 2, hd),
            Vector3D(ox - hw, mid_y + bar_thickness / 2, hd),
        ]

        # Верхняя часть правой вертикальной линии (до средней линии)
        front_right_top = [
            Vector3D(ox + hw - bar_thickness, h, -hd),
            Vector3D(ox + hw, h, -hd),
            Vector3D(ox + hw, mid_y + bar_thickness / 2, -hd),
            Vector3D(ox + hw - bar_thickness, mid_y + bar_thickness / 2, -hd),
        ]
        back_right_top = [
            Vector3D(ox + hw - bar_thickness, h, hd),
            Vector3D(ox + hw, h, hd),
            Vector3D(ox + hw, mid_y + bar_thickness / 2, hd),
            Vector3D(ox + hw - bar_thickness, mid_y + bar_thickness / 2, hd),
        ]

        # Верхняя горизонтальная линия
        front_top = [
            Vector3D(ox - hw + bar_thickness, h, -hd),
            Vector3D(ox + hw, h, -hd),
            Vector3D(ox + hw, h - bar_thickness, -hd),
            Vector3D(ox - hw + bar_thickness, h - bar_thickness, -hd),
        ]
        back_top = [
            Vector3D(ox - hw + bar_thickness, h, hd),
            Vector3D(ox + hw, h, hd),
            Vector3D(ox + hw, h - bar_thickness, hd),
            Vector3D(ox - hw + bar_thickness, h - bar_thickness, hd),
        ]

        # Средняя горизонтальная линия
        front_middle = [
            Vector3D(ox - hw - extra, mid_y + bar_thickness / 2, -hd),
            Vector3D(ox + hw + extra, mid_y + bar_thickness / 2, -hd),
            Vector3D(ox + hw + extra, mid_y - bar_thickness / 2, -hd),
            Vector3D(ox - hw - extra, mid_y - bar_thickness / 2, -hd),
        ]
        back_middle = [
            Vector3D(ox - hw - extra, mid_y + bar_thickness / 2, hd),
            Vector3D(ox + hw + extra, mid_y + bar_thickness / 2, hd),
            Vector3D(ox + hw + extra, mid_y - bar_thickness / 2, hd),
            Vector3D(ox - hw - extra, mid_y - bar_thickness / 2, hd),
        ]

        # Нижние боковые линии (от краёв средней линии вниз)
        front_left_bottom = [
            Vector3D(ox - hw - extra, mid_y - bar_thickness / 2, -hd),
            Vector3D(ox - hw - extra + bar_thickness, mid_y - bar_thickness / 2, -hd),
            Vector3D(ox - hw - extra + bar_thickness, 0, -hd),
            Vector3D(ox - hw - extra, 0, -hd),
        ]
        back_left_bottom = [
            Vector3D(ox - hw - extra, mid_y - bar_thickness / 2, hd),
            Vector3D(ox - hw - extra + bar_thickness, mid_y - bar_thickness / 2, hd),
            Vector3D(ox - hw - extra + bar_thickness, 0, hd),
            Vector3D(ox - hw - extra, 0, hd),
        ]

        front_right_bottom = [
            Vector3D(ox + hw + extra - bar_thickness, mid_y - bar_thickness / 2, -hd),
            Vector3D(ox + hw + extra, mid_y - bar_thickness / 2, -hd),
            Vector3D(ox + hw + extra, 0, -hd),
            Vector3D(ox + hw + extra - bar_thickness, 0, -hd),
        ]
        back_right_bottom = [
            Vector3D(ox + hw + extra - bar_thickness, mid_y - bar_thickness / 2, hd),
            Vector3D(ox + hw + extra, mid_y - bar_thickness / 2, hd),
            Vector3D(ox + hw + extra, 0, hd),
            Vector3D(ox + hw + extra - bar_thickness, 0, hd),
        ]

        # Объединяем все вершины
        self.vertices = (
            front_left_top
            + back_left_top
            + front_right_top
            + back_right_top
            + front_top
            + back_top
            + front_middle
            + back_middle
            + front_left_bottom
            + back_left_bottom
            + front_right_bottom
            + back_right_bottom
        )

        colors = [QColor(0, 102, 204), QColor(0, 82, 163), QColor(0, 61, 122)]

        # Создание граней
        self._create_faces_for_part(front_left_top, back_left_top, colors)
        self._create_faces_for_part(front_right_top, back_right_top, colors)
        self._create_faces_for_part(front_top, back_top, colors)
        self._create_faces_for_part(front_middle, back_middle, colors)
        self._create_faces_for_part(front_left_bottom, back_left_bottom, colors)
        self._create_faces_for_part(front_right_bottom, back_right_bottom, colors)

    def create_letter_B(self, h, w, d, ox, bar):
        """Создание геометрии буквы Б."""
        hw, hd = w / 2, d / 2
        colors = [QColor(0, 102, 204), QColor(0, 72, 143)]

        # Левая вертикальная стойка
        f_left = [
            Vector3D(ox - hw, h, -hd),
            Vector3D(ox - hw + bar, h, -hd),
            Vector3D(ox - hw + bar, 0, -hd),
            Vector3D(ox - hw, 0, -hd),
        ]
        b_left = [
            Vector3D(ox - hw, h, hd),
            Vector3D(ox - hw + bar, h, hd),
            Vector3D(ox - hw + bar, 0, hd),
            Vector3D(ox - hw, 0, hd),
        ]
        self._create_faces_for_part(f_left, b_left, colors)

        # Верхняя перекладина
        f_top = [
            Vector3D(ox - hw + bar, h, -hd),
            Vector3D(ox + hw, h, -hd),
            Vector3D(ox + hw, h - bar, -hd),
            Vector3D(ox - hw + bar, h - bar, -hd),
        ]
        b_top = [
            Vector3D(ox - hw + bar, h, hd),
            Vector3D(ox + hw, h, hd),
            Vector3D(ox + hw, h - bar, hd),
            Vector3D(ox - hw + bar, h - bar, hd),
        ]
        self._create_faces_for_part(f_top, b_top, colors)

        # Нижняя перекладина
        f_bot = [
            Vector3D(ox - hw + bar, bar, -hd),
            Vector3D(ox + hw, bar, -hd),
            Vector3D(ox + hw, 0, -hd),
            Vector3D(ox - hw + bar, 0, -hd),
        ]
        b_bot = [
            Vector3D(ox - hw + bar, bar, hd),
            Vector3D(ox + hw, bar, hd),
            Vector3D(ox + hw, 0, hd),
            Vector3D(ox - hw + bar, 0, hd),
        ]
        self._create_faces_for_part(f_bot, b_bot, colors)

        # Средняя горизонтальная перекладина
        mid_y = h / 2
        f_mid = [
            Vector3D(ox - hw + bar, mid_y + bar / 2, -hd),
            Vector3D(ox + hw, mid_y + bar / 2, -hd),
            Vector3D(ox + hw, mid_y - bar / 2, -hd),
            Vector3D(ox - hw + bar, mid_y - bar / 2, -hd),
        ]
        b_mid = [
            Vector3D(ox - hw + bar, mid_y + bar / 2, hd),
            Vector3D(ox + hw, mid_y + bar / 2, hd),
            Vector3D(ox + hw, mid_y - bar / 2, hd),
            Vector3D(ox - hw + bar, mid_y - bar / 2, hd),
        ]
        self._create_faces_for_part(f_mid, b_mid, colors)

        # Правая укороченная стойка
        f_right = [
            Vector3D(ox + hw - bar, mid_y, -hd),
            Vector3D(ox + hw, mid_y, -hd),
            Vector3D(ox + hw, 0, -hd),
            Vector3D(ox + hw - bar, 0, -hd),
        ]
        b_right = [
            Vector3D(ox + hw - bar, mid_y, hd),
            Vector3D(ox + hw, mid_y, hd),
            Vector3D(ox + hw, 0, hd),
            Vector3D(ox + hw - bar, 0, hd),
        ]
        self._create_faces_for_part(f_right, b_right, colors)

    def get_transformed_faces(self):
        """
        Применяет текущую матрицу трансформации к каждой вершине.
        Возвращает новый список граней, готовых к отрисовке.
        """
        # Сначала масштабируем, потом применяем вращение/перенос
        final_mat = (
            Matrix4x4.scaling(self.scale, self.scale, self.scale) * self.transform
        )

        transformed_faces = []
        for face in self.faces:
            # Умножаем каждую вершину (Vector3D) на матрицу
            new_verts = [final_mat * v for v in face.vertices]
            # Создаем временную грань для рендеринга
            transformed_faces.append(Face(new_verts, face.color))
        return transformed_faces

    def rotate(self, axis, angle):
        """Накапливает вращение в матрице трансформации"""
        if axis == 0:
            rot = Matrix4x4.rotation_x(angle)
        elif axis == 1:
            rot = Matrix4x4.rotation_y(angle)
        else:
            rot = Matrix4x4.rotation_z(angle)

        # Перемножаем матрицы, чтобы сохранить предыдущие повороты
        self.transform = rot * self.transform

    def translate(self, dx, dy, dz):
        """Смещает букву в пространстве"""
        move = Matrix4x4.translation(dx, dy, dz)
        self.transform = move * self.transform

    def set_scale(self, s):
        self.scale = s
