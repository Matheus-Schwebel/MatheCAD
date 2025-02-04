import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QGraphicsView, QTextEdit
from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QWidget,QMessageBox, QAction, QFileDialog
from PyQt5.QtGui import QPen, QBrush, QColor, QPainter, QPainterPath, QImage
from PyQt5.QtCore import Qt, QRectF
import re

def interpret_commands(code, local_scope):
    lines = code.split("\n")
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):  # Ignorar linhas vazias e comentários
            continue
        try:
            # Verificar atribuições de Quadra (ex: quadra3 = Quadra(...))
            match = re.match(r"(\w+)\s*=\s*Quadra\(([^)]+)\)", line)
            if match:
                var_name = match.group(1)  # Nome da variável (ex: quadra3)
                params = match.group(2).split(",")  # Parâmetros da função
                x, y, width, height = map(int, params[:4])
                quadra = Quadra(x, y, width, height, local_scope["scene"], local_scope["zone_colors"])
                local_scope[var_name] = quadra  # Armazenando a instância no escopo
                quadra.desenha_quadra()
                continue

            # Verificar atribuições de atributos (ex: quadra3.zone = "commercial")
            match = re.match(r"(\w+)\.(\w+)\s*=\s*\"(.+)\"", line)
            if match:
                obj_name, attr, value = match.groups()
                if obj_name in local_scope:
                    setattr(local_scope[obj_name], attr, value)

            # Verificar chamadas de métodos (ex: quadra3.create_terrains(num_plots=4, margin=10))
            match = re.match(r"(\w+)\.(\w+)\((.*)\)", line)
            if match:
                obj_name, method_name, params = match.groups()
                if obj_name in local_scope:
                    obj = local_scope[obj_name]
                    method = getattr(obj, method_name, None)
                    if method:
                        param_dict = {}
                        for param in params.split(","):
                            key_value = param.split("=")
                            if len(key_value) == 2:
                                key, value = key_value
                                param_dict[key.strip()] = int(value.strip())
                        method(**param_dict)

            # Desenhar linha independente
            if "draw_independent_line(" in line:
                parts = line.replace("draw_independent_line(", "").replace(")", "").split(",")
                x, y, length, width = map(int, parts[:4])
                draw_independent_line(x, y, length, width, local_scope["scene"])

            # Desenhar rotatória
            elif "draw_roundabout(" in line:
                parts = line.replace("draw_roundabout(", "").replace(")", "").split(",")
                x, y, radius = map(int, parts[:3])
                draw_roundabout(x, y, radius, local_scope["scene"])

        except Exception as e:
            print(f"Erro ao interpretar comando: {line} - {e}")


class CADGraphicsView(QGraphicsView):
    def __init__(self, scene):
        super().__init__(scene)
        self.setRenderHint(QPainter.Antialiasing)
        self.zone_colors = {
            "residencial": "blue",
            "residential": "blue",
            "commercial": "yellow",
            "comercial": "yellow",
            "park": "green",
            "parque": "green",
            "industrial": "gray",
            "APP" : "forestgreen",
            "services" : "lightseagreen"
            # Adicione outras zonas e suas cores conforme necessário
        }

    def draw_terrain(self, x, y, width, height, zone="residential"):
        # Obter a cor associada ao zoneamento
        color = self.zone_colors.get(zone, "blue")  # Padrão para azul se a zona não for encontrada
        brush = QBrush(QColor(color))
        rect = self.scene().addRect(QRectF(x, y, width, height), QPen(Qt.black, 2), brush)  # Contorno visível
        # Exibir o nome do zoneamento no centro do terreno
        text_item = self.scene().addText(zone)
        text_item.setPos(x + width / 4, y + height / 4)
        return rect

    def draw_rounded_rectangle(self, x, y, width, height, radius=20):
        # Criar um retângulo com cantos arredondados usando QGraphicsRectItem
        rect_item = self.scene().addRect(QRectF(x, y, width, height), QPen(Qt.black, 3))
        rect_item.setBrush(QBrush(QColor("lightgray")))
        rect_item.setRoundRect(radius, radius)
        return rect_item

    def draw_roundabout(self, x, y, radius):
        # Desenhar uma rotatória redonda
        brush = QBrush(QColor("green"))
        ellipse = self.scene().addEllipse(QRectF(x - radius, y - radius, radius * 2, radius * 2), QPen(Qt.black, 3), brush)
        return ellipse

    def draw_independent_line(self, x, y, length, width):
        # Criar uma linha independente (canteiro ou rua)
        line = self.scene().addRect(QRectF(x, y, length, width), QPen(Qt.black, 2), QBrush(QColor("darkgray")))
        return line

class CADWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("City Planner")
        self.setGeometry(100, 100, 1000, 700)

        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        
        self.editor = QTextEdit()
        self.run_button = QPushButton("Run Code")
        self.run_button.clicked.connect(self.run_code)

        # Definir as cores dos zoneamentos
        self.zone_colors = {
            "residencial": "blue",
            "residential": "blue",
            "commercial": "yellow",
            "comercial": "yellow",
            "park": "green",
            "parque": "green",
            "industrial": "gray",
            "APP" : "forestgreen",
            "services" : "lightseagreen"
            # Adicione outras zonas e suas cores conforme necessário
        }

        layout = QVBoxLayout()
        layout.addWidget(self.view)
        layout.addWidget(self.editor)
        layout.addWidget(self.run_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.create_menu()

    def create_menu(self):
        """Cria a barra de menu com opções."""
        menubar = self.menuBar()

        # Menu Arquivo
        file_menu = menubar.addMenu("Arquivo")

        open_action = QAction("Abrir", self)
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)

         # Ação de Sair
        exit_action = QAction("Salvar", self)
        exit_action.triggered.connect(self.save_file)
        file_menu.addAction(exit_action)

        # Ação de Sair
        exit_action = QAction("Sair", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        save_image_action = QAction("Salvar como Imagem", self)
        save_image_action.triggered.connect(self.save_as_image)
        file_menu.addAction(save_image_action)

        # Menu Ajuda
        help_menu = menubar.addMenu("Ajuda")
        about_action = QAction("Sobre", self)
        about_action.triggered.connect(self.show_help)
        help_menu.addAction(about_action)

    def save_as_image(self):
    # Obter o retângulo da cena inteira (não só a área visível)
        scene_rect = self.scene.sceneRect()

    # Criar uma imagem com o tamanho total da cena
        image = QImage(scene_rect.size().toSize(), QImage.Format_ARGB32_Premultiplied)

    # Cria um QPainter para renderizar a cena na imagem
        painter = QPainter(image)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)
    
    # Renderiza toda a cena no QImage com as dimensões totais
        self.scene.render(painter, source=scene_rect, target=QRectF(0, 0, scene_rect.width(), scene_rect.height()))
        painter.end()

    # Abrir um diálogo para salvar a imagem
        file_name, _ = QFileDialog.getSaveFileName(self, "Salvar Imagem", "", "Imagem (*.png *.jpg *.bmp)")
        if file_name:
            image.save(file_name)
    def save_file(self):
        """Abre um diálogo para salvar o conteúdo do editor em um arquivo."""
        file_name, _ = QFileDialog.getSaveFileName(self, "Salvar Arquivo", "", "Texto (*.txt);;Todos os Arquivos (*)")
        if file_name:
            with open(file_name, "w") as file:
                file.write(self.editor.toPlainText())

    def open_file(self):
        """Abre um diálogo para selecionar e abrir um arquivo no editor."""
        file_name, _ = QFileDialog.getOpenFileName(self, "Abrir Arquivo", "", "Texto (*.txt);;Todos os Arquivos (*)")
        if file_name:
            with open(file_name, "r") as file:
                self.editor.setPlainText(file.read())

    def show_help(self):
        # Exibir o QMessageBox com as opções "Sair" e "Próximo"
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Help")
        msg.setText("""Exemplo de código para zoneamento e rotatórias:\n\n
                    # Criando a primeira quadra com zoneamento residencial
quadra1 = Quadra(100, 100, 400, 200, scene, zone_colors)
quadra1.zone = "residential"  # Zoneamento residencial
quadra1.desenha_quadra()
quadra1.create_terrains()

draw_roundabout(525, 75, 12)
#quadrainter.desenha_quadra()
#quadrainter.create_terrains()
                    
                    """)
        msg.setStandardButtons(QMessageBox.Close | QMessageBox.Ok)
        msg.setDefaultButton(QMessageBox.Ok)

        # Adicionar as opções "Sair" e "Próximo"
        reply = msg.exec_()
        if reply == QMessageBox.Ok:
            self.show_example_code()
        elif reply == QMessageBox.Close:
            self.close()

    def show_example_code(self):
        # Exibir exemplo de código adicional
        example_msg = QMessageBox(self)
        example_msg.setIcon(QMessageBox.Information)
        example_msg.setWindowTitle("Next Example")
        example_msg.setText("Exemplo de código para criar terrenos:\n\n"
                            "quadra3.create_terrains(num_plots=4, margin=10)")
        example_msg.setStandardButtons(QMessageBox.Ok)
        example_msg.exec_()

    def run_code(self):
        code = self.editor.toPlainText()
        self.scene.clear()

        # Passando as cores dos zoneamentos para o código inserido
        local_scope = {
            "Quadra": Quadra,
            "scene": self.scene,
            "zone_colors": self.zone_colors,
            "draw_independent_line": draw_independent_line,
            "draw_roundabout": draw_roundabout
        }
        try:
            interpret_commands(code, local_scope)  # Run the code with the current scope
        except Exception as e:
            print(f"Erro: {e}")

