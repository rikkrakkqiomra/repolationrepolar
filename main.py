import PyPDF2
import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.filechooser import FileChooserListView
from tkinter import filedialog


class PDFtoTextConverter(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # build the UI
        self.orientation = 'vertical'
        self.padding = 20
        self.size_hint = (1, 1)

        # add a label to show the selected file
        self.file_label = Label(text='No file selected')
        self.add_widget(self.file_label)

        # add a file chooser
        self.file_chooser = FileChooserListView()
        self.file_chooser.filters = ['*.pdf']
        self.add_widget(self.file_chooser)

        # add a button to convert the PDF file to text
        self.convert_button = Button(text='Convert to text', disabled=True)
        self.convert_button.bind(on_press=self.convert_pdf_to_text)
        self.add_widget(self.convert_button)

        # add a button to select a file
        self.select_button = Button(text='Select a PDF file')
        self.select_button.bind(on_press=self.select_pdf_file)
        self.add_widget(self.select_button)

    def select_pdf_file(self, instance):
        # show the file dialog to select a PDF file
        pdf_file_path = filedialog.askopenfilename(
            filetypes=[("PDF Files", "*.pdf")],
            title="Select a PDF file"
        )

        # update the label to show the selected file
        self.file_label.text = os.path.basename(pdf_file_path)

        # enable the convert button
        self.convert_button.disabled = False

    def convert_pdf_to_text(self, instance):
        # get the path of the selected PDF file
        pdf_file_path = self.file_chooser.selection[0]

        # open the PDF file in read binary mode
        with open(pdf_file_path, 'rb') as pdf_file:
            # create a PDF reader object
            pdf_reader = PyPDF2.PdfReader(pdf_file)

            # create a text file with the same name as the PDF file
            txt_file_path = pdf_file_path.replace('.pdf', '.txt')
            with open(txt_file_path, 'w') as txt_file:
                # loop through each page in the PDF file
                for page_num in range(len(pdf_reader.pages)):
                    # extract the text from the current page
                    page_text = pdf_reader.pages[page_num].extract_text()

                    # write the text to the text file
                    txt_file.write(page_text)

        # show a message to the user
        self.file_label.text = 'PDF file converted to text'
        self.convert_button.disabled = True


class PDFtoTextApp(App):
    def build(self):
        return PDFtoTextConverter()


if __name__ == '__main__':
    PDFtoTextApp().run()