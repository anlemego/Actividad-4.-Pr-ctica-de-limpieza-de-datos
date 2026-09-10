# Limpieza de Datos - Cafe Sales Dataset

Este repositorio contiene la solución completa para la auditoría, limpieza y transformación del dataset `Cafe Sales – Dirty Data for Cleaning Training`.

## Descripción del Procedimiento

El flujo de trabajo automatizado descarga el dataset dinámicamente mediante la librería `kagglehub`, aplica criterios de parsing para convertir datos inválidos a valores nulos sintácticos y ejecuta reglas de negocio enfocadas en recuperar la consistencia financiera y lógica del catálogo del establecimiento.

### Pasos ejecutados:
1. **Ingesta automatizada:** Descarga remota del dataset directamente desde Kaggle.
2. **Normalización de texto:** Extracción de espacios sobrantes y estandarización de cadenas vacías.
3. **Imputación lógica:** Inferencia de precios unitarios según el catálogo de productos.
4. **Recálculo matemático:** Corrección de la relación $\text{Total Spent} = \text{Quantity} \times \text{Price Per Unit}$.
5. **Estandarización temporal:** Conversión de fechas al estándar `YYYY-MM-DD`.

---

## Tabla Resumen de Calidad de Datos

| Problema encontrado | Registros afectados | Acción realizada | Justificación |
| :--- | :--- | :--- | :--- |
| Cadenas de texto inválidas (`ERROR`, `UNKNOWN`, vacíos) | ~1,200 celdas distribuidas | Conversión automática a `NaN` mediante la carga con `na_values`. | Prevenir errores de conversión de tipo y permitir el uso de funciones vectoriales en Pandas. |
| Tipos de datos inconsistentes (números leídos como `object`) | Columnas `Quantity`, `Price Per Unit`, `Total Spent` | Coerción de tipos con `pd.to_numeric(errors='coerce')`. | Habilitar operaciones aritméticas y agregaciones analíticas. |
| Precios unitarios faltantes (`Price Per Unit`) | Variable según la muestra (~10% de registros) | Imputación condicional basada en la columna `Item` usando un diccionario de precios del menú. | Preservar el registro completo sin inventar datos desalineados de la realidad operativa. |
| Discrepancias / vacíos en `Total Spent` y `Quantity` | Variable (~15% de registros) | Recálculo algebraico: $\text{Total} = \text{Quantity} \times \text{Precio}$ y viceversa. | Garantizar la integridad y coherencia matemática en los registros analizados. |
| Inconsistencias en variables categóricas (`Location`, `Payment Method`) | ~800 registros | Sustitución de `NaN` por el valor predeterminado `'Unknown'`. | Evitar descartar registros de ventas válidos manteniendo la categoría no especificada explícita. |
| Fechas con formato inconsistente o guardadas como string | Toda la columna `Transaction Date` | Conversión a tipo `datetime64` con `pd.to_datetime`. | Permitir el filtrado, ordenamiento y agregación por periodos temporales. |

---

## Requisitos para Ejecución

Para reproducir el código contenido en este repositorio:

```bash
pip install pandas numpy kagglehub
