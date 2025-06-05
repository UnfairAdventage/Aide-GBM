# Calculadora de Criticalidad del Gasto Metabólico

## 🎯 Objetivo

Aplicación de escritorio en Python para calcular la criticalidad del gasto metabólico diario utilizando análisis de Fourier y estadística. Permite a los usuarios ingresar datos personales y de ejercicio, visualizar resultados detallados y realizar análisis avanzados.

---

## 🖥️ Características Principales

*   **Cálculo Metabólico:** Calcula el Gasto Metabólico Basal (TMB), Factor de Actividad Física (AF) y Gasto Bruto Diario (GB) basándose en datos personales y minutos de ejercicio.
*   **Análisis de Fourier:** Determina los coeficientes de Fourier ($a_k$, $b_k$, $A_k$) para identificar patrones de frecuencia en el Gasto Bruto Diario.
*   **Análisis Estadístico:** Realiza regresión lineal sobre las transformaciones logarítmicas de los coeficientes de Fourier ($\log_{10}(k)$ vs $\log_{10}(A_k)$), calcula la pendiente ($\alpha$), el intercepto ($C$), el coeficiente de correlación ($r$), medias ($\bar{x}$, $\bar{y}$) y desviaciones estándar ($\sigma_x$, $\sigma_y$).
*   **Interfaz Gráfica Intuitiva:** Desarrollada con PyQt5 (o Tkinter, según la elección inicial), organizada en pestañas para facilitar el ingreso de datos y la visualización de resultados.
*   **Visualización Tabular:** Muestra los resultados diarios, los coeficientes de Fourier y los resultados estadísticos en tablas claras y organizadas.
*   **Generación de Gráficos:** Crea un gráfico de dispersión de $\log_{10}(A_k)$ vs $\log_{10}(k)$ con la línea de regresión lineal.
*   **Exportación de Resultados:** Permite exportar los datos tabulares a archivos CSV o Excel.

---

## 🛠️ Instalación Paso a Paso

### Requisitos del Sistema

*   Python 3.8 o superior
*   Sistema operativo compatible con PyQt5 (Windows, macOS, Linux)

### Pasos de Instalación

1.  **Clonar el repositorio:**

    ```bash
    git clone <url-del-repositorio>
    cd metabolic_criticality
    ```

2.  **Crear y activar un entorno virtual (Recomendado):**

    ```bash
    # Crear entorno virtual
    python -m venv venv

    # Activar entorno virtual
    # En Windows:
    .\\venv\\Scripts\\activate
    # En macOS/Linux:
    source venv/bin/activate
    ```

3.  **Instalar dependencias:**

    Asegúrate de que tu entorno virtual esté activado.

    ```bash
    pip install -r requirements.txt
    ```
    *Nota: El archivo `requirements.txt` listará las dependencias necesarias como `numpy`, `pandas`, `matplotlib`, `pytest`, y `pyqt5` (o `tkinter` si se eligió esa opción).*

---

## 🚀 Cómo Ejecutar la App

Una vez que las dependencias estén instaladas y tu entorno virtual activado:

```bash
python -m src.main
```

Esto iniciará la interfaz gráfica de la aplicación.

---

## 🧪 Cómo Ejecutar los Tests

Para ejecutar las pruebas unitarias y verificar el correcto funcionamiento de la lógica de cálculo:

Asegúrate de estar en la raíz del proyecto (`metabolic_criticality/`) y que tu entorno virtual esté activado.

```bash
pytest
```

---

## 📂 Estructura del Proyecto

El proyecto sigue una estructura modular para una mejor organización y mantenibilidad:

```
metabolic_criticality/
│
├── src/                          # Código fuente de la aplicación
│   ├── __init__.py               # Inicializa el paquete src
│   ├── main.py                   # Punto de entrada: inicializa la app PyQt5 y la ventana principal
│   ├── views/                    # Módulos para la interfaz gráfica de usuario (GUI)
│   │   ├── __init__.py           # Inicializa el paquete views
│   │   ├── main_view.py          # Ventana principal con la estructura de pestañas y lógica UI de alto nivel
│   │   # Aunque no implementado como archivos separados actualmente,
│   │   # una refactorización futura podría incluir:
│   │   # personal_data_tab.py    # Widget o lógica específica para la pestaña de datos personales
│   │   # daily_exercise_tab.py   # Widget o lógica específica para la pestaña de ejercicio diario
│   │   # daily_results_tab.py    # Widget o lógica específica para la pestaña de resultados diarios
│   │   # fourier_tab.py          # Widget o lógica específica para la pestaña de análisis de Fourier
│   │   # statistics_tab.py       # Widget o lógica específica para la pestaña de análisis estadístico
│   │
│   ├── models/                   # Módulos para la lógica de negocio y cálculos matemáticos
│   │   ├── __init__.py           # Inicializa el paquete models
│   │   ├── metabolic.py          # Funciones para calcular TMB, AF, GB
│   │   ├── fourier.py            # Funciones para calcular coeficientes de Fourier y transformaciones logarítmicas
│   │   ├── statistics.py         # Funciones para análisis estadístico (regresión, correlación, etc.)
│   │
│   ├── utils/                    # Módulos con funciones auxiliares
│   │   ├── __init__.py           # Inicializa el paquete utils
│   │   ├── helpers.py            # Funciones de ayuda general, como validación de entradas
│   │   # Una refactorización futura podría incluir:
│   │   # validators.py           # Funciones dedicadas a la validación de datos
│   │   # converters.py           # Funciones para conversiones de unidades o formatos
│
├── test/                         # Pruebas unitarias
│   ├── __init__.py               # Inicializa el paquete test
│   ├── test_metabolic.py         # Pruebas para el módulo metabolic.py
│   ├── test_fourier.py           # Pruebas para el módulo fourier.py
│   ├── test_statistics.py        # Pruebas para el módulo statistics.py
│   # Una refactorización futura podría incluir:
│   # test_validators.py          # Pruebas para el módulo validators.py
│
├── requirements.txt              # Lista de dependencias del proyecto
└── README.md                     # Documentación principal del proyecto
```

