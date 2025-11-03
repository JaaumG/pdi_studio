from views.menu_bar import MenuBar
from views.image_panel import ImagePanel
from views.control_panel import ControlPanel

class View:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller

        # Menu superior
        self.menu = MenuBar(self.root, controller)
        self.root.config(menu=self.menu.menubar)

        # Painéis
        # Passa a instância do controller para o control_panel
        self.control_panel = ControlPanel(self.root, controller)
        self.image_panel = ImagePanel(self.root)

        # Prioriza empacotar o painel de controle primeiro para reservar espaço do log
        self.control_panel.frame.pack(side="right", fill="y")
        self.image_panel.frame.pack(side="left", fill="both", expand=True)

    def display_original_image(self, image):
        self.image_panel.show_original_image(image)

    def display_image(self, image):
        self.image_panel.show_processed_image(image)

    def log_action(self, text):
        self.control_panel.add_log(text)
