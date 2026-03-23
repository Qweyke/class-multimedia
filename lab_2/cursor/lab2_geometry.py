from lab2_math import Vector3D


class Face:
    def __init__(self, vertices, color):
        self.vertices = vertices
        self.color = color

    def calculate_normal(self):
        """Вычисляет перпендикуляр к грани по трем точкам"""
        if len(self.vertices) < 3:
            return Vector3D(0, 0, 0, 0)

        # Берем две стороны грани (векторы)
        v1 = self.vertices[1] - self.vertices[0]
        v2 = self.vertices[2] - self.vertices[0]

        # Векторное произведение дает перпендикуляр (нормаль)
        # Важен порядок (v1 x v2), он определяет, куда смотрит "лицо"
        return v1.cross(v2).normalized()

    def calculate_center(self):
        """Находит среднюю точку грани (нужно для сортировки и видимости)"""
        count = len(self.vertices)
        if count == 0:
            return Vector3D(0, 0, 0, 1)

        sx = sum(v.x for v in self.vertices) / count
        sy = sum(v.y for v in self.vertices) / count
        sz = sum(v.z for v in self.vertices) / count
        return Vector3D(sx, sy, sz, 1)

    def is_visible(self, camera_pos):
        """Алгоритм отсечения невидимых граней (Back-face culling)"""
        current_normal = self.calculate_normal()
        current_center = self.calculate_center()

        # Вектор взгляда от камеры к объекту
        view_dir = (current_center - camera_pos).normalized()

        # Скалярное произведение:
        # Если < 0, угол между нормалью и взглядом > 90 градусов (грань смотрит на нас)
        return current_normal.dot(view_dir) < 0