---

## 🧮 Fórmulas Utilizadas

La aplicación utiliza las siguientes fórmulas para los cálculos:

### Gasto Metabólico Basal (TMB)

*   **Para hombres:**
    $$
    \text{TMB} = 88.362 + (13.397 \times \text{peso}) + (4.799 \times \text{altura}) - (5.677 \times \text{edad})
    $$
*   **Para mujeres:**
    $$
    \text{TMB} = 447.593 + (9.247 \times \text{peso}) + (3.098 \times \text{altura}) - (4.333 \times \text{edad})
    $$
    *Peso en kg, Altura en cm, Edad en años.*

### Factor de Actividad Física (AF)

$$
\text{AF} = 1.2 + 0.01 \times (\text{minutos de ejercicio})
$$
*Minutos de ejercicio diario.*

### Gasto Bruto Diario (GB)

$$
\text{GB} = \text{TMB} \times \text{AF}
$$

### Coeficientes de Fourier

Para una serie de datos $x_n$ (Gasto Bruto Diario) con $N$ puntos (días), los coeficientes para una frecuencia $k$ se calculan como:

*   **Frecuencia angular:**
    $$
    f = 2\pi k \frac{n}{N}
    $$
    *Donde $n$ es el índice del día (de 1 a $N$).*

*   **Coeficiente $a_k$:**
    $$
    a_k = \frac{2}{N} \sum_{n=1}^{N} x_n \cos(f)
    $$

*   **Coeficiente $b_k$:**
    $$
    b_k = \frac{2}{N} \sum_{n=1}^{N} x_n \sin(f)
    $$

*   **Amplitud $A_k$:**
    $$
    A_k = \sqrt{a_k^2 + b_k^2}
    $$

### Transformación Logarítmica para Análisis de Fourier

*   $$
    x = \log_{10}(k)
    $$
*   $$
    y = \log_{10}(A_k)
    $$
    *Estas transformaciones se aplican para $k > 0$ y $A_k > 0$.*

### Análisis Estadístico (Regresión Lineal $y = \alpha x + C$)

*   **Pendiente ($\alpha$):**
    $$
    \alpha = \frac{N \sum xy - (\sum x)(\sum y)}{N \sum x^2 - (\sum x)^2}
    $$

*   **Intercepto ($C$):**
    $$
    C = \bar{y} - \alpha \bar{x}
    $$

*   **Coeficiente de Correlación ($r$):**
    $$
    r = \frac{\frac{\sum xy}{N} - \bar{x} \bar{y}}{\sigma_x \sigma_y}
    $$

*   **Media Aritmética ($\bar{x}$, $\bar{y}$):**
    $$
    \bar{x} = \frac{\sum x}{N}, \quad \bar{y} = \frac{\sum y}{N}
    $$
    *Donde $N$ es el número de puntos $(x, y)$ utilizados en la regresión (pares $\log_{10}(k), \log_{10}(A_k)$ para $k > 0$).*

*   **Desviación Estándar ($\sigma_x$, $\sigma_y$):**
    $$
    \sigma_x = \sqrt{\frac{\sum x^2}{N} - \bar{x}^2}, \quad \sigma_y = \sqrt{\frac{\sum y^2}{N} - \bar{y}^2}
    $$

---

## 📊 Explicación de la Interfaz de Usuario (UI)

La ventana principal está organizada en pestañas para guiar al usuario a través del proceso de análisis:

1.  **Datos Personales:**
    *   Permite ingresar información personal como Sexo, Peso (kg), Altura (cm) y Edad (años).
    *   Se define el "Número de días de análisis (N)" para la recopilación de datos de ejercicio.
    *   El botón "Siguiente" valida los datos personales y configura la tabla de ejercicio diario.

