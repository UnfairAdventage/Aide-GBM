# Calculadora de Criticalidad del Gasto Metabólico

Esta aplicación de escritorio permite calcular la criticalidad del gasto metabólico de una persona utilizando transformadas de Fourier y la fórmula de Harris-Benedict.

## Características

- Cálculo del Gasto Metabólico Basal (TMB) usando la fórmula de Harris-Benedict
- Transformada de Fourier para análisis de frecuencias
- Interfaz gráfica intuitiva con PyQt5
- Tablas interactivas para visualización de resultados
- Cálculo de coeficientes de Fourier para diferentes valores de K
- Análisis estadístico básico

## Requisitos

- Python 3.8 o superior
- PyQt5
- NumPy
- Pandas
- Matplotlib

## Instalación

1. Clonar el repositorio:
```bash
git clone <url-del-repositorio>
cd proyecto_criticalidad
```

2. Crear un entorno virtual (opcional pero recomendado):
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

## Uso

1. Ejecutar la aplicación:
```bash
python src/main.py
```

2. En la interfaz:
   - Ingrese los datos personales (sexo, peso, altura, edad)
   - Agregue los minutos de ejercicio diarios usando el botón "Agregar Día"
   - Haga clic en "Calcular" para ver los resultados
   - Use el selector de K para ver diferentes coeficientes de Fourier

## Estructura del Proyecto

```
proyecto_criticalidad/
│
├── src/
│   ├── main.py                 # Punto de entrada
│   ├── app.py                  # Clase principal de la aplicación
│   ├── models/
│   │   └── person.py          # Modelo de datos personales
│
├── requirements.txt
└── README.md
```

## Fórmulas Utilizadas

### TMB (Gasto Metabólico Basal)

Para hombres:
```
TMB = 88.362 + (13.397 * peso) + (4.799 * altura) - (5.677 * edad)
```

Para mujeres:
```
TMB = 447.593 + (9.247 * peso) + (3.098 * altura) - (4.333 * edad)
```

### Transformada de Fourier

Para una serie X_n:
```
a_k = (2/N) * Σ(X_n * cos(2πkn/N))
b_k = (2/N) * Σ(X_n * sin(2πkn/N))
```

## Contribuir

Las contribuciones son bienvenidas. Por favor, asegúrese de:

1. Hacer fork del repositorio
2. Crear una rama para su feature (`git checkout -b feature/AmazingFeature`)
3. Commit sus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles. 