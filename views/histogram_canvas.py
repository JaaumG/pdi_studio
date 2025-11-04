import tkinter as tk
from tkinter import Canvas, Frame, Label
import numpy as np


class HistogramCanvas:
	"""Widget simples para exibir histogramas (grayscale e BGR)."""

	def __init__(self, root, width=280, height=180, bg="#111"):
		self.frame = Frame(root, bg="#222")
		Label(self.frame, text="Histograma", bg="#222", fg="white").pack(pady=2)

		self.canvas = Canvas(self.frame, width=width, height=height, bg=bg, highlightthickness=1, highlightbackground="#444")
		self.canvas.pack(fill="x", padx=5, pady=5)

		self.width = width
		self.height = height

	def pack(self, **kwargs):
		self.frame.pack(**kwargs)

	def clear(self):
		self.canvas.delete("all")

	def draw_histogram(self, hist_data: dict):
		"""
		hist_data: dict com arrays de 256 bins. Pode conter chaves 'gray', 'b', 'g', 'r'.
		"""
		self.clear()
		if not hist_data:
			return

		# Normaliza para caber no canvas
		def norm(hist):
			hist = np.asarray(hist, dtype=float)
			m = hist.max() if hist.size else 1.0
			return (hist / (m if m > 0 else 1.0)) * (self.height - 10)

		# Background grid simples
		self.canvas.create_rectangle(0, 0, self.width, self.height, outline="#444")
		for i in range(1, 4):
			y = i * (self.height / 4)
			self.canvas.create_line(0, y, self.width, y, fill="#222")

		# Dimensão por bin (assume 256)
		bins = 256
		step = self.width / bins

		# Decide quais curvas desenhar
		curves = []
		if 'gray' in hist_data and ('b' not in hist_data and 'g' not in hist_data and 'r' not in hist_data):
			curves.append(('gray', '#aaaaaa'))
		else:
			for key, color in [('b', '#3fa9f5'), ('g', '#7bd389'), ('r', '#ff6b6b')]:
				if key in hist_data:
					curves.append((key, color))

		for key, color in curves:
			hist = norm(hist_data[key])
			# desenha como linhas verticais (estilo barras finas)
			for i in range(bins):
				x0 = int(i * step)
				x1 = int((i + 1) * step)
				y = self.height - hist[i]
				self.canvas.create_line(x0, self.height, x0, y, fill=color)
