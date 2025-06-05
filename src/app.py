#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Aplicación principal para el cálculo de criticalidad del gasto metabólico.
"""

from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                            QLabel, QLineEdit, QComboBox, QPushButton, QTableWidget,
                            QTableWidgetItem, QSpinBox, QMessageBox, QTabWidget,
                            QFileDialog, QTextEdit)
from PyQt5.QtCore import Qt
from PyQt5.QtWebEngineWidgets import QWebEngineView
import numpy as np
import pandas as pd
from models.person import Person

class MetabolicApp(QMainWindow):
    """Ventana principal de la aplicación."""
    
    def __init__(self):
        super().__init__()
        self.person = None
        self.init_ui()
        
    def init_ui(self):
        """Inicializa la interfaz de usuario."""
        self.setWindowTitle('Calculadora de Criticalidad Metabólica')
        self.setGeometry(100, 100, 1200, 800)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Pestañas
        tabs = QTabWidget()
        layout.addWidget(tabs)
        
        # Pestaña de entrada de datos
        input_tab = QWidget()
        input_layout = QVBoxLayout(input_tab)
        
        # Tabla de datos personales y ejercicio
        self.input_table = QTableWidget()
        self.input_table.setRowCount(4)
        self.input_table.setColumnCount(2)
        self.input_table.setHorizontalHeaderLabels(['Campo', 'Valor'])
        campos = ['Sexo (M/F)', 'Peso (kg)', 'Altura (cm)', 'Edad (años)']
        for i, campo in enumerate(campos):
            self.input_table.setItem(i, 0, QTableWidgetItem(campo))
        self.input_table.setItem(0, 1, QTableWidgetItem('M'))
        self.input_table.setItem(1, 1, QTableWidgetItem(''))
        self.input_table.setItem(2, 1, QTableWidgetItem(''))
        self.input_table.setItem(3, 1, QTableWidgetItem(''))
        input_layout.addWidget(self.input_table)
        
        # Tabla de minutos de ejercicio por día
        self.exercise_table = QTableWidget()
        self.exercise_table.setColumnCount(1)
        self.exercise_table.setHorizontalHeaderLabels(['Minutos de ejercicio'])
        self.exercise_table.setRowCount(5)
        for i in range(5):
            self.exercise_table.setItem(i, 0, QTableWidgetItem(''))
        input_layout.addWidget(self.exercise_table)
        
        # Botón para agregar día
        add_day_btn = QPushButton('Agregar Día')
        add_day_btn.clicked.connect(self.add_exercise_day)
        input_layout.addWidget(add_day_btn)
        
        # Botón para eliminar día
        remove_day_btn = QPushButton('Eliminar Día')
        remove_day_btn.clicked.connect(self.remove_exercise_day)
        input_layout.addWidget(remove_day_btn)
        
        # Botón calcular
        calculate_btn = QPushButton('Calcular')
        calculate_btn.clicked.connect(self.calculate)
        input_layout.addWidget(calculate_btn)
        
        tabs.addTab(input_tab, "Datos de Entrada")
        
        # Pestaña de resultados diarios
        daily_tab = QWidget()
        daily_layout = QVBoxLayout(daily_tab)
        self.daily_table = QTableWidget()
        daily_layout.addWidget(self.daily_table)
        tabs.addTab(daily_tab, "Datos Diarios")
        
        # Pestaña de Fourier
        fourier_tab = QWidget()
        fourier_layout = QVBoxLayout(fourier_tab)
        
        # Selector de K
        k_layout = QHBoxLayout()
        k_layout.addWidget(QLabel('Frecuencia K:'))
        self.k_spin = QSpinBox()
        self.k_spin.setMinimum(1)
        self.k_spin.setMaximum(100)
        self.k_spin.valueChanged.connect(self.update_fourier_table)
        k_layout.addWidget(self.k_spin)
        fourier_layout.addLayout(k_layout)
        
        # Tabla de Fourier
        self.fourier_table = QTableWidget()
        fourier_layout.addWidget(self.fourier_table)
        
        # Resumen de Fourier
        self.fourier_summary = QTableWidget()
        self.fourier_summary.setRowCount(1)
        self.fourier_summary.setColumnCount(4)
        self.fourier_summary.setHorizontalHeaderLabels([
            'K', 'a_k', 'b_k', 'log10(K)'
        ])
        fourier_layout.addWidget(self.fourier_summary)
        
        # Tabla de resumen de Fourier (todas las K)
        self.fourier_full_summary = QTableWidget()
        fourier_layout.addWidget(self.fourier_full_summary)
        
        # Área para mostrar la fórmula y sustitución en LaTeX renderizado
        self.fourier_formula_view = QWebEngineView()
        fourier_layout.addWidget(self.fourier_formula_view)
        # Tabla de log10(K) vs log10(Ak)
        self.log_table = QTableWidget()
        fourier_layout.addWidget(self.log_table)
        
        tabs.addTab(fourier_tab, "Análisis de Fourier")
        
        # Pestaña de estadísticas
        stats_tab = QWidget()
        stats_layout = QVBoxLayout(stats_tab)
        self.stats_table = QTableWidget()
        stats_layout.addWidget(self.stats_table)
        tabs.addTab(stats_tab, "Análisis Estadístico")
        
        # Botón exportar
        export_btn = QPushButton('Exportar a Excel')
        export_btn.clicked.connect(self.export_to_excel)
        layout.addWidget(export_btn)
        
    def add_exercise_day(self):
        current_row = self.exercise_table.rowCount()
        self.exercise_table.insertRow(current_row)
        self.exercise_table.setItem(current_row, 0, QTableWidgetItem(''))

    def remove_exercise_day(self):
        current_row = self.exercise_table.rowCount()
        if current_row > 1:
            self.exercise_table.removeRow(current_row - 1)

    def calculate(self):
        """Realiza los cálculos y actualiza las tablas."""
        try:
            sexo = self.input_table.item(0, 1).text().strip()
            peso = float(self.input_table.item(1, 1).text())
            altura = float(self.input_table.item(2, 1).text())
            edad = int(self.input_table.item(3, 1).text())
            minutos = []
            for row in range(self.exercise_table.rowCount()):
                item = self.exercise_table.item(row, 0)
                if item and item.text().strip():
                    minutos.append(float(item.text().strip()))
            if not minutos:
                raise ValueError('Debes ingresar al menos un día de ejercicio.')
            self.person = Person(sexo, peso, altura, edad, minutos)
            self.update_daily_table()
            self.update_fourier_table()
            self.update_stats_table()
        except Exception as e:
            QMessageBox.warning(self, 'Error', f'Error en los datos: {e}')
            
    def update_daily_table(self):
        """Actualiza la tabla de datos diarios."""
        if not self.person:
            return
            
        daily_data = self.person.get_daily_data()
        
        # Configurar tabla
        self.daily_table.setRowCount(len(daily_data))
        self.daily_table.setColumnCount(5)
        self.daily_table.setHorizontalHeaderLabels([
            'Día', 'Ejercicio (min)', 'TMB', 'AF', 'GB'
        ])
        
        # Llenar datos
        for i, data in enumerate(daily_data):
            self.daily_table.setItem(i, 0, QTableWidgetItem(str(data['day'])))
            self.daily_table.setItem(i, 1, QTableWidgetItem(f"{data['exercise']:.0f}"))
            self.daily_table.setItem(i, 2, QTableWidgetItem(f"{data['tmb']:.3f}"))
            self.daily_table.setItem(i, 3, QTableWidgetItem(f"{data['af']:.2f}"))
            self.daily_table.setItem(i, 4, QTableWidgetItem(f"{data['gb']:.2f}"))
            
    def update_fourier_table(self):
        """Actualiza la tabla de coeficientes de Fourier."""
        if not self.person:
            return
        k = self.k_spin.value()
        fourier_data = self.person.get_fourier_table(k)
        # Configurar tabla
        self.fourier_table.setRowCount(len(fourier_data))
        self.fourier_table.setColumnCount(6)
        self.fourier_table.setHorizontalHeaderLabels([
            'n', 'x', 'cos', 'sin', 'x*cos', 'x*sin'
        ])
        # Llenar datos
        for i, data in enumerate(fourier_data):
            self.fourier_table.setItem(i, 0, QTableWidgetItem(str(data['n'])))
            self.fourier_table.setItem(i, 1, QTableWidgetItem(f"{data['x']:.2f}"))
            self.fourier_table.setItem(i, 2, QTableWidgetItem(f"{data['cos']:.4f}"))
            self.fourier_table.setItem(i, 3, QTableWidgetItem(f"{data['sin']:.4f}"))
            self.fourier_table.setItem(i, 4, QTableWidgetItem(f"{data['x_cos']:.2f}"))
            self.fourier_table.setItem(i, 5, QTableWidgetItem(f"{data['x_sin']:.2f}"))
        # Actualizar resumen
        a_k, b_k, Ak, log10_Ak = self.person.calculate_fourier_coefficients(k)
        self.fourier_summary.setRowCount(1)
        self.fourier_summary.setColumnCount(5)
        self.fourier_summary.setHorizontalHeaderLabels([
            'K', 'a_k', 'b_k', 'Ak', 'log10(Ak)'
        ])
        self.fourier_summary.setItem(0, 0, QTableWidgetItem(str(k)))
        self.fourier_summary.setItem(0, 1, QTableWidgetItem(f"{a_k:.4f}"))
        self.fourier_summary.setItem(0, 2, QTableWidgetItem(f"{b_k:.4f}"))
        self.fourier_summary.setItem(0, 3, QTableWidgetItem(f"{Ak:.4f}"))
        self.fourier_summary.setItem(0, 4, QTableWidgetItem(f"{log10_Ak:.4f}"))
        # Proceso completo para todos los K (tabla resumen en HTML con MathJax)
        N = len(self.person.calculate_daily_expenditure())
        table_rows = []
        for k_val in range(1, N+1):
            a_k_val, b_k_val, Ak_val, log10_Ak_val = self.person.calculate_fourier_coefficients(k_val)
            row = f"""
