import math


class Vector3D:
    def __init__(self, x=0, y=0, z=0, w=1):
        self.x = x
        self.y = y
        self.z = z
        self.w = w  # 1 для точек, 0 для векторов

    def __add__(self, other):
        # Точка + Вектор = Точка. Вектор + Вектор = Вектор.
        return Vector3D(self.x + other.x, self.y + other.y, self.z + other.z, self.w)

    def __sub__(self, other):
        # Точка - Точка = Вектор (w становится 0)
        new_w = 1 if self.w != other.w else 0
        return Vector3D(self.x - other.x, self.y - other.y, self.z - other.z, new_w)

    def __mul__(self, scalar):
        # Масштабируем только направление, не трогаем тип объекта (w)
        return Vector3D(self.x * scalar, self.y * scalar, self.z * scalar, self.w)

    def length(self):
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)

    def normalized(self):
        l = self.length()
        if l == 0:
            return Vector3D(0, 0, 0, 0)
        return Vector3D(self.x / l, self.y / l, self.z / l, 0)

    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other):
        # Векторное произведение - критично для вычисления нормалей граней
        return Vector3D(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x,
            0,  # Результат всегда вектор
        )


class Matrix4x4:
    def __init__(self):
        # Создаем единичную матрицу (Identity)
        self.m = [[0.0] * 4 for _ in range(4)]
        for i in range(4):
            self.m[i][i] = 1.0

    def __mul__(self, other):
        if isinstance(other, Vector3D):
            # Полноценное умножение 4x4 на 1x4
            # Заметь: теперь везде умножаем на other.w!
            x = (
                self.m[0][0] * other.x
                + self.m[0][1] * other.y
                + self.m[0][2] * other.z
                + self.m[0][3] * other.w
            )

            y = (
                self.m[1][0] * other.x
                + self.m[1][1] * other.y
                + self.m[1][2] * other.z
                + self.m[1][3] * other.w
            )

            z = (
                self.m[2][0] * other.x
                + self.m[2][1] * other.y
                + self.m[2][2] * other.z
                + self.m[2][3] * other.w
            )

            w = (
                self.m[3][0] * other.x
                + self.m[3][1] * other.y
                + self.m[3][2] * other.z
                + self.m[3][3] * other.w
            )

            # Делаем перспективное деление только если w не 1 и не 0
            if w != 0 and w != 1:
                return Vector3D(x / w, y / w, z / w, 1)
            return Vector3D(x, y, z, w)

        elif isinstance(other, Matrix4x4):
            # Склеивание двух трансформаций в одну
            res = Matrix4x4()
            for i in range(4):
                for j in range(4):
                    res.m[i][j] = sum(self.m[i][k] * other.m[k][j] for k in range(4))
            return res

    @staticmethod
    def translation(x, y, z):
        mat = Matrix4x4()
        mat.m[0][3] = x  # Тот самый "оранжевый столбец"
        mat.m[1][3] = y
        mat.m[2][3] = z
        return mat

    @staticmethod
    def rotation_x(angle):
        mat = Matrix4x4()
        rad = math.radians(angle)
        c, s = math.cos(rad), math.sin(rad)
        # Ось X остается неподвижной (1, 0, 0), меняются Y и Z
        mat.m[1][1], mat.m[1][2] = c, -s
        mat.m[2][1], mat.m[2][2] = s, c
        return mat

    @staticmethod
    def rotation_y(angle):
        mat = Matrix4x4()
        rad = math.radians(angle)
        c, s = math.cos(rad), math.sin(rad)
        # Ось Y остается неподвижной (0, 1, 0), меняются X и Z
        mat.m[0][0], mat.m[0][2] = c, s
        mat.m[2][0], mat.m[2][2] = -s, c
        return mat

    @staticmethod
    def rotation_z(angle):
        mat = Matrix4x4()
        rad = math.radians(angle)
        c, s = math.cos(rad), math.sin(rad)
        # Ось Z остается неподвижной (0, 0, 1), меняются X и Y
        mat.m[0][0], mat.m[0][1] = c, -s
        mat.m[1][0], mat.m[1][1] = s, c
        return mat

    @staticmethod
    def scaling(sx, sy, sz):
        mat = Matrix4x4()
        mat.m[0][0], mat.m[1][1], mat.m[2][2] = sx, sy, sz
        return mat
