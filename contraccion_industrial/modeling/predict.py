"""Uso del modelo para predecir casos nuevos.

Momento de la predicción: cuando el INDEC publica el IPI del mes t (en t+2).
Entrada: una fila por división con las 15 predictoras de ese mes (ver
docs/diccionario_de_datos.md), calculadas con contraccion_industrial.features.
Salida: probabilidad estimada de que la división esté en contracción
interanual en el mes t+5 (3 meses después de la decisión) y la clase
predicha con el umbral 0,5.

El modelo no recalcula escalas ni vecinos con los datos nuevos: usa el
pipeline guardado en models/modelo_final.joblib tal como se entrenó.

Se corre desde la carpeta raíz del repositorio con:  python -m contraccion_industrial.modeling.predict
(predice las filas pendientes, cuyo resultado todavía no se publicó).
"""
import joblib
import pandas as pd

from contraccion_industrial.config import HORIZONTE, MODELS, PREDICTORAS
from contraccion_industrial.modeling.train import UMBRAL, cargar_datos

ARCHIVO_MODELO = MODELS / "modelo_final.joblib"
ARCHIVO_PREDICCIONES = MODELS / "predicciones_pendientes.csv"


def cargar_modelo(ruta=ARCHIVO_MODELO):
    return joblib.load(ruta)


def predecir(modelo, nuevos, umbral=UMBRAL):
    """Devuelve una copia de `nuevos` con la probabilidad y la clase predichas.
    `nuevos` debe tener las 15 columnas de PREDICTORAS, sin faltantes."""
    faltan = [c for c in PREDICTORAS if c not in nuevos.columns]
    assert not faltan, f"Faltan predictoras: {faltan}"
    assert not nuevos[PREDICTORAS].isna().any().any(), "Hay faltantes en las predictoras"
    salida = nuevos.copy()
    salida["prob_contraccion"] = modelo.predict_proba(nuevos[PREDICTORAS])[:, 1]
    salida["prediccion"] = (salida["prob_contraccion"] >= umbral).astype(int)
    if "fecha" in salida.columns:
        salida["mes_predicho"] = salida["fecha"] + pd.DateOffset(months=HORIZONTE)
    return salida


if __name__ == "__main__":
    _, _, pendientes = cargar_datos()
    resultado = predecir(cargar_modelo(), pendientes)
    columnas = ["fecha", "mes_decision", "mes_predicho", "codigo_division", "division",
                "contraccion_hoy", "prob_contraccion", "prediccion"]
    resultado[columnas].to_csv(ARCHIVO_PREDICCIONES, index=False)
    print(resultado[columnas].tail(16).to_string(index=False))
    print("Guardado en", ARCHIVO_PREDICCIONES)
