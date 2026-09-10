import os
import pandas as pd
import numpy as np
import kagglehub

# 1. Descarga automática del dataset desde Kaggle
path = kagglehub.dataset_download("ahmedmohamed2003/cafe-sales-dirty-data-for-cleaning-training")
csv_file = [f for f in os.listdir(path) if f.endswith('.csv')][0]
full_path = os.path.join(path, csv_file)

# 2. Carga del dataset transformando placeholders ruidosos en NaN
dirty_values = ['ERROR', 'UNKNOWN', 'ERROR ', 'UNKNOWN ', '', ' ', 'null', 'NULL']
df = pd.read_csv(full_path, na_values=dirty_values)

print("=== Inspección Inicial ===")
print(df.info())
print("\nValores nulos por columna:")
print(df.isnull().sum())

# 3. Limpieza de espacios en blanco en columnas de texto
text_cols = ['Item', 'Payment Method', 'Location']
for col in text_cols:
    if col in df.columns:
        df[col] = df[col].astype(str).str.strip()
        df[col] = df[col].replace({'nan': np.nan, 'None': np.nan, '': np.nan})

# 4. Conversión de columnas numéricas a float/int
num_cols = ['Quantity', 'Price Per Unit', 'Total Spent']
for col in num_cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')

# 5. Inferir precios faltantes según el menú del negocio
menu_prices = {
    'Coffee': 2.0, 'Tea': 1.5, 'Sandwich': 4.0, 
    'Salad': 5.0, 'Cake': 3.0, 'Cookie': 1.0, 
    'Smoothie': 4.0, 'Juice': 3.0
}
df['Price Per Unit'] = df['Price Per Unit'].fillna(df['Item'].map(menu_prices))

# 6. Recálculo e imputación de inconsistencias matemáticas
# Si falta 'Total Spent', calcularlo
df['Total Spent'] = df['Total Spent'].fillna(df['Quantity'] * df['Price Per Unit'])

# Si falta 'Quantity', calcularlo
df['Quantity'] = df['Quantity'].fillna(df['Total Spent'] / df['Price Per Unit'])

# Asegurar consistencia lógica en filas con datos desalineados
valid_math = df['Quantity'].notnull() & df['Price Per Unit'].notnull()
df.loc[valid_math, 'Total Spent'] = df.loc[valid_math, 'Quantity'] * df.loc[valid_math, 'Price Per Unit']

# 7. Tratamiento de variables categóricas faltantes
df['Payment Method'] = df['Payment Method'].fillna('Unknown')
df['Location'] = df['Location'].fillna('Unknown')

# 8. Normalización del formato de fechas
df['Transaction Date'] = pd.to_datetime(df['Transaction Date'], errors='coerce')

# 9. Verificación de resultados y exportación
print("\n=== Inspección Final (Post-Limpieza) ===")
print(df.isnull().sum())

output_path = "clean_cafe_sales.csv"
df.to_csv(output_path, index=False)
print(f"\nBase de datos limpia exportada correctamente en: {output_path}")
