import os
import pandas as pd
import numpy as np

from optimizador.services.data_loader import DataLoader
from optimizador.services.optimization_model import OptimizationModel
from optimizador.services.output_presenter import OutputPresenter

file_example = "optimization_problem_data_2.csv"
if __name__ == "__main__":
    # Ruta al CSV de prueba
    base_dir = os.path.dirname(__file__)
    csv_path = os.path.join(base_dir, "data", "tests", file_example)
    
    # 1. Cargar datos
    print(f"\nCargando archivo: {csv_path}")
    loader = DataLoader(csv_path)
    params = loader.load_and_validate()
    print("Datos cargados correctamente.")
    
    # 2. Resolver el modelo
    print("\nEjecutando modelo de optimización...")
    model = OptimizationModel(params)
    solution = model.solve()
    print("Modelo resuelto.")
    
    # 3. Mostrar resultados por consola
    print("\nResultados:")
    print(f"x_A óptimo: {solution['x_A_opt']:.2f}")
    print(f"x_B óptimo: {solution['x_B_opt']:.2f}")
    print(f"Ingreso máximo: ${solution['revenue_opt']:.2f}")
    
    # 4. Guardar gráficos
    presenter = OutputPresenter(params, solution)
    feasible_region = presenter._build_plt_feasible_region()
    optimal_units = presenter._build_plt_optimal_units()

    # Región factible
    output_path = os.path.join(base_dir, "figures/feasible_region.png")
    with open(output_path, "wb") as f:
        import base64
        f.write(base64.b64decode(feasible_region))
    print(f'\nGráfico "Región factible" guardado en: {output_path}')
    
    output_path = os.path.join(base_dir, "figures/optimal_units.png")
    with open(output_path, "wb") as f:
        import base64
        f.write(base64.b64decode(optimal_units))
    print(f'\nGráfico "Unidades óptimas" guardado en: {output_path}')