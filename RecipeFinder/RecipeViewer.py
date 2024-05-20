import sys
import csv
from PyQt6.QtWidgets import QApplication, QLineEdit, QVBoxLayout, QLabel, QWidget, QMainWindow, QTableView
from PyQt6.QtCore import Qt, QAbstractTableModel, QVariant

class CSVViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('CSV Viewer')
        self.setGeometry(100, 100, 800, 600)

        self.recipe_search_input = QLineEdit(self)
        self.recipe_search_input.setPlaceholderText("Search Recipe Name...")
        self.recipe_search_input.textChanged.connect(self.filter_recipeName_data)

        self.ingredient_search_input = QLineEdit(self)
        self.ingredient_search_input.setPlaceholderText("Search Ingredients...")
        self.ingredient_search_input.textChanged.connect(self.filter_ingredient_data)

        self.cookTime_search_input = QLineEdit(self)
        self.cookTime_search_input.setPlaceholderText("Less than ...")
        self.cookTime_search_input.textChanged.connect(self.filter_cookTime_data)

        self.table_view = QTableView()
        table_container_widget = QWidget()
        search_container_widget = QWidget()

        self.setCentralWidget(table_container_widget)

        table_layout = QVBoxLayout(table_container_widget)
        search_layout = QVBoxLayout(search_container_widget)
        search_layout.addWidget(self.recipe_search_input)
        search_layout.addWidget(self.ingredient_search_input)
        search_layout.addWidget(self.cookTime_search_input)
        table_layout.addWidget(self.table_view)

        self._original_data = []  # Store original data for filtering

        self.load_data('recipes.csv')

    def load_data(self, file_path):
        try:
            with open(file_path, 'r', newline='') as file:
                reader = csv.reader(file)
                data = list(reader)
                self.header = data[0] 
                self._original_data = data[1:] 

                self.filter_recipeName_data()  # Load data on startup
                
            model = CSVModel(data)
            self.table_view.setModel(model)
            self.table_view.horizontalHeader().setVisible(False)
        except Exception as e:
            print("Error loading CSV:", e)

    def filter_recipeName_data(self):
        search_query = self.recipe_search_input.text().lower()
        filtered_data = [row for row in self._original_data if any(search_query in str(row[1]).lower() for cel in row)]
        model = CSVModel(filtered_data, self.header)
        self.table_view.setModel(model)
    
    def filter_ingredient_data(self):
        search_query = self.ingredient_search_input.text().lower()
        if search_query:
            ingredients = [ingredient.strip() for ingredient in search_query.split(",")]
            filtered_data = [row for row in self._original_data if all(ingredient.lower() in row[4].lower() for ingredient in ingredients)]
            model = CSVModel(filtered_data, self.header)
            self.table_view.setModel(model)
        else:
            print("Ingredients search query is empty.")

    def filter_cookTime_data(self):
        search_query = self.cookTime_search_input.text()
        if search_query:
            try:
              search_query = float(search_query)
              filtered_data = [row for row in self._original_data if row[3] != 'N/A' and float(row[3].split(' ')[0]) < search_query]
              model = CSVModel(filtered_data, self.header)
              self.table_view.setModel(model)
            except ValueError:
              print("Invalid input for cook time search.")

class CSVModel(QAbstractTableModel):
    def __init__(self, data, header, parent=None):
        super().__init__(parent)
        self._data = data
        self._header = header

    def rowCount(self, parent=None):
        return len(self._data)

    def columnCount(self, parent=None):
        if len(self._data) > 0:
            return len(self._data[0])
        return 0

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            row = index.row()
            col = index.column()
            return str(self._data[row][col])
        return QVariant()
    
    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return self._header[section]
        return super().headerData(section, orientation, role)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CSVViewer()
    window.show()
    sys.exit(app.exec())