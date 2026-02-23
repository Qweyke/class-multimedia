import numpy as np
import sympy as sp


class FunctionResolver:
    @staticmethod
    def get_prepared_values(
        left_x: float, right_x: float, function_symbolic: str, points_qnty: int
    ):
        """
        Solves the function and returns x, y, and the y-min/max bounds.
        """
        # 1. Sympy logic: prepare the expression
        x_sym = sp.symbols("x")
        # Replace ^ with ** for python compatibility and parse
        expr_sym = sp.parse_expr(function_symbolic.replace("^", "**"))

        # Convert to a fast numpy function
        lambdified_func = sp.lambdify(x_sym, expr_sym, "numpy")

        # 2. Raw data generation
        with np.errstate(divide="ignore", invalid="ignore"):
            raw_x_vals = np.linspace(left_x, right_x, points_qnty)
            raw_y_vals = lambdified_func(raw_x_vals)

            # If the result is a constant (e.g., f(x) = 5), numpy returns a scalar.
            # We must convert it to an array of the same shape as x.
            if not isinstance(raw_y_vals, np.ndarray):
                raw_y_vals = np.full_like(raw_x_vals, raw_y_vals)

        # 3. BOUNDS CALCULATION (The Logic you requested)
        # Identify indices where values are NOT infinity and NOT NaN
        finite_mask = np.isfinite(raw_y_vals)
        finite_data = raw_y_vals[finite_mask]

        if finite_data.size > 0:
            # These are the actual 'visible' boundaries for the legend/mapper
            real_min = float(finite_data.min())
            real_max = float(finite_data.max())

            # Determine how far we should "clamp" the infinite spikes.
            # We set a margin so the lines go slightly off-screen rather than
            # stopping exactly at the border.
            margin = (real_max - real_min) * 2 if real_max != real_min else 1.0
            upper_val = real_max + margin
            lower_val = real_min - margin
        else:
            # Fallback if the function is entirely undefined in this range
            real_min, real_max = -1.0, 1.0
            upper_val, lower_val = 100, -100

        # 4. PROCESSING DISCONTINUITIES (Cleaning the data)
        bad_vals_idxs = np.where(~finite_mask)[0]

        for idx in bad_vals_idxs:
            val_to_check = raw_y_vals[idx]

            # Handle NaN (Removable discontinuities)
            if np.isnan(val_to_check):
                # Try to interpolate if not at the very edge
                if 0 < idx < len(raw_y_vals) - 1:
                    left_y, right_y = raw_y_vals[idx - 1], raw_y_vals[idx + 1]
                    if np.isfinite(left_y) and np.isfinite(right_y):
                        # Simple average to fill the gap
                        raw_y_vals[idx] = (left_y + right_y) / 2
                continue

            # Handle Infinities: Clamp them so the Renderer doesn't crash
            if np.isposinf(val_to_check):
                raw_y_vals[idx] = upper_val
            elif np.isneginf(val_to_check):
                raw_y_vals[idx] = lower_val

        # Return the coordinates and the "Healthy" bounds for the Mapper
        return (
            real_min,
            real_max,
            raw_x_vals,
            raw_y_vals,
        )
