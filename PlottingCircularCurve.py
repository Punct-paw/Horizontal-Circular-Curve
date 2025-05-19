import sys
import numpy as np
import matplotlib.pyplot as plt
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QGridLayout, QMessageBox
)
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from dataclasses import dataclass
import CircularCurve  # Import the above module

@dataclass
class Point:
    x: float
    y: float

class CircularCurveApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Horizontal Circular Curve Diagram")
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        form_layout = QGridLayout()
        self.inputs = {}

        labels = ['Back Bearing (deg)', 'Ahead Bearing (deg)', 'PI Easting (x in ft)', 'PI Northing (y in ft)', 'Degree of Curve (deg)']
        keys = ['BB', 'AB', 'PI_x', 'PI_y', 'D']

        for i, (label, key) in enumerate(zip(labels, keys)):
            form_layout.addWidget(QLabel(label), i, 0)
            self.inputs[key] = QLineEdit()
            form_layout.addWidget(self.inputs[key], i, 1)
        layout.addLayout(form_layout)

        button_layout = QHBoxLayout()
        self.calc_btn = QPushButton("Calculate and Plot")
        self.calc_btn.clicked.connect(self.run_calculation)
        button_layout.addWidget(self.calc_btn)
        layout.addLayout(button_layout)

        self.canvas = FigureCanvas(plt.figure(figsize=(16, 7)))
        layout.addWidget(self.canvas)

        self.result_label = QLabel("")
        layout.addWidget(self.result_label)
        self.setLayout(layout)

    def run_calculation(self):
        try:
            BB = float(self.inputs['BB'].text())
            AB = float(self.inputs['AB'].text())
            PI_x = float(self.inputs['PI_x'].text())
            PI_y = float(self.inputs['PI_y'].text())
            D = float(self.inputs['D'].text())

            PI = Point(PI_x, PI_y)
            
            #Calculate Curve Parameters
            Delta, R, L, LC, T, E, M, BBAzimuth, ABAzimuth, PC, PT = CircularCurve.Horizontal_Circular_Curve.circular_curve(BB, AB, PI, D)
            Center_Point,Direction=CircularCurve.Horizontal_Circular_Curve.Find_center_of_circle(PC,PT,BB,AB,R)

            #Generate correct arc points based on center-to-PC/PT angles
            arc_points=CircularCurve.Horizontal_Circular_Curve.Generate_arc_points(Center_Point,PC,PT,R,Direction)
            summary = (
                f"Delta: {Delta:.4f}°\n"
                f"Radius: {R:.4f} ft\n"
                f"Length of Curve (L): {L:.4f} ft\n"
                f"Long Chord (LC): {LC:.4f} ft\n"
                f"Tangent (T): {T:.4f} ft\n"
                f"External Distance (E): {E:.4f} ft\n"
                f"Middle Ordinate (M): {M:.4f} ft\n"
                f"PC: ({PC.x:.2f}, {PC.y:.2f})\n"
                f"PT: ({PT.x:.2f}, {PT.y:.2f})"
            )
            self.result_label.setText(summary)
           
            #Plotting
            self.canvas.figure.clear()
            ax = self.canvas.figure.add_subplot(111)

            #Plot the arc
            x_vals = [p.x for p in arc_points]
            y_vals = [p.y for p in arc_points]
            ax.plot(x_vals, y_vals, 'r-', label="Horizontal Curve")

            # Plot key points
            ax.plot([PI.x], [PI.y], 'ko', label='PI')
            ax.plot([PC.x], [PC.y], 'go', label='PC')
            ax.plot([PT.x], [PT.y], 'bo', label='PT')
            ax.plot([Center_Point.x], [Center_Point.y], 'mo', label='Center')

            # Annotate points
            ax.annotate('PI', (PI.x, PI.y), textcoords="offset points", xytext=(5,5), ha='left')
            ax.annotate('PC', (PC.x, PC.y), textcoords="offset points", xytext=(5,5), ha='left')
            ax.annotate('PT', (PT.x, PT.y), textcoords="offset points", xytext=(5,5), ha='left')
            ax.annotate('Center', (Center_Point.x, Center_Point.y), textcoords="offset points", xytext=(5,5), ha='left')

            # Draw tangents
            ax.plot([PC.x, PI.x], [PC.y, PI.y], 'g--', label='Back Tangent')
            ax.plot([PT.x, PI.x], [PT.y, PI.y], 'b--', label='Ahead Tangent')

            # Radius lines
            ax.plot([Center_Point.x, PC.x], [Center_Point.y, PC.y], 'm:', label='Radius')
            ax.plot([Center_Point.x, PT.x], [Center_Point.y, PT.y], 'm:')

            # Display values as annotations
            ax.text(0.01, 0.95, f"R = {R:.2f} ft", transform=ax.transAxes, fontsize=10, verticalalignment='top')
            ax.text(0.01, 0.90, f"T = {T:.2f} ft", transform=ax.transAxes, fontsize=10, verticalalignment='top')
            ax.text(0.01, 0.85, f"L = {L:.2f} ft", transform=ax.transAxes, fontsize=10, verticalalignment='top')
            ax.text(0.01, 0.80, f"LC = {LC:.2f} ft", transform=ax.transAxes, fontsize=10, verticalalignment='top')
            ax.text(0.01, 0.75, f"E = {E:.2f} ft", transform=ax.transAxes, fontsize=10, verticalalignment='top')
            ax.text(0.01, 0.70, f"M = {M:.2f} ft", transform=ax.transAxes, fontsize=10, verticalalignment='top')
            ax.text(0.01, 0.65, f"Δ = {Delta:.2f}°", transform=ax.transAxes, fontsize=10, verticalalignment='top')
            ax.text(0.01, 0.60, f"Direction = {Direction}", transform=ax.transAxes, fontsize=10, verticalalignment='top')
            
            
            

           #Final Formatting

            ax.legend()
            ax.set_title("Horizontal Circular Curve Layout")
            ax.set_aspect('equal')
            ax.margins(0.2)  # Add 20% margin around the curve
            ax.autoscale_view()
            self.canvas.draw()

        except ValueError:
            QMessageBox.critical(self, "Input Error", "Please enter valid numeric inputs.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CircularCurveApp()
    window.show()
    sys.exit(app.exec())