2.  **Ejercicio Diario:**
    *   Una tabla donde se ingresan los "Minutos de ejercicio" para cada uno de los N días definidos previamente.
    *   La columna "Día (n)" se completa automáticamente.
    *   El botón "Calcular TMB, AF y GB" procesa los datos personales y de ejercicio para calcular los resultados metabólicos diarios y procede con los análisis de Fourier y estadístico.

3.  **Resultados Diarios:**
    *   Muestra en una tabla los resultados calculados para cada día: Día, Minutos de ejercicio, TMB, AF y GB.
    *   Incluye un botón para exportar estos resultados a un archivo CSV o Excel.

4.  **Análisis de Fourier:**
    *   Presenta una tabla con los resultados del análisis de Fourier para diferentes valores de $k$ (actualmente k=1 a min(N, 5)): $k$, $a_k$, $b_k$, $A_k$, $\log_{10}(k)$, $\log_{10}(A_k)$, $x$, $y$, $xy$.
    *   Permite exportar estos resultados.

5.  **Análisis Estadístico:**
    *   Muestra los resultados del análisis estadístico realizado sobre los datos de $\log_{10}(k)$ y $\log_{10}(A_k)$.
    *   Incluye la Pendiente ($\alpha$), Intercepto ($C$), Coeficiente de Correlación ($r$), Media de x ($\bar{x}$), Media de y ($\bar{y}$), Desviación Estándar de x ($\sigma_x$) y Desviación Estándar de y ($\sigma_y$).
    *   Contiene un botón para generar el gráfico de dispersión de $\log_{10}(A_k)$ vs $\log_{10}(k)$ con la línea de regresión.

---

## ❗ Errores Comunes y Cómo Solucionarlos

*   **`ModuleNotFoundError: No module named 'src'` o `No module named 'views'`:** Este error ocurre típicamente al intentar ejecutar el archivo `main.py` directamente como un script (`python main.py`) en lugar de ejecutarlo como un módulo dentro del paquete `src`.
    *   **Solución:** Asegúrate de ejecutar la aplicación desde la raíz del proyecto (`metabolic_criticality/`) utilizando el comando.
```py
python -m src.main
```

*   **Errores de validación de entrada:** Mensajes emergentes que indican "Invalid Input" (Entrada Inválida).
    *   **Solución:** Revisa que los valores ingresados en los campos de texto (Peso, Altura, Edad, Número de días, Minutos de ejercicio) sean números válidos y positivos (enteros para Edad y Días). Asegúrate de seleccionar una opción válida para Sexo.

*   **Resultados inesperados en el Análisis de Fourier:** Si los valores de $k$ mostrados no son los esperados.
    *   **Contexto:** El análisis de Fourier estándar para datos reales calcula coeficientes hasta $k = N/2$. La aplicación está configurada para mostrar coeficientes para $k$ de 1 hasta un máximo de 5 o el número de días ($N$), lo que sea menor, para alinearse con un requisito específico. Si N es pequeño (por ejemplo, N=3), solo verás resultados para k=1, 2.
    *   **Solución:** Asegúrate de ingresar un número de días (N) suficiente para generar los coeficientes de Fourier para los valores de $k$ que deseas analizar. Para ver resultados hasta k=5, necesitas ingresar al menos 5 días de datos.

*   **Errores durante el cálculo estadístico (por ejemplo, `ZeroDivisionError`):** Esto puede ocurrir si hay datos insuficientes para realizar el análisis (menos de 2 puntos para la regresión) o si los datos resultan en una desviación estándar de cero.
    *   **Solución:** Asegúrate de tener al menos dos pares válidos de $(\log_{10}(k), \log_{10}(A_k))$ después de realizar el análisis de Fourier. Esto requiere que haya al menos dos valores de $A_k > 0$ para $k > 0$.

---

## 🧑‍💻 Público Objetivo

Esta herramienta está diseñada para:

*   **Estudiantes:** Interesados en aplicar conceptos de cálculo metabólico, análisis de Fourier y estadística a datos biológicos.
*   **Nutriólogos/Profesionales de la Salud:** Que deseen una herramienta de escritorio para realizar análisis metabólicos y explorar patrones en el gasto diario.
*   **Programadores:** Que busquen una aplicación de ejemplo en Python con GUI (PyQt5/Tkinter) y deseen expandir sus funcionalidades (por ejemplo, agregar más fórmulas, opciones de visualización, integración con bases de datos).

---

## Licencia

Este proyecto está bajo la Licencia Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International.
Consulta el archivo `LICENSE` para más detalles o visita:
https://creativecommons.org/licenses/by-nc-nd/4.0/

---

**Autor:** Alexander Martínez González (UnfairAdventage \\ UknownByAnxer)

**Fecha:** 04-06-2025