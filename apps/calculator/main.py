import ast
import operator
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QGridLayout, QLineEdit, QPushButton
)
from PySide6.QtCore import Qt

_ALLOWED = {
    ast.Add: operator.add, ast.Sub: operator.sub,
    ast.Mult: operator.mul, ast.Div: operator.truediv,
    ast.Pow: operator.pow, ast.USub: operator.neg,
    ast.UAdd: operator.pos, ast.Mod: operator.mod
}

def safe_eval(expression):
    tree = ast.parse(expression, mode="eval")
    def visit(node):
        if isinstance(node, ast.Expression):
            return visit(node.body)
        if isinstance(node, ast.Constant) and type(node.value) in (int, float):
            return node.value
        if isinstance(node, ast.BinOp) and type(node.op) in _ALLOWED:
            left, right = visit(node.left), visit(node.right)
            if isinstance(node.op, ast.Pow) and abs(right) > 8:
                raise ValueError("Слишком большая степень")
            return _ALLOWED[type(node.op)](left, right)
        if isinstance(node, ast.UnaryOp) and type(node.op) in _ALLOWED:
            return _ALLOWED[type(node.op)](visit(node.operand))
        raise ValueError("Недопустимое выражение")
    return visit(tree)

class CalculatorWindow(QMainWindow):
    def __init__(self, desktop):
        super().__init__(desktop)
        self.setWindowTitle("Калькулятор HexOS")
        self.resize(330, 430)
        self.expression = QLineEdit()
        self.expression.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.expression.setMinimumHeight(65)
        self.expression.setPlaceholderText("0")
        self.expression.setStyleSheet("font-size: 22pt; padding: 8px;")
        central = QWidget()
        layout = QVBoxLayout(central)
        layout.addWidget(self.expression)
        grid = QGridLayout()
        buttons = [
            ("C", 0, 0), ("(", 0, 1), (")", 0, 2), ("÷", 0, 3),
            ("7", 1, 0), ("8", 1, 1), ("9", 1, 2), ("×", 1, 3),
            ("4", 2, 0), ("5", 2, 1), ("6", 2, 2), ("−", 2, 3),
            ("1", 3, 0), ("2", 3, 1), ("3", 3, 2), ("+", 3, 3),
            ("0", 4, 0), (".", 4, 1), ("⌫", 4, 2), ("=", 4, 3),
        ]
        for text, row, col in buttons:
            button = QPushButton(text)
            button.setMinimumSize(55, 55)
            button.clicked.connect(lambda checked=False, t=text: self.press(t))
            grid.addWidget(button, row, col)
        layout.addLayout(grid)
        self.setCentralWidget(central)

    def press(self, key):
        if key == "C":
            self.expression.clear()
        elif key == "⌫":
            self.expression.setText(self.expression.text()[:-1])
        elif key == "=":
            expr = self.expression.text().replace("×", "*").replace("÷", "/").replace("−", "-")
            try:
                result = safe_eval(expr)
                self.expression.setText(str(result))
            except Exception:
                self.expression.setText("Ошибка")
        else:
            self.expression.setText(self.expression.text() + key)
