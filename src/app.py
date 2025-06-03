#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Aplicación principal para el cálculo de criticalidad del gasto metabólico.
"""

from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                            QLabel, QLineEdit, QComboBox, QPushButton, QTableWidget,
                            QTableWidgetItem, QSpinBox, QMessageBox, QTabWidget)
from PyQt5.QtCore import Qt
import numpy as np
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
        
        # Formulario de datos personales
        form_layout = QHBoxLayout()
        
        # Sexo
        sex_layout = QVBoxLayout()
        sex_layout.addWidget(QLabel('Sexo:'))
        self.sex_combo = QComboBox()
        self.sex_combo.addItems(['M', 'F'])
        sex_layout.addWidget(self.sex_combo)
        form_layout.addLayout(sex_layout)
        
        # Peso
        weight_layout = QVBoxLayout()
        weight_layout.addWidget(QLabel('Peso (kg):'))
        self.weight_input = QLineEdit()
        weight_layout.addWidget(self.weight_input)
        form_layout.addLayout(weight_layout)
        
        # Altura
        height_layout = QVBoxLayout()
        height_layout.addWidget(QLabel('Altura (cm):'))
        self.height_input = QLineEdit()
        height_layout.addWidget(self.height_input)
        form_layout.addLayout(height_layout)
        
        # Edad
        age_layout = QVBoxLayout()
        age_layout.addWidget(QLabel('Edad (años):'))
        self.age_input = QLineEdit()
        age_layout.addWidget(self.age_input)
        form_layout.addLayout(age_layout)
        
        input_layout.addLayout(form_layout)
        
        # Tabla de ejercicio
        exercise_layout = QVBoxLayout()
        exercise_layout.addWidget(QLabel('Minutos de ejercicio por día:'))
        self.exercise_table = QTableWidget()
        self.exercise_table.setColumnCount(1)
        self.exercise_table.setHorizontalHeaderLabels(['Minutos'])
        exercise_layout.addWidget(self.exercise_table)
        input_layout.addLayout(exercise_layout)
        
        # Botón para agregar días
        add_day_btn = QPushButton('Agregar Día')
        add_day_btn.clicked.connect(self.add_exercise_day)
        input_layout.addWidget(add_day_btn)
        
        # Botón calcular
        calculate_btn = QPushButton('Calcular')
        calculate_btn.clicked.connect(self.calculate)
        input_layout.addWidget(calculate_btn)
        
        tabs.addTab(input_tab, "Datos de Entrada")
        
        # Pestaña de resultados
        results_tab = QWidget()
        results_layout = QVBoxLayout(results_tab)
        
        # Selector de K
        k_layout = QHBoxLayout()
        k_layout.addWidget(QLabel('Frecuencia K:'))
        self.k_spin = QSpinBox()
        self.k_spin.setMinimum(1)
        self.k_spin.setMaximum(100)
        self.k_spin.valueChanged.connect(self.update_fourier_table)
        k_layout.addWidget(self.k_spin)
        results_layout.addLayout(k_layout)
        
        # Tabla de resultados
        self.results_table = QTableWidget()
        results_layout.addWidget(self.results_table)
        
        tabs.addTab(results_tab, "Resultados")
        
    def add_exercise_day(self):
        """Agrega una nueva fila para ingresar minutos de ejercicio."""
        current_row = self.exercise_table.rowCount()
        self.exercise_table.insertRow(current_row)
        
    def calculate(self):
        """Realiza los cálculos y actualiza las tablas."""
        try:
            # Obtener datos del formulario
            sex = self.sex_combo.currentText()
            weight = float(self.weight_input.text())
            height = float(self.height_input.text())
            age = int(self.age_input.text())
            
            # Obtener minutos de ejercicio
            exercise_minutes = []
            for row in range(self.exercise_table.rowCount()):
                item = self.exercise_table.item(row, 0)
                if item and item.text():
                    exercise_minutes.append(float(item.text()))
                else:
                    exercise_minutes.append(0.0)
            
            # Crear objeto Person
            self.person = Person(sex, weight, height, age, exercise_minutes)
            
            # Actualizar tabla de resultados
            self.update_results_table()
            
        except ValueError as e:
            QMessageBox.warning(self, 'Error', 'Por favor, ingrese valores numéricos válidos.')
            
    def update_results_table(self):
        """Actualiza la tabla de resultados con los cálculos."""
        if not self.person:
            return
            
        # Configurar tabla
        self.results_table.setRowCount(len(self.person.exercise_minutes))
        self.results_table.setColumnCount(5)
        self.results_table.setHorizontalHeaderLabels([
            'Día', 'Min. Ejercicio', 'TMB', 'AF', 'GB'
        ])
        
        # Llenar datos
        bmr = self.person.calculate_bmr()
        daily_expenditure = self.person.calculate_daily_expenditure()
        
        for i, (minutes, gb) in enumerate(zip(self.person.exercise_minutes, daily_expenditure)):
            self.results_table.setItem(i, 0, QTableWidgetItem(str(i + 1)))
            self.results_table.setItem(i, 1, QTableWidgetItem(str(minutes)))
            self.results_table.setItem(i, 2, QTableWidgetItem(f"{bmr:.2f}"))
            self.results_table.setItem(i, 3, QTableWidgetItem(str(minutes)))
            self.results_table.setItem(i, 4, QTableWidgetItem(f"{gb:.2f}"))
            
    def update_fourier_table(self):
        """Actualiza la tabla de coeficientes de Fourier."""
        if not self.person:
            return
            
        k = self.k_spin.value()
        a_k, b_k = self.person.calculate_fourier_coefficients(k)
        
        # Crear nueva tabla para coeficientes de Fourier
        fourier_table = QTableWidget()
        fourier_table.setRowCount(1)
        fourier_table.setColumnCount(4)
        fourier_table.setHorizontalHeaderLabels([
            'K', 'a_k', 'b_k', 'log10(K)'
        ])
        
        fourier_table.setItem(0, 0, QTableWidgetItem(str(k)))
        fourier_table.setItem(0, 1, QTableWidgetItem(f"{a_k:.4f}"))
        fourier_table.setItem(0, 2, QTableWidgetItem(f"{b_k:.4f}"))
        fourier_table.setItem(0, 3, QTableWidgetItem(f"{np.log10(k):.4f}"))
        
        # Reemplazar la tabla actual
        self.results_table.setRowCount(0)
        self.results_table.setColumnCount(4)
        self.results_table.setHorizontalHeaderLabels([
            'K', 'a_k', 'b_k', 'log10(K)'
        ])
        
        for col in range(4):
            item = fourier_table.item(0, col)
            if item:
                self.results_table.setItem(0, col, QTableWidgetItem(item.text())) 