class Quadra:
    def __init__(self, x, y, width, height, scene, zone_colors):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.scene = scene
        self.zone_colors = zone_colors
        self.zone = "residential"  # Zoneamento inicial

    def desenha_quadra(self):
        # Criar um caminho com cantos arredondados
        path = QPainterPath()
        path.setFillRule(Qt.WindingFill)
        path.addRoundedRect(QRectF(self.x, self.y, self.width, self.height), 20, 20)  # 20 é o raio do arredondamento
        
        # Usar o dicionário de cores para o zoneamento
        zone_color = self.zone_colors.get(self.zone, "blue")  # Buscar a cor do zoneamento
        rect_item = self.scene.addPath(path, QPen(Qt.black, 3))  # Usando QPen para contorno
        rect_item.setBrush(QBrush(QColor(zone_color)))  # Preenchendo com a cor do zoneamento
        
        # Exibir o nome do zoneamento no centro da quadra
        text_item = self.scene.addText(self.zone)
        text_item.setPos(self.x + self.width / 4, self.y + self.height / 4)  # Posicionar o texto no centro
        return rect_item
    
    def create_terrains(self, num_plots=4, margin=0):
        plot_width = (self.width - (num_plots - 1) * margin) / num_plots  # Ajuste na largura para garantir que os terrenos não se sobreponham
        plot_height = self.height / 2  # Dividir a altura da quadra em duas partes
        
        # Criar os terrenos para a parte de cima (4 terrenos)
        for i in range(num_plots):
            self.scene.addRect(QRectF(self.x + i * (plot_width + margin), self.y, plot_width, plot_height), QPen(Qt.black, 2))
        
        # Criar os terrenos para a parte de baixo (4 terrenos)
        for i in range(num_plots):
            self.scene.addRect(QRectF(self.x + i * (plot_width + margin), self.y + plot_height, plot_width, plot_height), QPen(Qt.black, 2))
    # def create_roundabout(self, x, y, radius):
    #     return draw_roundabout(x, y, radius, self.scene)

# Função para criar uma linha independente (avenida ou canteiro)
def draw_independent_line(x, y, width, height, scene):
    line = scene.addRect(QRectF(x, y, width, height))
    line.setBrush(QBrush(QColor("gray")))  # Linha de cor cinza
    line.setPen(QPen(Qt.NoPen))  # Sem borda
    return line

# Função para desenhar a rotatória
def draw_roundabout(x, y, radius, scene):
    brush = QBrush(QColor("green"))
    ellipse = scene.addEllipse(QRectF(x - radius, y - radius, radius * 2, radius * 2), QPen(Qt.black, 3), brush)
    return ellipse

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CADWindow()
    window.show()
    sys.exit(app.exec_())
