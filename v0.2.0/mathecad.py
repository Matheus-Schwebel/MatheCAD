import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QGraphicsView, QTextEdit, QPushButton, QVBoxLayout, QWidget,QGraphicsRectItem, QMessageBox
from PyQt5.QtGui import QPen, QBrush, QColor, QPainter, QPainterPath
from PyQt5.QtCore import Qt, QRectF
class CADGraphicsView(QGraphicsView):
    def __init__(self, scene):
        super().__init__(scene)
        self.setRenderHint(QPainter.Antialiasing)
        self.zone_colors = {
            "residential": "blue",
            "commercial": "yellow",
            "park": "green",
            "industrial": "gray",
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
        self.setWindowTitle("MatheCAD 0.2")
        self.setGeometry(100, 100, 1000, 700)

        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        
        self.editor = QTextEdit()
        self.run_button = QPushButton("Run Code")
        self.run_button.clicked.connect(self.run_code)

        # Definir as cores dos zoneamentos
        self.zone_colors = {
            "residential": "lightblue",
            "commercial": "yellow",
            "park": "green",
            "industrial": "gray"
        }

        layout = QVBoxLayout()
        layout.addWidget(self.view)
        layout.addWidget(self.editor)
        layout.addWidget(self.run_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

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
            exec(code, {}, local_scope)
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
    def create_roundabout(self, x, y, radius):
        msg = QMessageBox()
        msg.setWindowTitle("Aviso: Função Obsoleta")
        msg.setText("A Função <b style='color: red'><i>Quadra().create_roundabout()</i></b> está obsoleta e será substituída por <b style='color: green'><i>draw_roundabout()</i></b> na versão 0.3.")
        msg.setIcon(QMessageBox.Warning)  # Ícone de aviso
        msg.exec_()

        # Criar a rotatória
        return CADGraphicsView(self.scene).draw_roundabout(x, y, radius)
        

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