<tr>
<td> {k_val} </td>
<td> $${{a_{{{k_val}}} = {a_k_val:.4f}}}$$ </td>
<td> $${{b_{{{k_val}}} = {b_k_val:.4f}}}$$ </td>
<td> $${{A_{{{k_val}}} = {Ak_val:.4f}}}$$ </td>
<td> $${{\log_{{10}}({k_val}) = {np.log10(k_val):.4f}}}$$ </td>
<td> $${{\log_{{10}}(A_{{{k_val}}}) = {log10_Ak_val:.4f}}}$$ </td>
</tr>
"""
            table_rows.append(row)
        table_html = f"""
<table border='1' cellpadding='6' style='border-collapse:collapse;'>
<tr>
<th>K</th><th>a_k</th><th>b_k</th><th>A_k</th><th>log10(K)</th><th>log10(Ak)</th>
</tr>
{''.join(table_rows)}
</table>
"""
        html = f"""
<html><head>
<script src='https://polyfill.io/v3/polyfill.min.js?features=es6'></script>
<script src='https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js'></script>
<style>body {{ font-family: Arial; font-size: 16px; }}</style>
</head><body>
{table_html}
</body></html>
"""
        self.fourier_formula_view.setHtml(html)
        # Tabla de log10(K) vs log10(Ak) para K=1..N
        self.log_table.setRowCount(N)
        self.log_table.setColumnCount(3)
        self.log_table.setHorizontalHeaderLabels(['K', 'log10(K)', 'log10(Ak)'])
        for k_val in range(1, N+1):
            _, _, Ak_k, log10_Ak_k = self.person.calculate_fourier_coefficients(k_val)
            self.log_table.setItem(k_val-1, 0, QTableWidgetItem(str(k_val)))
            self.log_table.setItem(k_val-1, 1, QTableWidgetItem(f"{np.log10(k_val):.4f}"))
            self.log_table.setItem(k_val-1, 2, QTableWidgetItem(f"{log10_Ak_k:.4f}"))
            
    def update_stats_table(self):
        """Actualiza la tabla de análisis estadístico."""
        if not self.person:
            return
            
        stats = self.person.get_statistical_analysis()
        
        # Configurar tabla
        self.stats_table.setRowCount(1)
        self.stats_table.setColumnCount(8)
        self.stats_table.setHorizontalHeaderLabels([
            'Media X', 'Media Y', 'Var X', 'Var Y',
            'Correlación', 'Σxy', 'Σx²', 'Σy²'
        ])
        
        # Llenar datos
        self.stats_table.setItem(0, 0, QTableWidgetItem(f"{stats.mean_x:.2f}"))
        self.stats_table.setItem(0, 1, QTableWidgetItem(f"{stats.mean_y:.2f}"))
        self.stats_table.setItem(0, 2, QTableWidgetItem(f"{stats.variance_x:.2f}"))
        self.stats_table.setItem(0, 3, QTableWidgetItem(f"{stats.variance_y:.2f}"))
        self.stats_table.setItem(0, 4, QTableWidgetItem(f"{stats.correlation:.4f}"))
        self.stats_table.setItem(0, 5, QTableWidgetItem(f"{stats.xy_sum:.2f}"))
        self.stats_table.setItem(0, 6, QTableWidgetItem(f"{stats.x2_sum:.2f}"))
        self.stats_table.setItem(0, 7, QTableWidgetItem(f"{stats.y2_sum:.2f}"))
        
    def export_to_excel(self):
        """Exporta los datos a un archivo Excel."""
        if not self.person:
            QMessageBox.warning(self, 'Error', 'No hay datos para exportar.')
            return
            
        try:
            file_name, _ = QFileDialog.getSaveFileName(
                self,
                "Guardar archivo Excel",
                "",
                "Excel Files (*.xlsx)"
            )
            
            if file_name:
                # Crear DataFrame para datos diarios
                daily_data = self.person.get_daily_data()
                daily_df = pd.DataFrame(daily_data)
                
                # Crear DataFrame para Fourier
                k = self.k_spin.value()
                fourier_data = self.person.get_fourier_table(k)
                fourier_df = pd.DataFrame(fourier_data)
                
                # Crear DataFrame para estadísticas
                stats = self.person.get_statistical_analysis()
                stats_df = pd.DataFrame([{
                    'Media X': stats.mean_x,
                    'Media Y': stats.mean_y,
                    'Var X': stats.variance_x,
                    'Var Y': stats.variance_y,
                    'Correlación': stats.correlation,
                    'Σxy': stats.xy_sum,
                    'Σx²': stats.x2_sum,
                    'Σy²': stats.y2_sum
                }])
                
                # Crear Excel writer
                with pd.ExcelWriter(file_name) as writer:
                    daily_df.to_excel(writer, sheet_name='Datos Diarios', index=False)
                    fourier_df.to_excel(writer, sheet_name='Fourier', index=False)
                    stats_df.to_excel(writer, sheet_name='Estadísticas', index=False)
                    
                QMessageBox.information(self, 'Éxito', 'Datos exportados correctamente.')
                
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Error al exportar: {str(e)}') 