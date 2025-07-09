from pulp import (
    LpProblem, LpMaximize, LpVariable,
    LpStatus, value, lpSum,
    PULP_CBC_CMD
)
import numpy as np


class OptimizationModel:
    """
    Resuelve el problema lineal de maximización de ingresos
    """
    def __init__(self, params: dict):
        """
        params debe contener:
        T_A, T_B, T_M, P_A, P_B
        """
        self.p = params
        self.solution = None
        self.status = None

    # --- método principal --------------------------------------------------
    def solve(self, verbose = False) -> dict:
        # Extraer datos
        T_A = self.p["T_A"] # Coeficientes que acompañan la primera variable x_A
        T_B = self.p["T_B"] # Coeficientes que acompañan la segunda variable x_B
        T_M = self.p["T_M"] # Cotas superiores de la inecuación
        total_restrictions = T_M.size # Cantidad de retstricciones
        
        prob = LpProblem("Revenue_Maximization", LpMaximize)

        # Variables de decisión (continuas y ≥0)
        x_A = LpVariable("x_A", lowBound=0)
        x_B = LpVariable("x_B", lowBound=0)

        # Función objetivo
        prob += self.p["P_A"] * x_A + self.p["P_B"] * x_B

        # Restricciones lineales
        for i in range(total_restrictions):
            # T_A[i] x_A + T_B[i] x_B <= T_M[i]
            prob += T_A[i] * x_A + T_B[i] * x_B <= T_M[i]

        # Resolver
        prob.solve(PULP_CBC_CMD(msg=verbose))

        self.status = LpStatus[prob.status]
        if self.status != "Optimal":
            raise ValueError(
                f"El modelo no halló solución óptima (estado: {self.status})"
            )

        self.solution = {
            "x_A_opt": x_A.varValue,
            "x_B_opt": x_B.varValue,
            "revenue_opt": value(prob.objective),
        }
        return self.solution