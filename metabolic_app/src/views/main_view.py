#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTabWidget, QVBoxLayout, QWidget, QLabel, QLineEdit, QPushButton, QFormLayout, QComboBox, QTableWidget, QTableWidgetItem, QHBoxLayout, QHeaderView, QMessageBox, QFileDialog, QGridLayout, QSpacerItem, QSizePolicy)
from PyQt5.QtCore import Qt # Import Qt for text alignment

# Import helper functions for validation
from src.utils.helpers import validate_integer_input, validate_numeric_input, validate_sex_input

# Import metabolic calculation functions
from src.models.metabolic import calculate_tmb, calculate_af, calculate_gb

# Import Fourier analysis functions
from src.models.fourier import calculate_specific_fourier_coefficients, calculate_log_transformations

# Import statistical analysis functions
from src.models.statistics import calculate_mean, calculate_std_dev, calculate_regression_slope, calculate_regression_intercept, calculate_correlation_coefficient

# Import matplotlib for plotting
import matplotlib.pyplot as plt

# Import pandas for data handling and export
import pandas as pd

class MainWindow(QMainWindow):
    """Main window of the Metabolic Analysis application."""
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Metabolic Analysis")
        self.setGeometry(100, 100, 800, 600) # (x, y, width, height)

        # Apply modern styling
        self.setStyleSheet(self._get_modern_stylesheet())

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.tab_widget = QTabWidget()
        self.layout.addWidget(self.tab_widget)

        # Create tabs
        self.personal_data_tab = QWidget()
        self.exercise_data_tab = QWidget()
        self.daily_results_tab = QWidget()
        self.fourier_analysis_tab = QWidget()
        self.statistical_analysis_tab = QWidget()

        # Add tabs to the tab widget
        self.tab_widget.addTab(self.personal_data_tab, "Datos Personales")
        self.tab_widget.addTab(self.exercise_data_tab, "Ejercicio Diario")
        self.tab_widget.addTab(self.daily_results_tab, "Resultados Diarios")
        self.tab_widget.addTab(self.fourier_analysis_tab, "Análisis de Fourier")
        self.tab_widget.addTab(self.statistical_analysis_tab, "Análisis Estadístico")

        self._setup_personal_data_tab()
        self._setup_exercise_data_tab()
        self._setup_daily_results_tab()
        self._setup_fourier_analysis_tab()
        self._setup_statistical_analysis_tab()

        # Connect signals
        self.next_button.clicked.connect(self._process_personal_data)
        self.calculate_button.clicked.connect(self._calculate_metabolic_data)

        # Store calculated data for analysis
        self._daily_gb_values = []
        self._num_days = 0
        self._k_values = []
        self._a_k_values = []
        self._b_k_values = []
        self._A_k_values = []
        self._log10_k_values = [] # x values for regression
        self._log10_A_k_values = [] # y values for regression
        self._regression_alpha = 0.0
        self._regression_c = 0.0
        self._correlation_r = 0.0

    def _get_modern_stylesheet(self) -> str:
        """Returns a modern stylesheet string for the application."""
        return """
/* Main window and general styling */
QMainWindow {
    background-color: #f5f7fa;
    font-family: 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
    font-size: 11pt;
}

QWidget {
    background-color: #f5f7fa;
    color: #2d3748;
}

/* Tab widget styling */
QTabWidget::pane {
    border: 1px solid #e2e8f0;
    background-color: #ffffff;
    border-radius: 6px;
    margin-top: 4px;
}

QTabWidget::tab-bar {
    left: 8px;
}

QTabBar::tab {
    background: #edf2f7;
    border: 1px solid #e2e8f0;
    border-bottom: none;
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
    min-width: 120px;
    padding: 8px 16px;
    margin-right: 4px;
    color: #4a5568;
}

QTabBar::tab:hover {
    background: #e2e8f0;
}

QTabBar::tab:selected {
    background: #ffffff;
    color: #2d3748;
    font-weight: 500;
}

/* Form elements */
QLabel {
    color: #4a5568;
    margin-bottom: 4px;
    font-size: 10.5pt;
}

QLineEdit, QComboBox {
    border: 1px solid #e2e8f0;
    border-radius: 6px;
    padding: 6px 8px;
    background-color: #ffffff;
    min-height: 28px;
    font-size: 10.5pt;
}

QLineEdit:focus, QComboBox:focus {
    border: 1px solid #4299e1;
    outline: none;
}

QComboBox::drop-down {
    border: 0px;
    width: 24px;
}

QComboBox::down-arrow {
    image: url(arrow_down.png);
    width: 12px;
    height: 12px;
}

/* Buttons */
QPushButton {
    color: white;
    background-color: #4299e1;
    border: none;
    border-radius: 6px;
    padding: 8px 16px;
    font-weight: 500;
    min-width: 80px;
}

QPushButton:hover {
    background-color: #3182ce;
}

QPushButton:pressed {
    background-color: #2b6cb0;
}

/* Tables */
QTableWidget {
    gridline-color: #e2e8f0;
    background-color: #ffffff;
    alternate-background-color: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 6px;
    font-size: 10pt;
}

QTableWidget::item {
    padding: 6px 8px;
}

QHeaderView::section {
    background-color: #edf2f7;
    color: #2d3748;
    padding: 8px;
    border: 1px solid #e2e8f0;
    font-weight: 500;
}

QHeaderView::section:checked {
    background-color: #e2e8f0;
}

/* Export button specific */
QPushButton#exportButton {
    background-color: #48bb78;
}

QPushButton#exportButton:hover {
    background-color: #38a169;
}

QPushButton#exportButton:pressed {
    background-color: #2f855a;
}
        """

    def _setup_personal_data_tab(self):
        """Sets up the layout and widgets for the Personal Data tab."""
        # Use a QVBoxLayout as the main layout for the tab
        main_layout = QVBoxLayout()
        self.personal_data_tab.setLayout(main_layout)

        # Create a horizontal layout to center the form and button
        center_layout = QHBoxLayout()
        main_layout.addLayout(center_layout)

        # Add horizontal spacers to center the form
        center_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        # Use a QVBoxLayout for the form and button to stack them vertically
        form_and_button_layout = QVBoxLayout()
        center_layout.addLayout(form_and_button_layout)

        # Left side: Personal Data Inputs using QFormLayout
        personal_data_layout = QFormLayout()
        form_and_button_layout.addLayout(personal_data_layout)

        self.sex_combo = QComboBox()
        self.sex_combo.addItems(['Masculino', 'Femenino'])
        personal_data_layout.addRow("Sexo:", self.sex_combo)

        self.weight_input = QLineEdit()
        personal_data_layout.addRow("Peso (kg):", self.weight_input)

        self.height_input = QLineEdit()
        personal_data_layout.addRow("Altura (cm):", self.height_input)

        self.age_input = QLineEdit()
        personal_data_layout.addRow("Edad (años):", self.age_input)

        self.days_input = QLineEdit()
        personal_data_layout.addRow("Número de días de análisis (N):", self.days_input)

        # Add some spacing between the form fields and the button
        form_and_button_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed))

        # Add the button, centered horizontally within its layout
        button_layout = QHBoxLayout()
        button_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.next_button = QPushButton("Siguiente")
        # Set a fixed width for the button for better control in the centered layout
        self.next_button.setFixedWidth(150) # Example fixed width
        button_layout.addWidget(self.next_button)
        button_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        form_and_button_layout.addLayout(button_layout)

        # Add vertical spacer to push the centered content to the top
        main_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Add horizontal spacers to center the form (matching the left spacer)
        center_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

    def _setup_exercise_data_tab(self):
        """Sets up the layout and widgets for the Exercise Data tab."""
        main_layout = QVBoxLayout()
        self.exercise_data_tab.setLayout(main_layout)

        # Top: Exercise Table
        self.exercise_table = QTableWidget()
        self.exercise_table.setColumnCount(2)
        self.exercise_table.setHorizontalHeaderLabels(["Día (n)", "Minutos de ejercicio"])
        # Set header stretch to fill the available space
        header = self.exercise_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        self.exercise_table.setAlternatingRowColors(True) # Enable alternating row colors via stylesheet

        main_layout.addWidget(self.exercise_table)

        # Bottom: Calculate button, aligned to the right
        button_layout = QHBoxLayout()
        button_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.calculate_button = QPushButton("Calcular TMB, AF y GB")
        button_layout.addWidget(self.calculate_button)

        main_layout.addLayout(button_layout)

    def _setup_daily_results_tab(self):
        """Sets up the layout and widgets for the Daily Results tab."""
        layout = QVBoxLayout()
        self.daily_results_tab.setLayout(layout)

        self.results_table = QTableWidget()
        self.results_table.setColumnCount(5)
        self.results_table.setHorizontalHeaderLabels(["Día", "Minutos de ejercicio", "TMB", "AF", "GB"])
        # Set header stretch to fill the available space
        header = self.results_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        self.results_table.setAlternatingRowColors(True)

        layout.addWidget(self.results_table)

        self.export_daily_results_button = QPushButton("Exportar Resultados Diarios")
        layout.addWidget(self.export_daily_results_button)
        self.export_daily_results_button.clicked.connect(lambda: self._export_results(self.results_table, "resultados_diarios"))

    def _setup_fourier_analysis_tab(self):
        """Sets up the layout and widgets for the Fourier Analysis tab."""
        layout = QVBoxLayout()
        self.fourier_analysis_tab.setLayout(layout)

        self.fourier_table = QTableWidget()
        # Corrected column count and headers to match Fourier results displayed
        self.fourier_table.setColumnCount(9)
        self.fourier_table.setHorizontalHeaderLabels(["k", "a_k", "b_k", "A_k", "log10(k)", "log10(A_k)", "x", "y", "xy"])
        # Set header stretch to fill the available space
        header = self.fourier_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        self.fourier_table.setAlternatingRowColors(True)

        layout.addWidget(self.fourier_table)

        self.export_fourier_results_button = QPushButton("Exportar Resultados Fourier")
        layout.addWidget(self.export_fourier_results_button)
        self.export_fourier_results_button.clicked.connect(lambda: self._export_results(self.fourier_table, "resultados_fourier"))

    def _setup_statistical_analysis_tab(self):
        """Sets up the layout and widgets for the Statistical Analysis tab."""
        layout = QFormLayout()
        self.statistical_analysis_tab.setLayout(layout)

        self.alpha_label = QLabel("\u03B1 (Slope):") # Unicode for alpha
        self.alpha_value = QLabel("")
        layout.addRow(self.alpha_label, self.alpha_value)

        self.c_label = QLabel("C (Intercept):")
        self.c_value = QLabel("")
        layout.addRow(self.c_label, self.c_value)

        self.r_label = QLabel("r (Correlation Coefficient):")
        self.r_value = QLabel("")
        layout.addRow(self.r_label, self.r_value)

        self.mean_x_label = QLabel("\u00AFx (Mean of x):") # Unicode for x-bar
        self.mean_x_value = QLabel("")
        layout.addRow(self.mean_x_label, self.mean_x_value)

        self.mean_y_label = QLabel("\u00AFy (Mean of y):") # Unicode for y-bar
        self.mean_y_value = QLabel("")
        layout.addRow(self.mean_y_label, self.mean_y_value)

        self.std_dev_x_label = QLabel("\u03C3x (Std Dev of x):") # Unicode for sigma x
        self.std_dev_x_value = QLabel("")
        layout.addRow(self.std_dev_x_label, self.std_dev_x_value)

        self.std_dev_y_label = QLabel("\u03C3y (Std Dev of y):") # Unicode for sigma y
        self.std_dev_y_value = QLabel("")
        layout.addRow(self.std_dev_y_label, self.std_dev_y_value)

        self.generate_plot_button = QPushButton("Generar Gráfico x vs y")
        layout.addRow(self.generate_plot_button)
        self.generate_plot_button.clicked.connect(self._generate_plot)

    def _process_personal_data(self):
        """Reads and validates personal data and updates the exercise table."""
        try:
            # Validate and get the number of days
            num_days_str = self.days_input.text()
            num_days = validate_integer_input(num_days_str, "Número de días de análisis")

            if num_days <= 0:
                 QMessageBox.warning(self, "Invalid Input", "Número de días de análisis (N) must be a positive integer.")
                 return

            # Clear existing rows and set row count for exercise table
            self.exercise_table.setRowCount(num_days)

            # Populate the 'Día (n)' column
            for i in range(num_days):
                item = QTableWidgetItem(str(i + 1))
                item.setFlags(item.flags() & ~Qt.ItemIsEditable) # Make day column read-only
                self.exercise_table.setItem(i, 0, item)

            # Switch to the Exercise Data tab
            self.tab_widget.setCurrentIndex(1) # Index 1 is Exercise Diario

        except ValueError as e:
            QMessageBox.warning(self, "Invalid Input", str(e))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An unexpected error occurred: {e}")

    def _calculate_metabolic_data(self):
        """Reads data, performs metabolic calculations, and displays results."""
        try:
            # 1. Read and validate personal data
            sex = validate_sex_input(self.sex_combo.currentText())
            weight = validate_numeric_input(self.weight_input.text(), "Peso")
            height = validate_numeric_input(self.height_input.text(), "Altura")
            age = validate_integer_input(self.age_input.text(), "Edad")
            self._num_days = self.exercise_table.rowCount() # Get N from the exercise table row count

            if self._num_days == 0:
                 QMessageBox.warning(self, "Missing Data", "Please enter the number of days and exercise minutes.")
                 return

            # 2. Read and validate exercise minutes data
            exercise_minutes_list = []
            for i in range(self._num_days):
                item = self.exercise_table.item(i, 1)
                if item is None or item.text() == "":
                     QMessageBox.warning(self, "Missing Data", f"Please enter exercise minutes for Day {i+1}.")
                     return
                exercise_minutes = validate_numeric_input(item.text(), f"Minutos de ejercicio for Day {i+1}")
                exercise_minutes_list.append(exercise_minutes)

            # 3. Perform metabolic calculations and populate results table
            self.results_table.setRowCount(self._num_days)
            self._daily_gb_values = []

            for i in range(self._num_days):
                day = i + 1
                exercise_minutes = exercise_minutes_list[i]

                tmb = calculate_tmb(sex, weight, height, age)
                af = calculate_af(exercise_minutes)
                gb = calculate_gb(tmb, af)
                self._daily_gb_values.append(gb)

                self.results_table.setItem(i, 0, QTableWidgetItem(str(day)))
                self.results_table.setItem(i, 1, QTableWidgetItem(str(exercise_minutes)))
                self.results_table.setItem(i, 2, QTableWidgetItem(f"{tmb:.2f}")) # Format to 2 decimal places
                self.results_table.setItem(i, 3, QTableWidgetItem(f"{af:.2f}"))
                self.results_table.setItem(i, 4, QTableWidgetItem(f"{gb:.2f}"))

            # Perform Fourier and Statistical analysis
            self._perform_fourier_analysis()
            self._perform_statistical_analysis()

            # Switch to the Daily Results tab
            self.tab_widget.setCurrentIndex(2) # Index 2 is Resultados Diarios

        except ValueError as e:
            QMessageBox.warning(self, "Invalid Input", str(e))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An unexpected error occurred: {e}")

    def _perform_fourier_analysis(self):
        """Performs Fourier analysis and populates the Fourier analysis table."""
        if not self._daily_gb_values or self._num_days == 0:
            # No data to analyze, clear the table and return
            self.fourier_table.setRowCount(0)
            self._k_values = []
            self._a_k_values = []
            self._b_k_values = []
            self._A_k_values = []
            self._log10_k_values = []
            self._log10_A_k_values = []
            return

        try:
            N = self._num_days
            daily_gb_values = self._daily_gb_values

            # Determine the range of k values to display (from 1 up to min(N, 5))
            max_k_to_display = min(N, 5)

            # Calculate Fourier coefficients for the desired k values (1 to max_k_to_display)
            self._k_values, self._a_k_values, self._b_k_values, self._A_k_values = calculate_specific_fourier_coefficients(daily_gb_values, N, max_k_to_display)

            # Calculate log transformations for the displayed k values
            # These are already for k > 0 since calculate_specific_fourier_coefficients starts k from 1
            self._log10_k_values, self._log10_A_k_values = calculate_log_transformations(self._k_values, self._A_k_values)

            # Populate the Fourier table
            self.fourier_table.setRowCount(len(self._k_values))
            for i in range(len(self._k_values)):
                k = self._k_values[i]
                ak = self._a_k_values[i]
                bk = self._b_k_values[i]
                Ak = self._A_k_values[i]

                self.fourier_table.setItem(i, 0, QTableWidgetItem(str(k)))
                self.fourier_table.setItem(i, 1, QTableWidgetItem(f"{ak:.4f}")) # Format to 4 decimal places
                self.fourier_table.setItem(i, 2, QTableWidgetItem(f"{bk:.4f}"))
                self.fourier_table.setItem(i, 3, QTableWidgetItem(f"{Ak:.4f}"))

                # Get corresponding log transformed values for the current k
                # These are only available for k > 0 and are stored in _log10_k_values and _log10_A_k_values
                log10_k_str = "N/A"
                log10_Ak_str = "N/A"
                x_str = "N/A"
                y_str = "N/A"
                xy_str = "N/A"

                try:
                    # Find the index of the current k in the list of displayed k values (which starts from 1)
                    log_index = self._k_values.index(k)
                    # Check if this index is valid for log transformed values
                    if log_index < len(self._log10_k_values):
                        log10_k = self._log10_k_values[log_index]
                        log10_Ak = self._log10_A_k_values[log_index]

                        log10_k_str = f"{log10_k:.4f}"
                        log10_Ak_str = f"{log10_Ak:.4f}" if log10_Ak != float('-inf') else "-inf"
                        x_str = log10_k_str
                        y_str = log10_Ak_str

                        # Calculate xy using the numeric log values before formatting
                        numeric_x = log10_k
                        numeric_y = log10_Ak if log10_Ak != float('-inf') else 0 # Treat log(-inf) as 0 for xy calculation
                        xy_str = f"{numeric_x * numeric_y:.4f}"

                except ValueError: # Should not happen if k is in _k_values
                    pass
                except IndexError: # Should not happen if logic is correct
                    pass


                self.fourier_table.setItem(i, 4, QTableWidgetItem(log10_k_str))
                self.fourier_table.setItem(i, 5, QTableWidgetItem(log10_Ak_str))
                self.fourier_table.setItem(i, 6, QTableWidgetItem(x_str))
                self.fourier_table.setItem(i, 7, QTableWidgetItem(y_str))
                self.fourier_table.setItem(i, 8, QTableWidgetItem(xy_str))

        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred during Fourier analysis: {e}")

    def _perform_statistical_analysis(self):
        """Performs statistical analysis on log-transformed Fourier coefficients and displays results."""
        # Use the stored log-transformed values from _perform_fourier_analysis
        x_values = self._log10_k_values
        y_values = self._log10_A_k_values
        N = len(x_values) # N for statistical analysis is the number of log-transformed points (k > 0)

        if N < 2:
            # Not enough data points for regression/correlation (need at least 2)
            # Clear statistical results and stored regression values
            self.alpha_value.setText("")
            self.c_value.setText("")
            self.r_value.setText("")
            self.mean_x_value.setText("")
            self.mean_y_value.setText("")
            self.std_dev_x_value.setText("")
            self.std_dev_y_value.setText("")
            self._regression_alpha = 0.0
            self._regression_c = 0.0
            self._correlation_r = 0.0
            return

        try:
            # Calculate statistical measures
            mean_x = calculate_mean(x_values)
            mean_y = calculate_mean(y_values)
            std_dev_x = calculate_std_dev(x_values, mean_x)
            std_dev_y = calculate_std_dev(y_values, mean_y)
            alpha = calculate_regression_slope(x_values, y_values, N)
            c = calculate_regression_intercept(x_values, y_values, alpha, N)
            r = calculate_correlation_coefficient(x_values, y_values, N)

            # Store regression values for plotting
            self._regression_alpha = alpha
            self._regression_c = c
            self._correlation_r = r

            # Display results
            self.alpha_value.setText(f"{alpha:.4f}") # Format to 4 decimal places
            self.c_value.setText(f"{c:.4f}")
            self.r_value.setText(f"{r:.4f}")
            self.mean_x_value.setText(f"{mean_x:.4f}")
            self.mean_y_value.setText(f"{mean_y:.4f}")
            self.std_dev_x_value.setText(f"{std_dev_x:.4f}")
            self.std_dev_y_value.setText(f"{std_dev_y:.4f}")

        except ValueError as e:
            QMessageBox.warning(self, "Statistical Analysis Error", str(e))
            # Clear results and stored regression values on error
            self.alpha_value.setText("")
            self.c_value.setText("")
            self.r_value.setText("")
            self.mean_x_value.setText("")
            self.mean_y_value.setText("")
            self.std_dev_x_value.setText("")
            self.std_dev_y_value.setText("")
            self._regression_alpha = 0.0
            self._regression_c = 0.0
            self._correlation_r = 0.0
        except ZeroDivisionError as e:
             QMessageBox.warning(self, "Statistical Analysis Error", str(e))
             # Clear results and stored regression values on error
             self.alpha_value.setText("")
             self.c_value.setText("")
             self.r_value.setText("")
             self.mean_x_value.setText("")
             self.mean_y_value.setText("")
             self.std_dev_x_value.setText("")
             self.std_dev_y_value.setText("")
             self._regression_alpha = 0.0
             self._regression_c = 0.0
             self._correlation_r = 0.0
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An unexpected error occurred during statistical analysis: {e}")
            # Clear results and stored regression values on error
            self.alpha_value.setText("")
            self.c_value.setText("")
            self.r_value.setText("")
            self.mean_x_value.setText("")
            self.mean_y_value.setText("")
            self.std_dev_x_value.setText("")
            self.std_dev_y_value.setText("")
            self._regression_alpha = 0.0
            self._regression_c = 0.0
            self._correlation_r = 0.0

    def _generate_plot(self):
        """Generates and displays the scatter plot with the regression line."""
        x_values = self._log10_k_values
        y_values = self._log10_A_k_values

        if not x_values or not y_values or len(x_values) < 2:
            QMessageBox.warning(self, "Plotting Error", "Not enough data points (k > 0) to generate a plot with a regression line.")
            return

        try:
            plt.figure()
            plt.scatter(x_values, y_values, label='Data Points')

            # Plot the regression line: y = alpha * x + C
            # Generate x values for the line based on the range of x_values
            x_line = [min(x_values), max(x_values)]
            y_line = [self._regression_alpha * x + self._regression_c for x in x_line]
            plt.plot(x_line, y_line, color='red', label=f'Regression Line (y = {self._regression_alpha:.4f}x + {self._regression_c:.4f})')

            plt.xlabel('log10(k)')
            plt.ylabel('log10(A_k)')
            plt.title('Análisis de Fourier: log10(A_k) vs log10(k)')
            plt.legend()
            plt.grid(True)
            plt.show()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"An unexpected error occurred during plotting: {e}")

    def _export_results(self, table_widget: QTableWidget, base_filename: str):
        """Exports the data from a QTableWidget to a CSV or Excel file."""
        if table_widget.rowCount() == 0 or table_widget.columnCount() == 0:
            QMessageBox.warning(self, "Export Error", "No data to export.")
            return

        try:
            # Get table data and headers
            rows = table_widget.rowCount()
            cols = table_widget.columnCount()
            headers = [table_widget.horizontalHeaderItem(c).text() for c in range(cols)]

            data = []
            for r in range(rows):
                row_data = []
                for c in range(cols):
                    item = table_widget.item(r, c)
                    if item is not None:
                        row_data.append(item.text())
                    else:
                        row_data.append("")
                data.append(row_data)

            # Create a pandas DataFrame
            df = pd.DataFrame(data, columns=headers)

            # Get save file name from user
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            fileName, _ = QFileDialog.getSaveFileName(self, "Save File", f"{base_filename}.csv","CSV Files (*.csv);;Excel Files (*.xlsx)", options=options)

            if fileName:
                if fileName.endswith('.csv'):
                    df.to_csv(fileName, index=False)
                elif fileName.endswith('.xlsx'):
                    df.to_excel(fileName, index=False)
                QMessageBox.information(self, "Export Successful", f"Data exported to {fileName}")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"An unexpected error occurred during export: {e}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_()) 