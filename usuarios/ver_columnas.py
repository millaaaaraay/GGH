import pandas as pd

ruta_excel = r"C:\Users\millaray\Documents\Usuarios AD revisado.xlsx"  # Ajusta esta ruta a la correcta

df = pd.read_excel(ruta_excel, engine='openpyxl')

print(df.columns.tolist())
