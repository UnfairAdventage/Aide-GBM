#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Modelo para almacenar y calcular datos personales relacionados con el gasto metabólico.
"""

from dataclasses import dataclass
from typing import List, Dict, Tuple
import numpy as np
from utils.math_tools import (
    calculate_activity_factor,
    calculate_fourier_coefficients,
    calculate_statistics,
    calculate_fourier_table,
    StatisticalAnalysis
)

@dataclass
class Person:
    """Clase que representa a una persona y sus datos metabólicos."""
    
    sex: str  # 'M' o 'F'
    weight: float  # en kg
    height: float  # en cm
    age: int  # en años
    exercise_minutes: List[float]  # lista de minutos de ejercicio por día
    
    def calculate_bmr(self) -> float:
        """
        Calcula el Gasto Metabólico Basal (TMB) usando la fórmula de Harris-Benedict.
        
        Returns:
            float: Valor del TMB en kcal/día
        """
        if self.sex.upper() == 'M':
            return 88.362 + (13.397 * self.weight) + (4.799 * self.height) - (5.677 * self.age)
        else:
            return 447.593 + (9.247 * self.weight) + (3.098 * self.height) - (4.333 * self.age)
    
    def calculate_activity_factors(self) -> List[float]:
        """
        Calcula los factores de actividad física para cada día.
        
        Returns:
            List[float]: Lista de factores de actividad física
        """
        return [calculate_activity_factor(minutes) for minutes in self.exercise_minutes]
    
    def calculate_daily_expenditure(self) -> List[float]:
        """
        Calcula el gasto bruto diario (GB) para cada día.
        
        Returns:
            List[float]: Lista de gastos brutos diarios
        """
        bmr = self.calculate_bmr()
        activity_factors = self.calculate_activity_factors()
        return [bmr * af for af in activity_factors]
    
    def calculate_fourier_coefficients(self, k: int) -> Tuple[float, float, float, float]:
        """
        Calcula los coeficientes de Fourier para una frecuencia k dada.
        Args:
            k (int): Frecuencia para el cálculo
        Returns:
            tuple: (a_k, b_k, Ak, log10_Ak) coeficientes de Fourier
        """
        return calculate_fourier_coefficients(self.calculate_daily_expenditure(), k)
    
    def get_daily_data(self) -> List[Dict[str, float]]:
        """
        Obtiene los datos diarios en formato de diccionario.
        
        Returns:
            List[Dict[str, float]]: Lista de diccionarios con datos diarios
        """
        bmr = self.calculate_bmr()
        activity_factors = self.calculate_activity_factors()
        daily_expenditure = self.calculate_daily_expenditure()
        
        return [
            {
                'day': i + 1,
                'exercise': minutes,
                'tmb': bmr,
                'af': af,
                'gb': gb
            }
            for i, (minutes, af, gb) in enumerate(zip(
                self.exercise_minutes,
                activity_factors,
                daily_expenditure
            ))
        ]
    
    def get_fourier_table(self, k: int) -> List[Dict[str, float]]:
        """
        Genera la tabla de cálculos de Fourier.
        
        Args:
            k (int): Frecuencia para el cálculo
            
        Returns:
            List[Dict[str, float]]: Tabla de cálculos de Fourier
        """
        return calculate_fourier_table(self.calculate_daily_expenditure(), k)
    
    def get_statistical_analysis(self) -> StatisticalAnalysis:
        """
        Realiza el análisis estadístico entre ejercicio y gasto bruto.
        
        Returns:
            StatisticalAnalysis: Resultados del análisis estadístico
        """
        return calculate_statistics(self.exercise_minutes, self.calculate_daily_expenditure()) 