"""Entrenamiento de los modelos.

Flujo, respetando el orden temporal y sin usar el conjunto de evaluación final
para tomar decisiones:

1. Para cada algoritmo se prueba una grilla de hiperparámetros con validación
   temporal dentro del entrenamiento (cortes enero 2021, 2022, 2023 y 2024):
   en cada corte se entrena con lo conocido antes y se valida con las
   predicciones de los 12 meses siguientes. El escalado (si corresponde) se
   ajusta dentro de cada corte, porque es parte del pipeline.
2. Criterio de selección: exactitud balanceada promedio de los cuatro cortes
   (promedio del recall de cada clase). Se eligió porque la proporción de
   contracciones cambia mucho entre años (15% a 87% en los cortes), y con F1
   de la clase positiva un clasificador que dice siempre "contracción" ya
   obtiene un valor alto.
3. Con los hiperparámetros elegidos, cada modelo se entrena una sola vez con
   todo el entrenamiento y se evalúa una sola vez en 2025-2026.
4. Para predecir casos nuevos (modelo "de uso"), el modelo elegido se vuelve a
   entrenar con todas las filas cuyo resultado ya se conoce.

Se corre desde la carpeta raíz del repositorio con:  python -m contraccion_industrial.modeling.train
"""
import itertools
import warnings

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import balanced_accuracy_score, f1_score, roc_auc_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier

from contraccion_industrial.config import MODELS, PREDICTORAS, PROCESSED
from contraccion_industrial.modeling.particiones import (cortes_validacion, excluir_sin_historia,
                                                         separar_por_corte)
from contraccion_industrial.modeling.preprocesamiento import armar_pipeline

CORTE_EVALUACION = "2025-01-01"
CORTES_VALIDACION = ["2021-01-01", "2022-01-01", "2023-01-01", "2024-01-01"]
UMBRAL = 0.5          # probabilidad a partir de la cual se predice "contracción"
SEMILLA = 0

# Grillas de hiperparámetros: cada combinación se valida con los 4 cortes.
GRILLAS = {
    "logistica": {"C": [0.001, 0.01, 0.1, 1, 10],
                  "class_weight": [None, "balanced"],
                  "escalado": ["estandar", "robusto"]},
    "knn": {"n_neighbors": [5, 9, 15, 25, 51, 101],
            "weights": ["uniform", "distance"],
            "escalado": ["estandar", "robusto"]},
    "arbol": {"max_depth": [2, 3, 4, 6, 8],
              "min_samples_leaf": [10, 40, 80],
              "class_weight": [None, "balanced"]},
    "random_forest": {"max_depth": [3, 6, None],
                      "min_samples_leaf": [5, 20],
                      "max_features": ["sqrt", 0.5],
                      "class_weight": [None, "balanced"]},
    "gradient_boosting": {"learning_rate": [0.05, 0.1],
                          "max_depth": [1, 2, 3],
                          "n_estimators": [100, 300]},
}

NOMBRES = {"logistica": "Regresión logística", "knn": "KNN", "arbol": "Árbol de decisión",
           "random_forest": "Random Forest", "gradient_boosting": "Gradient Boosting"}


def cargar_datos():
    """Tabla modelable y sus particiones: entrenamiento, evaluación final y pendientes."""
    tabla = pd.read_csv(PROCESSED / "tabla_modelo.csv", dtype={"codigo_division": str},
                        parse_dates=["fecha", "mes_decision", "mes_etiqueta_conocida"])
    con_historia, _ = excluir_sin_historia(tabla[tabla["ipi_var_ia"].notna()])
    entrenamiento, evaluacion, pendientes = separar_por_corte(con_historia, CORTE_EVALUACION)
    return entrenamiento, evaluacion, pendientes


def crear_modelo(nombre, params):
    """Arma el pipeline (escalado + modelo, o solo modelo) para una configuración."""
    p = dict(params)
    escalado = p.pop("escalado", "estandar")
    if nombre == "logistica":
        modelo = LogisticRegression(max_iter=5000, **p)
    elif nombre == "knn":
        modelo = KNeighborsClassifier(**p)
    elif nombre == "arbol":
        modelo = DecisionTreeClassifier(random_state=SEMILLA, **p)
    elif nombre == "random_forest":
        modelo = RandomForestClassifier(n_estimators=300, random_state=SEMILLA, n_jobs=-1, **p)
    elif nombre == "gradient_boosting":
        modelo = GradientBoostingClassifier(random_state=SEMILLA, **p)
    else:
        raise ValueError(nombre)
    return armar_pipeline(modelo, nombre, escalado)


def configuraciones(nombre):
    grilla = GRILLAS[nombre]
    for valores in itertools.product(*grilla.values()):
        yield dict(zip(grilla.keys(), valores))


def validar(nombre, params, entrenamiento):
    """Métricas de una configuración en cada corte de validación temporal."""
    filas = []
    for corte, ent, val in cortes_validacion(entrenamiento, CORTES_VALIDACION):
        modelo = crear_modelo(nombre, params).fit(ent[PREDICTORAS], ent["objetivo"])
        prob = modelo.predict_proba(val[PREDICTORAS])[:, 1]
        pred = (prob >= UMBRAL).astype(int)
        filas.append({"corte": f"{corte:%Y}",
                      "exactitud_balanceada": balanced_accuracy_score(val["objetivo"], pred),
                      "f1": f1_score(val["objetivo"], pred, zero_division=0),
                      "auc": roc_auc_score(val["objetivo"], prob)})
    return pd.DataFrame(filas)


def buscar_hiperparametros(entrenamiento):
    """Valida todas las configuraciones de todas las grillas. Devuelve una fila por configuración."""
    filas = []
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        for nombre in GRILLAS:
            for params in configuraciones(nombre):
                m = validar(nombre, params, entrenamiento)
                fila = {"modelo": nombre, "params": params,
                        "exactitud_balanceada": m["exactitud_balanceada"].mean(),
                        "desvio": m["exactitud_balanceada"].std(),
                        "f1": m["f1"].mean(), "auc": m["auc"].mean()}
                fila.update({f"eb_{c}": v for c, v in zip(m["corte"], m["exactitud_balanceada"])})
                filas.append(fila)
    return pd.DataFrame(filas)


def mejores_por_modelo(resultados):
    """La mejor configuración de cada algoritmo según la validación."""
    idx = resultados.groupby("modelo")["exactitud_balanceada"].idxmax()
    return resultados.loc[idx].sort_values("exactitud_balanceada", ascending=False).reset_index(drop=True)


def entrenar(nombre, params, datos):
    return crear_modelo(nombre, params).fit(datos[PREDICTORAS], datos["objetivo"])


def guardar(modelo, nombre_archivo):
    MODELS.mkdir(parents=True, exist_ok=True)
    joblib.dump(modelo, MODELS / nombre_archivo)
    return MODELS / nombre_archivo


if __name__ == "__main__":
    entrenamiento, evaluacion, pendientes = cargar_datos()
    resultados = buscar_hiperparametros(entrenamiento)
    mejores = mejores_por_modelo(resultados)
    print(mejores[["modelo", "params", "exactitud_balanceada", "desvio", "f1", "auc"]].to_string())
    elegido = mejores.iloc[0]
    observadas = pd.concat([entrenamiento, evaluacion])
    ruta = guardar(entrenar(elegido["modelo"], elegido["params"], observadas), "modelo_final.joblib")
    print("Modelo de uso guardado en", ruta)
