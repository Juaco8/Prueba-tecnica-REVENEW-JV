from django import forms

class form_CSV(forms.Form):
    # Solicitar archivos y otra información en el formulario
    
    # Archivo CSV con BBDD
    file  = forms.FileField(label="Archivo CSV")
    
    def clean_file(self):
        f = self.cleaned_data['file']
        if not f.name.endswith('.csv'):
            raise forms.ValidationError("Solo se permiten archivos CSV.")
        return f
    
class form_EditParams(forms.Form):
    reset_to_base = forms.BooleanField(
        required=False,
        label="Volver a los parámetros originales"
    )
    
    # Tiempos
    T_Ai = forms.FloatField(required=False, label="Coeficiente A")
    T_Bi = forms.FloatField(required=False, label="Coeficiente B")
    T_Mi = forms.FloatField(required=False, label="Cota superior")
    
    # Precios
    P_A = forms.FloatField(required=False, label="Precio Producto A")
    P_B = forms.FloatField(required=False, label="Precio Producto B")
    
    add_row = forms.BooleanField(
        required=False,
        label="Agregar esta nueva restricción"
    )
    
    #Fila a eliminar
    delete_row_index = forms.IntegerField(required=False, label="Eliminar restricción número (índice)")
        