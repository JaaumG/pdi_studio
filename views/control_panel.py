import tkinter as tk
from tkinter import scrolledtext, Scale, Frame, Label, Button
from tkinter import font as tkfont
from tkinter import ttk
from views.histogram_canvas import HistogramCanvas

class ControlPanel:
    def __init__(self, root, controller):
        self.controller = controller

        # Cores principais
        bg_main = "#1e1e1e"
        bg_panel = "#252526"
        fg_text = "#f3f3f3"
        accent = "#3fa9f5"

        self.frame = tk.Frame(root, bg=bg_panel, width=320)  # Largura melhor à leitura
        self.frame.pack_propagate(False)

        # Título do painel
        title_font = tkfont.Font(size=12, weight="bold")
        subtitle_font = tkfont.Font(size=9)
        Label(self.frame, text="PDI Studio", fg=fg_text, bg=bg_panel, font=title_font).pack(pady=(12, 0))
        Label(self.frame, text="Ferramentas", fg="#c9c9c9", bg=bg_panel, font=subtitle_font).pack(pady=(0, 6))

        # ttk styling (dark, modern)
        style = ttk.Style()
        try:
            style.theme_use('clam')
        except Exception:
            pass
        style.configure('Accent.TButton', background=accent, foreground='#000', padding=(8, 6))
        style.map('Accent.TButton', background=[('active', '#2f90d6'), ('pressed', '#277ab6')])
        style.configure('Dark.Horizontal.TScale', troughcolor='#2d2d2d', background='#3a3a3a')

        controls_frame = Frame(self.frame, bg=bg_panel)
        controls_frame.pack(pady=6, padx=12, fill="x")

        # Brilho
        brightness_row = Frame(controls_frame, bg=bg_panel)
        brightness_row.pack(fill='x')
        Label(brightness_row, text="Brilho", fg=fg_text, bg=bg_panel).pack(side='left')
        self.brightness_value = tk.IntVar(value=0)
        Label(brightness_row, textvariable=self.brightness_value, fg="#bfbfbf", bg=bg_panel).pack(side='right')

        self.brightness_var = tk.DoubleVar(value=0)
        self.brightness_slider = ttk.Scale(
            controls_frame,
            from_=-127,
            to=127,
            orient=tk.HORIZONTAL,
            variable=self.brightness_var,
            command=lambda v: self._on_brightness_change(v),
            style='Dark.Horizontal.TScale',
        )
        self.brightness_slider.pack(fill="x", pady=4)

        # Contraste
        contrast_row = Frame(controls_frame, bg=bg_panel)
        contrast_row.pack(fill='x', pady=(8, 0))
        Label(contrast_row, text="Contraste (x10)", fg=fg_text, bg=bg_panel).pack(side='left')
        self.contrast_value = tk.IntVar(value=10)
        Label(contrast_row, textvariable=self.contrast_value, fg="#bfbfbf", bg=bg_panel).pack(side='right')

        self.contrast_var = tk.DoubleVar(value=10)
        self.contrast_slider = ttk.Scale(
            controls_frame,
            from_=1,
            to=30,
            orient=tk.HORIZONTAL,
            variable=self.contrast_var,
            command=lambda v: self._on_contrast_change(v),
            style='Dark.Horizontal.TScale',
        )
        self.contrast_slider.pack(fill="x", pady=4)

        ttk.Button(
            controls_frame,
            text="Aplicar Brilho/Contraste",
            command=self.on_apply_brightness_contrast,
            style='Accent.TButton',
        ).pack(pady=(6, 10), fill="x")

        # Limiar Global
        threshold_row = Frame(controls_frame, bg=bg_panel)
        threshold_row.pack(fill='x')
        Label(threshold_row, text="Limiar Global", fg=fg_text, bg=bg_panel).pack(side='left')
        self.threshold_value = tk.IntVar(value=127)
        Label(threshold_row, textvariable=self.threshold_value, fg="#bfbfbf", bg=bg_panel).pack(side='right')

        self.threshold_var = tk.DoubleVar(value=127)
        self.threshold_slider = ttk.Scale(
            controls_frame,
            from_=0,
            to=255,
            orient=tk.HORIZONTAL,
            variable=self.threshold_var,
            command=lambda v: self._on_threshold_change(v),
            style='Dark.Horizontal.TScale',
        )
        self.threshold_slider.pack(fill="x", pady=4)

        ttk.Button(
            controls_frame,
            text="Aplicar Limiar Global",
            command=self.on_apply_threshold,
            style='Accent.TButton',
        ).pack(pady=(6, 10), fill="x")

        # Área do histograma
        self.hist_widget = HistogramCanvas(self.frame)
        self.hist_widget.pack(padx=10, pady=5, fill="x")

        Frame(self.frame, height=1, bg="#3a3a3a").pack(fill="x", padx=10, pady=10)

        tk.Label(self.frame, text="Histórico de Ações", fg=fg_text, bg=bg_panel).pack(pady=(0, 6))
        self.log_area = scrolledtext.ScrolledText(
            self.frame, width=35, height=20, bg=bg_main, fg=fg_text, insertbackground=fg_text
        )  # Altura ajustada
        self.log_area.pack(padx=10, pady=10, fill="both", expand=True)

    def on_apply_brightness_contrast(self):
        brightness = self.brightness_slider.get()
        contrast = self.contrast_slider.get() / 10.0

        self.controller.apply_brightness_contrast(brightness, contrast)

    def on_apply_threshold(self):
        threshold_value = self.threshold_slider.get()
        self.controller.apply_global_threshold(threshold_value)

    def add_log(self, text):
        self.log_area.insert(tk.END, f"> {text}\n")
        self.log_area.see(tk.END)

    def draw_histogram(self, hist_data: dict):
        if hasattr(self, 'hist_widget') and self.hist_widget:
            self.hist_widget.draw_histogram(hist_data)

    # Handlers de sliders para atualizar valores de texto
    def _on_brightness_change(self, val):
        try:
            self.brightness_value.set(int(float(val)))
        except Exception:
            pass

    def _on_contrast_change(self, val):
        try:
            self.contrast_value.set(int(float(val)))
        except Exception:
            pass

    def _on_threshold_change(self, val):
        try:
            self.threshold_value.set(int(float(val)))
        except Exception:
            pass
