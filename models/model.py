import cv2
from PIL import Image, ImageTk
import numpy as np

class Model:
    def __init__(self):
        self.image = None
        self.original = None

    def load_image(self, path):
        self.image = cv2.imread(path)
        self.original = self.image.copy()
        return self.to_tk_image(self.image)

    def save_image(self, path):
        if self.image is not None:
            cv2.imwrite(path, self.image)

    def reset_image(self):
        if self.original is not None:
            self.image = self.original.copy()
            return self.to_tk_image(self.image)

    # ========== Operações de PDI ==========
    def convert_to_gray(self):
        if self.image is None:
            return None

        if len(self.image.shape) == 2:
            self.image = cv2.cvtColor(self.image, cv2.COLOR_GRAY2BGR)

        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        self.image = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
        return self.to_tk_image(self.image)

    def equalize_histogram(self):
        if self.image is None:
            return None

        if len(self.image.shape) == 2:
            self.image = cv2.cvtColor(self.image, cv2.COLOR_GRAY2BGR)

        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        equalized = cv2.equalizeHist(gray)
        self.image = cv2.cvtColor(equalized, cv2.COLOR_GRAY2BGR)
        return self.to_tk_image(self.image)

    def apply_brightness_contrast(self, brightness, contrast):
        if self.image is None:
            return None
        self.image = cv2.convertScaleAbs(self.image, alpha=contrast, beta=brightness)
        return self.to_tk_image(self.image)

    def apply_global_threshold(self, threshold_value):
        if self.image is None:
            return None

        if len(self.image.shape) == 2:
            self.image = cv2.cvtColor(self.image, cv2.COLOR_GRAY2BGR)

        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, threshold_value, 255, cv2.THRESH_BINARY)
        self.image = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)
        return self.to_tk_image(self.image)

    def apply_otsu_threshold(self):
        if self.image is None:
            return None

        if len(self.image.shape) == 2:
            self.image = cv2.cvtColor(self.image, cv2.COLOR_GRAY2BGR)

        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        self.image = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)
        return self.to_tk_image(self.image)

    # ========== Conversão ==========
    def to_tk_image(self, cv_image):
        rgb = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(rgb)
        return ImageTk.PhotoImage(img)

    # ========== Histograma ==========
    def compute_histogram(self):
        """
        Retorna os histogramas da imagem atual.

        Saída:
          - Se imagem colorida: dict com chaves 'b', 'g', 'r', cada uma um array de 256 bins
          - Se imagem em escala de cinza: dict com chave 'gray'
        """
        if self.image is None:
            return None

        # Garante que temos BGR para cálculo de cinza quando necessário
        if len(self.image.shape) == 2:
            gray = self.image
        else:
            gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

        # Histograma em escala de cinza
        hist_gray = cv2.calcHist([gray], [0], None, [256], [0, 256]).flatten()

        if len(self.image.shape) == 2:
            return {"gray": hist_gray}

        # Histograma por canal (B, G, R)
        chans = cv2.split(self.image)
        hist_b = cv2.calcHist([chans[0]], [0], None, [256], [0, 256]).flatten()
        hist_g = cv2.calcHist([chans[1]], [0], None, [256], [0, 256]).flatten()
        hist_r = cv2.calcHist([chans[2]], [0], None, [256], [0, 256]).flatten()

        return {"b": hist_b, "g": hist_g, "r": hist_r, "gray": hist_gray}
