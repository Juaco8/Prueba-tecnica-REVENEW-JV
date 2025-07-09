# Librerías
from django.shortcuts import render, redirect
from django.http import HttpResponse # 1
from .forms import form_CSV, form_EditParams
from .services.data_loader import DataLoader
from .services.optimization_model import OptimizationModel
from .services.output_presenter import OutputPresenter
import pandas as pd
import numpy as np

# Otras funciones
def python_to_session(d):
    return {k: (v.tolist() if isinstance(v, np.ndarray) else v) for k, v in d.items()}

def np_to_python(d):
    out = {}
    for k, v in d.items():
        if isinstance(v, list):
            out[k] = np.array(v, dtype=float)
        else:
            out[k] = v
    return out

# Views
def view_apply_model(request):
    # Recepción de formulario
    if request.method == "POST":
        form = form_CSV(request.POST, request.FILES)
        if form.is_valid():
            file = form.cleaned_data["file"]
            try:
                # Cargar datos
                loader = DataLoader(file)
                params = loader.load_and_validate()
                request.session["params_base"] = {k: v.tolist() for k, v in params.items()}
                request.session["params_current"] = request.session["params_base"].copy()
                
                # Correr modelo
                model = OptimizationModel(params)
                solution = model.solve()
                
                # Mostrar resultados
                context = OutputPresenter(params, solution).get_context()
                return render(request, "optimizador/results.html", context)

            except ValueError as e:
                form.add_error("file", str(e))

    else:
        form = form_CSV()

    # Solicitud de formulario
    return render(request, "optimizador/upload_data.html",  {"form": form})

def view_edit_params(request):
    if "params_base" not in request.session:
        return redirect("upload_data")  # o algún manejo de error más amable
    
    # Copiamos los parámetros actuales
    current = np_to_python(request.session["params_current"])
    base = np_to_python(request.session["params_base"])

    if request.method == "POST":
        form = form_EditParams(request.POST)
        if form.is_valid():

            if form.cleaned_data["reset_to_base"]:
                request.session["params_current"] = python_to_session(base)
                return redirect("url_edit_params")

            if form.cleaned_data["add_row"]:
                try:
                    # Leemos y agregamos la fila
                    if (form.cleaned_data["T_Ai"] is not None) & (form.cleaned_data["T_Bi"] is not None) & (form.cleaned_data["T_Mi"] is not None):
                        current["T_A"] = np.append(current["T_A"], float(form.cleaned_data["T_Ai"]))
                        current["T_B"] = np.append(current["T_B"], float(form.cleaned_data["T_Bi"]))
                        current["T_M"] = np.append(current["T_M"], float(form.cleaned_data["T_Mi"]))
                        request.session["params_current"] = python_to_session(current)
                    else:
                        # No fue agregada completamente
                        form.add_error(None, "Error al agregar la restricción, todos los elementos deben añadirse")
                        return render(request, "optimizador/edit_params.html", {"form": form})
                except Exception:
                    form.add_error(None, "Error al agregar la restricción. Verifica los valores.")
                    return render(request, "optimizador/edit_params.html", {"form": form})
                
            # Eliminar fila por índice
            if form.cleaned_data["delete_row_index"] is not None:
                i = form.cleaned_data["delete_row_index"]
                try:
                    for key in ["T_A", "T_B", "T_M"]:
                        current[key] = np.delete(current[key], i)
                    request.session["params_current"] = python_to_session(current)
                except Exception:
                    form.add_error(None, f"No se pudo eliminar la fila {i}.")
                    return render(request, "optimizador/edit_params.html", {"form": form, "params": current})
                
            # Actualizar precios
            try:
                if form.cleaned_data["P_A"] is not None:
                    current["P_A"] = float(form.cleaned_data["P_A"])
                if form.cleaned_data["P_B"] is not None:
                    current["P_B"] = float(form.cleaned_data["P_B"])
                request.session["params_current"] = python_to_session(current)
            except Exception:
                form.add_error(None, "Error al actualizar precios. Verifica los valores.")
                return render(request, "optimizador/edit_params.html", {"form": form})
            
            # Ejecutar modelo con nuevos parámetros
            try:
                model = OptimizationModel(current)
                solution = model.solve()
                context = OutputPresenter(current, solution).get_context()
                return render(request, "optimizador/results.html", context)

            except Exception as e:
                form.add_error(None, f"Error al resolver modelo: {e}")
    else:
        form = form_EditParams()

    df = pd.DataFrame({
        "T_A": current["T_A"],
        "T_B": current["T_B"],
        "T_M": current["T_M"]
    })
    df.index.name = "i"
    restrictions_table = df.reset_index().to_html(index=False, classes="table table-bordered table-striped")

    return render(request, "optimizador/edit_params.html", {
        "form": form,
        "params": current,
        "restrictions_table": restrictions_table
    })