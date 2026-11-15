# Modelos

| Archivo | Contenido |
|---|---|
| `modelo_final.joblib` | Modelo de uso: pipeline de escalado estándar + KNN (k = 15, voto uniforme), elegido con validación temporal y reentrenado con las 1.648 filas cuyo resultado ya se conoce (datos de abril 2017 a marzo 2026). |
| `predicciones_pendientes.csv` | Predicciones para las 80 filas cuyo resultado todavía no se publicó (datos de abril a agosto 2026, meses predichos de septiembre 2026 a enero 2027): probabilidad de contracción y clase predicha con umbral 0,5. |

Se generan con `notebooks/2.0-mf-modelado-evaluacion.ipynb` o con `python -m contraccion_industrial.modeling.train` y `python -m contraccion_industrial.modeling.predict`, desde la carpeta raíz del repositorio. Cómo usar el modelo: [`docs/02_modelo_y_resultados.md`](../docs/02_modelo_y_resultados.md), sección 7.
