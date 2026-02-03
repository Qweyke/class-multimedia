import numpy as np
import sympy as sp


class FunctionResolver:
    def __init__(
        self, function_symbolic: str, left_x: float, right_x: float, points_qnty: int
    ):
        x_sym = sp.symbols("x")
        expr_sym = sp.parse_expr(function_symbolic.replace("^", "**"))

        self._lambdified_func = sp.lambdify(x_sym, expr_sym, "numpy")

        self._left_x = left_x
        self._right_x = right_x

        self._points_qnty = points_qnty

    def get_prepared_values(self):
        with np.errstate(divide="ignore", invalid="ignore"):
            raw_x_vals = np.linspace(self._left_x, self._right_x, self._points_qnty)
            raw_y_vals: np.array = self._lambdified_func(raw_x_vals)

        bad_vals_idxs = np.where(raw_y_vals[~np.isfinite(raw_y_vals)])[0]

    # def parse_math_function(
    #     func_name: str,
    # ):
    #     # Resolve breaking-vals

    #     finite_mask = np.isfinite(y_vals)
    #     finite_y = y_vals[finite_mask]

    #     if finite_y.size == 0:
    #         return

    #     # Determine left-right sides
    #     y_min_data = finite_y.min()
    #     y_max_data = finite_y.max()

    #     # Trim asymptotes
    #     y_range = y_max_data - y_min_data
    #     if y_range > 1000:
    #         y_min_data = max(y_min_data, -500)
    #         y_max_data = min(y_max_data, 500)

    def _calculate_func_vals(self):
        with np.errstate(divide="ignore", invalid="ignore"):
            x_vals = np.linspace(self._left_x, self._right_x, self._points_qnty)
            y_vals: np.array = self._lambdified_func(x_vals)

        return x_vals, y_vals

    def resolve_breaking_points(raw_x_vals, raw_y_vals):
        pass
