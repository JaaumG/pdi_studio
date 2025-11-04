from tkinter import Tk, filedialog, messagebox
from models.model import Model
from views.view import View

class Controller:
    def __init__(self):
        self.root = Tk()
        self.root.title("PDI Studio - Sistema Interativo de Processamento de Imagens")
        self.root.geometry("1600x900")

        # Model
        self.model = Model()

        # View
        self.view = View(self.root, controller=self)

    # ========== Métodos principais ==========
    def run(self):
        self.root.mainloop()

    def open_image(self):
        path = filedialog.askopenfilename(
            title="Selecione uma imagem",
            filetypes=[("Arquivos de imagem", "*.png;*.jpg;*.jpeg;*.bmp")]
        )
        if path:
            image = self.model.load_image(path)

            # Atualiza a imagem original e a processada (lado-a-lado)
            self.view.display_original_image(self.model.to_tk_image(self.model.original))
            self.view.display_image(image)
            self.update_histogram()

            self.view.log_action(f"Imagem carregada: {path}")

    def save_image(self):
        if self.model.image is None:
            messagebox.showwarning("Aviso", "Nenhuma imagem carregada.")
            return
        path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg"), ("BMP", "*.bmp")]
        )
        if path:
            self.model.save_image(path)
            self.view.log_action(f"Imagem salva em: {path}")

    def apply_reset(self):
        if self.model.original is None:
            messagebox.showwarning("Aviso", "Nenhuma imagem carregada.")
            return

        result = self.model.reset_image()
        self.view.display_image(result)
        self.update_histogram()
        self.view.log_action("Imagem resetada para o original.")

    def apply_gray(self):
        if self.model.image is None: return
        result = self.model.convert_to_gray()
        self.view.display_image(result)
        self.update_histogram()
        self.view.log_action("Conversão para tons de cinza aplicada.")

    def apply_equalization(self):
        if self.model.image is None: return
        result = self.model.equalize_histogram()
        self.view.display_image(result)
        self.update_histogram()
        self.view.log_action("Equalização de histograma aplicada.")

    def apply_brightness_contrast(self, brightness, contrast):
        if self.model.image is None: return
        result = self.model.apply_brightness_contrast(brightness, contrast)
        self.view.display_image(result)
        self.update_histogram()
        self.view.log_action(f"Brilho ({brightness}) e Contraste ({contrast:.1f}) aplicados.")

    def apply_global_threshold(self, threshold_value):
        if self.model.image is None: return
        result = self.model.apply_global_threshold(threshold_value)
        self.view.display_image(result)
        self.update_histogram()
        self.view.log_action(f"Limiar global ({threshold_value}) aplicado.")

    def apply_otsu_threshold(self):
        if self.model.image is None: return
        result = self.model.apply_otsu_threshold()
        self.view.display_image(result)
        self.update_histogram()
        self.view.log_action("Limiarização (Otsu) aplicada.")

    def show_histogram(self):
        if self.model.image is None:
            messagebox.showwarning("Aviso", "Nenhuma imagem carregada.")
            return
        hist = self.model.compute_histogram()
        if hist is not None:
            self.view.show_histogram(hist)
            self.view.log_action("Histograma exibido.")

    # Helper para atualizar histograma automaticamente
    def update_histogram(self):
        if self.model.image is None:
            return
        hist = self.model.compute_histogram()
        if hist is not None:
            self.view.show_histogram(hist)