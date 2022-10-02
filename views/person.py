from PySide6.QtWidgets import QHBoxLayout, QWidget

from logic.database import persist_item
from logic.model import Person
from logic.table_models import PersonModel
from views.base_classes import TableDialog, EditorDialog, EditorWidget


class AddPersonDialog(EditorDialog):

    def __init__(self, parent: QWidget):
        super(AddPersonDialog, self).__init__(parent=parent, ui_file_name="ui/personEditor.ui")

        self.widget.editorTitle.setText(self.tr("Add Person"))

        self.layout = QHBoxLayout(self)
        self.layout.addWidget(self.widget)
        self.button_box: QDialogButtonBox = self.widget.buttonBox  # noqa

        self.configure_widgets()

    def commit(self):
        first_name: str = self.widget.firstNameEdit.text()  # noqa
        last_name: str = self.widget.lastNameEdit.text()  # noqa
        email: str = self.widget.emailEdit.text()  # noqa

        person = Person(firstname=first_name, lastname=last_name, email=email)
        persist_item(person)
        self.parent.reload_table_contents(model=PersonModel())
        self.close()

    def clear_fields(self):
        self.widget.firstNameEdit.setText("")  # noqa
        self.widget.lastNameEdit.setText("")  # noqa
        self.widget.emailEdit.setText("")  # noqa


class PersonEditorWidget(EditorWidget):

    def __init__(self, item_id=None):
        super(PersonEditorWidget, self).__init__(ui_file_name="ui/personEditor.ui", item_id=item_id)

        self.firstNameEdit = self.widget.firstNameEdit  # noqa
        self.lastNameEdit = self.widget.lastNameEdit  # noqa
        self.emailEdit = self.widget.emailEdit  # noqa

    def fill_fields(self, person: Person):
        self.item_id = person.id
        self.firstNameEdit.setText(person.firstname)
        self.lastNameEdit.setText(person.lastname)
        self.emailEdit.setText(person.email)

    def get_values(self) -> dict:
        return {
            "item_id": self.item_id,
            "firstname": self.firstNameEdit.text(),
            "lastname": self.lastNameEdit.text(),
            "email": self.emailEdit.text(),
        }


class PersonWidget(TableDialog):

    def __init__(self):
        super(PersonWidget, self).__init__(table_ui_name="ui/personView.ui")
        self.add_dialog = AddPersonDialog(self)
        self.setup_table(PersonModel(), range(1, 4))

    def get_editor_widget(self) -> EditorWidget:
        return PersonEditorWidget()

    def configure_search(self):
        self.searchLine.textChanged.connect(lambda x: self.reload_table_contents(PersonModel(self.searchLine.text())))
