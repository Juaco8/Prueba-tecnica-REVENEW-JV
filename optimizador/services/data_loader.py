import pandas as pd
import numpy as np

class DataLoader:
    """
        Lectura y validación de archivo CSV
    """
    
    # Columnas a tener según el formato requerido para el CSV
    REQUIRED_COLUMNS = [
        "Product_A_Production_Time_Machine_1",
        "Product_A_Production_Time_Machine_2",
        "Product_B_Production_Time_Machine_1",
        "Product_B_Production_Time_Machine_2",
        "Machine_1_Available_Hours",
        "Machine_2_Available_Hours",
        "Price_Product_A",
        "Price_Product_B",
    ]
    REQUIRED_COLUMNS_label = [
        "T_A1",
        "T_A2",
        "T_B1",
        "T_B2",
        "T_M1",
        "T_M2",
        "P_A",
        "P_B"
    ]

    def __init__(self, file):
        self.file = file
        self.df = None
        self.base_params = None
        self.params = None

    # Carga y valida los datos
    def load_and_validate(self):
        try:
            # Lectura
            df_imported = pd.read_csv(self.file)
            required_columns = self.REQUIRED_COLUMNS
            required_columns_label = self.REQUIRED_COLUMNS_label

            # Columnas faltantes
            missing_cols = [col for col in required_columns if col not in df_imported.columns]
            if missing_cols:
                raise ValueError(f"Faltan columnas: {missing_cols}")

            # Extraemos las columnas necesarias, en el formato deseado si es posible y validamos sobre esta
            df = pd.DataFrame(index = df_imported.index, columns = required_columns_label, dtype = float)
            for i, column in enumerate(required_columns):
                column_label = required_columns_label[i]
                try:
                    df[column_label] = df_imported[column].astype(float).tolist()
                except:
                    raise ValueError(f"El archivo tiene datos no numéricos en la columna {column}")
                if df[column_label].isna().any():
                    raise ValueError(f"El archivo tiene datos vacíos en la columna {column}")
                if (df[column_label] <= 0).any():
                    raise ValueError(f"El archivo tiene datos no positivos en la columna {column}")
            
            # Guardar dataframe
            self.df = df
            
            # Escoger parámetros (Por defecto toma la primera fila)
            # Recomendaría ajustar la carga de archivos así se cargan varias restricciones
            row = df.iloc[0]
            params = {
                "T_A": row[["T_A1", "T_A2"]].to_numpy(), # Coeficientes que acompañan la primera variable x_A
                "T_B": row[["T_B1", "T_B2"]].to_numpy(), # Coeficientes que acompañan la primera variable x_B
                "T_M": row[["T_M1", "T_M2"]].to_numpy(), # Cotas superiores de la inecuación
                "P_A": row["P_A"], # Precios de A
                "P_B": row["P_B"]  # Precios de B
            }
            self.base_params = params.copy()
            self.params = params.copy()
            return params
        
        except Exception as e:
            raise ValueError(f"Error al cargar archivo: {str(e)}")