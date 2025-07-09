import io, base64
import numpy as np
import matplotlib.pyplot as plt


class OutputPresenter:
    """
    Genera gráficos a partir de los valores óptimos
    """
    def __init__(self, params: dict, solution: dict):
        self.p = params
        self.sol = solution

    # ------------------------------------------------------------------ #
    #   PÚBLICO
    # ------------------------------------------------------------------ #
    def get_context(self) -> dict:
        """
        Devuelve un diccionario para pasar directo al template.
        """
        return {
            "x_A_opt": self.sol["x_A_opt"],
            "x_B_opt": self.sol["x_B_opt"],
            "revenue_opt": self.sol["revenue_opt"],
            "plt_feasible_region": self._build_plt_feasible_region(),
            "plt_optimal_units": self._build_plt_optimal_units(),
        }

    # ------------------------------------------------------------------ #
    #   PRIVADO
    # ------------------------------------------------------------------ #
    def _build_plt_feasible_region(self) -> str:
        """
        Construye un PNG en memoria con la región factible y lo devuelve
        como string base64 para insertar en <img>.
        """
        
        # Extraer datos
        T_A = self.p["T_A"] # Coeficientes que acompañan la primera variable x_A
        T_B = self.p["T_B"] # Coeficientes que acompañan la segunda variable x_B
        T_M = self.p["T_M"] # Cotas superiores de la inecuación
        total_restrictions = T_M.size # Cantidad de retstricciones

        # Intersecciones con ejes X e Y para definir el área dibujada
        x_inters = np.where(T_A != 0, T_M / T_A, np.nan)
        y_inters = np.where(T_B != 0, T_M / T_B, np.nan)
        xmax = 5 if np.isnan(x_inters).all() else np.nanmax(x_inters)
        ymax = 5 if np.isnan(y_inters).all() else np.nanmax(y_inters)
        

        # Figura
        fig, ax = plt.subplots()

        # Graficar restricciones lineales
        x_vals = np.linspace(0, xmax, 200)
        y_feasible = np.full(200, ymax)
        for i in range(total_restrictions):
            # T_A[i] x_A + T_B[i] x_B <= T_M[i]
            y_vals = (T_M[i] - T_A[i] * x_vals) / T_B[i]
            ax.plot(x_vals, y_vals, label = f"Restricción {i+1}")
            y_feasible = np.minimum(y_feasible, y_vals)
        
        # Graficar región factible
        ax.fill_between(x_vals, 0, y_feasible, alpha=0.15)

        # Punto óptimo
        ax.scatter(self.sol["x_A_opt"], self.sol["x_B_opt"], s=60, zorder=5)
        ax.annotate(
            f"({self.sol['x_A_opt']:.2f}, {self.sol['x_B_opt']:.2f})",
            (self.sol["x_A_opt"], self.sol["x_B_opt"]),
            textcoords="offset points", xytext=(5, 5),
        )
        
        # Recta de precios
        y_vals = (self.sol["revenue_opt"] - self.p["P_A"] * x_vals) / self.p["P_B"]
        ax.plot(x_vals, y_vals, color = 'gray', linestyle = '--', label = f"Corte sensibilidad precios (P_A/P_B)")

        # Settings
        ax.set_xlim(0, xmax * 1.1)
        ax.set_ylim(0, ymax * 1.1)
        ax.set_xlabel("Unidades de Producto A (x_A)")
        ax.set_ylabel("Unidades de Producto B (x_B)")
        ax.set_title("Región factible y solución óptima")
        ax.legend()
        ax.grid(True)

        # Convertir a base64
        buffer = io.BytesIO()
        fig.tight_layout()
        fig.savefig(buffer, format="png")
        plt.close(fig)               # liberar memoria
        buffer.seek(0)
        b64 = base64.b64encode(buffer.read()).decode("ascii")
        return b64
    
    
    def _build_plt_optimal_units(self) -> str:
        """
        Construye un PNG en memoria con la cantidad de unidades a vender de cada producto y lo devuelve
        como string base64 para insertar en <img>.
        """

        # Extraer datos
        x_A = self.sol["x_A_opt"]
        x_B = self.sol["x_B_opt"]
        units = [x_A, x_B]
        labels = ["Producto A", "Producto B"]

        # Figura
        fig, ax = plt.subplots()
        colors = ['#1f77b4', '#ff7f0e']

        # Gráfico de bars
        bars = ax.bar(labels, units, color=colors, width = 0.5)

        # mostrar las cantidades encima de cada barra
        for bar, cantidad in zip(bars, units):
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 0.1,
                f"{cantidad:.1f}",
                ha='center', va='bottom',
                fontsize = 16
            )

        # Settings
        ax.set_ylim(0, np.max(units) * 1.1)
        ax.set_ylabel("Unidades")
        ax.set_title("Unidades vendidas caso óptimo")
        ax.yaxis.grid(True, linestyle='--', alpha=0.5)
        ax.xaxis.grid(False)
        ax.set_axisbelow(True)
        #ax.spines['top'].set_visible(False)
        #ax.spines['right'].set_visible(False)

        # Settings
        # ax.set_xlim(0, xmax * 1.1)
        # ax.set_ylim(0, ymax * 1.1)
        # ax.set_xlabel("Unidades de Producto A (x_A)")
        # ax.set_ylabel("Unidades de Producto B (x_B)")
        # ax.set_title("Región factible y solución óptima")
        # ax.legend()
        # ax.grid(True)

        # Convertir a base64
        buffer = io.BytesIO()
        fig.tight_layout()
        fig.savefig(buffer, format="png")
        plt.close(fig)               # liberar memoria
        buffer.seek(0)
        b64 = base64.b64encode(buffer.read()).decode("ascii")
        return b64