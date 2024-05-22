import sys
import csv
from PyQt6.QtWidgets import QApplication, QLineEdit, QVBoxLayout, QHBoxLayout, QLabel, QWidget, QMainWindow, QTableView, QPushButton, QDialog, QFormLayout, QSizePolicy
from PyQt6.QtCore import Qt, QAbstractTableModel, QVariant, QModelIndex
from PyQt6.QtGui import QDesktopServices, QColor
from PyQt6.QtCore import QUrl

class CSVViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Recipe Viewer')
        self.setGeometry(100, 100, 800, 600)

        self.setStyleSheet("background-color: #a0c0ff; color: #333;")

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
        self.table_view.clicked.connect(self.open_row_details)
        self.table_view.setTextElideMode(Qt.TextElideMode.ElideNone)

        self.recipe_search_input.setStyleSheet("background-color: #e0e0e0;")
        self.ingredient_search_input.setStyleSheet("background-color: #e0e0e0;")
        self.cookTime_search_input.setStyleSheet("background-color: #e0e0e0;")
        self.table_view.horizontalHeader().setStyleSheet("background-color: #e0e0e0;")
        self.table_view.verticalHeader().setStyleSheet("background-color: #e0e0e0;")
        self.table_view.setStyleSheet("QTableView { background-color: #e0e0e0; alternate-background-color: #f9f9f9; gridline-color: #a0c0ff; }"
                                      "QTableView::item:selected { background-color: #a0c0ff; }")
        
        # table_container_widget = QWidget()
        # search_container_widget = QWidget()
        container_widget = QWidget()

        self.setCentralWidget(container_widget)

        main_layout = QVBoxLayout(container_widget)
        # table_layout = QVBoxLayout(table_container_widget)
        search_layout = QHBoxLayout()
        search_layout.addWidget(QLabel("Recipe Name: "))
        search_layout.addWidget(self.recipe_search_input)
        search_layout.addWidget(QLabel("Ingredients: "))
        search_layout.addWidget(self.ingredient_search_input)
        search_layout.addWidget(QLabel("Cook Time: "))
        search_layout.addWidget(self.cookTime_search_input)
        # table_layout.addWidget(self.table_view)

        main_layout.addLayout(search_layout)
        main_layout.addWidget(self.table_view)
        # main_layout.setStretchFactor(self.table_view, 1)


        self._original_data = []  # Store original data for filtering
        self.filtered_data = []

        self.load_data('RecipeFinder/recipes.csv')

    def load_data(self, file_path):
        try:
            with open(file_path, 'r', newline='') as file:
                reader = csv.reader(file)
                data = list(reader)
                self.header = data[0] 
                self._original_data = data[1:] 

                self.filter_recipeName_data()  # Load data on startup
                
            model = CSVModel(data, self.header)
            self.table_view.setModel(model)
            self.resize_columns()
        except Exception as e:
            print("Error loading CSV:", e)

    def filter_recipeName_data(self):
        filtered_data = self._original_data
        search_query = self.recipe_search_input.text().lower()
        filtered_data = [row for row in self._original_data if any(search_query in str(row[1]).lower() for cel in row)]
        model = CSVModel(filtered_data, self.header, self._original_data)
        self.table_view.setModel(model)
        self.resize_columns()
    
    def filter_ingredient_data(self):
        filtered_data = self._original_data
        search_query = self.ingredient_search_input.text().lower()
        if search_query:
            ingredients = [ingredient.strip() for ingredient in search_query.split(",")]
            filtered_data = [row for row in self._original_data if all(ingredient.lower() in row[4].lower() for ingredient in ingredients)]
            model = CSVModel(filtered_data, self.header, self._original_data)
            self.table_view.setModel(model)
            self.resize_columns()
        else:
            print("Ingredients search query is empty.")

    def filter_cookTime_data(self):
        filtered_data = self._original_data
        search_query = self.cookTime_search_input.text()
        if search_query:
            try:
              search_query = float(search_query)
              filtered_data = [row for row in self._original_data if row[3] != 'N/A' and float(row[3].split(' ')[0]) <= search_query]
              model = CSVModel(filtered_data, self.header, self._original_data)
              self.table_view.setModel(model)
              self.resize_columns()
            except ValueError:
              print("Invalid input for cook time search.")

    def filter_data(self):
        filtered_data = self._original_data

        # Recipe search
        recipe_query = self.recipe_search_input.text().strip().lower()
        if recipe_query:
            filtered_data = [row for row in filtered_data if recipe_query in row[1].lower()]

        # Ingredient search
        ingredient_query = self.ingredient_search_input.text().strip().lower()
        if ingredient_query:
            ingredients = [ingredient.strip() for ingredient in ingredient_query.split(",")]
            filtered_data = [row for row in filtered_data if all(ingredient in row[4].lower() for ingredient in ingredients)]

        # CookTime search
        cookTime_query = self.cookTime_search_input.text()
        if cookTime_query:
            try:
                cookTime_value = float(cookTime_query)
                filtered_data = [row for row in filtered_data if row[2] != 'N/A' and float(row[3].split(' ')[0]) < cookTime_value]
            except ValueError:
                print("Invalid cook time input")

        model = CSVModel(filtered_data, self.header, self._original_data)
        self.table_view.setModel(model)
        self.resize_columns()

    
    def open_row_details(self, index: QModelIndex):
        # Retrieve the data from the selected row
        model = self.table_view.model()
        row_data = [model.index(index.row(), col).data() for col in range(model.columnCount())]

        detail_dialog = QDialog(self)
        detail_dialog.setWindowTitle("Recipe Details")
        layout = QFormLayout(detail_dialog)

        for header, data in zip(self.header, row_data):
            if header == 'Recipe URL': # Add clickable link
                address_label = QLabel(f'<a href="{data}">{data}</a>')
                address_label.setTextFormat(Qt.TextFormat.RichText)
                address_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextBrowserInteraction)
                address_label.setOpenExternalLinks(True)
                layout.addRow(QLabel(header), address_label)
            else:
                layout.addRow(QLabel(header), QLabel(str(data)))

        close_button = QPushButton("Close")
        close_button.clicked.connect(detail_dialog.accept)
        layout.addWidget(close_button)

        detail_dialog.exec()

    def resize_columns(self):
        for column in range(self.table_view.model().columnCount()):
            self.table_view.resizeColumnToContents(column)

class CSVModel(QAbstractTableModel):
    def __init__(self, data, header, original_data, skip_column=0, parent=None):
        super().__init__(parent)
        self._data = data
        self._header = header
        self._original_data = original_data
        self._skip_column = skip_column

    def rowCount(self, parent=None):
        return len(self._data)

    def columnCount(self, parent=None):
        if len(self._data) > 0:
            return len(self._data[0])
        return 0

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            row = index.row() + 1
            col = index.column()
            # Adjust the column index if it's past the skipped column
            if col >= self._skip_column:
                col += 1
            if col == 0:  # URL Column
                return f'<a href="{self._data[row][col]}">{self._data[row][col]}</a>'
            if row < len(self._data) and col < len(self._data[row]):
                return str(self._data[row][col])
        return QVariant()
    
    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            if section >= self._skip_column:
                section += 1
            if section < len(self._header):
                return self._header[section]
        return super().headerData(section, orientation, role)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CSVViewer()
    window.show()
    sys.exit(app.exec())