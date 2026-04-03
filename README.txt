# Proyecto Asset Management

Este proyecto analiza el ciclo de vida de activos tecnológicos, detectando inconsistencias, priorizando casos críticos y generando métricas clave para la toma de decisiones.

---

## 🚀 Funcionalidades

- Análisis de estados de activos
- Detección de inconsistencias (reglas de negocio)
- Priorización de casos (IA básica basada en reglas)
- Generación de métricas (summary)
- Exportación de resultados a CSV

---

## 📂 Estructura del proyecto
src/
│── main.py
│── analyzer.py
│── rules.py
│── advanced_rules.py
│── ai_module.py
│── summary.py

data/
│── assets.csv
│── movements.csv
│── status_history.csv

output/
│── results.csv
│── inconsistencias.csv
│── summary.csv

## ▶️ Cómo ejecutar

```bash
python src/main.py
