import sys

from rectpack import newPacker
from rectpack.geometry import Rectangle

from icecream import ic


from PySide6.QtWidgets import (
    QApplication,
    QGraphicsView,
    QGraphicsScene,
    QGraphicsRectItem,
)
from PySide6.QtGui import Qt


class RectsViewer(QGraphicsView):
    def __init__(self, width: int, height: int):
        super().__init__()

        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.setSceneRect(0, 0, width, height)

    def draw_rectangle(
        self,
        x: float,
        y: float,
        width: float,
        height: float,
        color: Qt.GlobalColor = Qt.red,
        line_width: int = 2,
    ) -> None:
        rect = QGraphicsRectItem(x, y, width, height)
        pen = rect.pen()
        pen.setColor(color)
        pen.setWidth(line_width)
        rect.setPen(pen)
        self.scene.addItem(rect)


def main() -> None:
    app = QApplication(sys.argv)

    bin_width = 914
    bin_height = 1700

    rectangles = [(210, 297) for _ in range(10)]
    
    packer = newPacker(rotation=True)

    for r in rectangles:
        packer.add_rect(*r)
    
    packer.add_bin(bin_width, bin_height, count=float("inf"))
    packer.pack()

    windows = []

    for index, b in enumerate(packer.bin_list()):
        def sums_w(rect: Rectangle) -> int:
            return rect.x + rect.width

        def sums_h(rect: Rectangle) -> int:
            return rect.y + rect.height

        viewer = RectsViewer(*b)
        rects = packer[index]
        for r in rects:
            viewer.draw_rectangle(r.x, r.y, r.width, r.height)

        max_w = max(list(map(sums_w, [r for r in rects])))
        max_h = max(list(map(sums_h, [r for r in rects])))
        viewer.draw_rectangle(0, 0, max_w, max_h, color=Qt.blue)

        windows.append(viewer)
    
    for w in windows:
        w.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
