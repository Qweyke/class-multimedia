import numpy as np
import sympy as sp


class FunctionResolver:
    @staticmethod
    def get_prepared_values(
        left_x: float, right_x: float, function_symbolic: str, points_qnty: int
    ):
        # 1. Lambdify logic (local)
        x_sym = sp.symbols("x")
        expr_sym = sp.parse_expr(function_symbolic.replace("^", "**"))
        lambdified_func = sp.lambdify(x_sym, expr_sym, "numpy")

        # 2. Raw data generation
        with np.errstate(divide="ignore", invalid="ignore"):
            raw_x_vals = np.linspace(left_x, right_x, points_qnty)
            raw_y_vals = lambdified_func(raw_x_vals)

            if not isinstance(raw_y_vals, np.ndarray):
                raw_y_vals = np.full_like(raw_x_vals, raw_y_vals)

        bad_vals_idxs = np.where(~np.isfinite(raw_y_vals))[0]

        # Early return
        if bad_vals_idxs.size == 0:
            return raw_x_vals, raw_y_vals

        # 3. Bounds calculation
        finite_data = raw_y_vals[np.isfinite(raw_y_vals)]
        if finite_data.size > 0:
            y_min_data = finite_data.min()
            y_max_data = finite_data.max()
            margin = (y_max_data - y_min_data) * 5
            upper_val = y_max_data + margin
            lower_val = y_min_data - margin
        else:
            upper_val, lower_val = 100, -100

        # 4. Processing loop
        for id in bad_vals_idxs:
            # Handle removable discontinuities
            val_to_check = raw_y_vals[id]

            if np.isnan(val_to_check):
                # Skip border-points
                if not (0 < id < len(raw_y_vals) - 1):
                    continue

                left_y_val, right_y_val = raw_y_vals[id - 1], raw_y_vals[id + 1]

                # Skip nan-neighborhood
                if not (np.isfinite(left_y_val) and np.isfinite(right_y_val)):
                    continue

                # Skip large gaps
                eps = 1e-4
                if abs(right_y_val + left_y_val) > eps:
                    continue

                # Interpolate new value for nan
                raw_y_vals[id] = (right_y_val - left_y_val) / 2

            if np.isposinf(val_to_check):
                raw_y_vals[id] = upper_val

            if np.isneginf(val_to_check):
                raw_y_vals[id] = lower_val

        return raw_x_vals, raw_y_vals
