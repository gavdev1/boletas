import os
from io import BytesIO
from jinja2 import Environment, FileSystemLoader
from xhtml2pdf import pisa
from domain.schemas.boleta import BoletaResponse


class PDFService:
    def __init__(self):
        # Configurar Jinja2 para cargar plantillas desde domain/templates
        # Support PyInstaller bundled assets
        import sys
        if getattr(sys, 'frozen', False):
            # If the app is frozen, the templates are in the same directory as the executable or in _MEIPASS
            base_path = sys._MEIPASS
            template_dir = os.path.join(base_path, "domain", "templates")
        else:
            template_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates")
            
        self.jinja_env = Environment(loader=FileSystemLoader(template_dir))

    def generar_boleta_pdf(self, boleta: BoletaResponse) -> BytesIO:
        """
        Genera un PDF a partir de una boleta y lo devuelve como un objeto BytesIO.
        """
        # 1. Cargar plantilla
        template = self.jinja_env.get_template("boleta_pdf.html")

        # 2. Renderizar HTML con los datos
        # Pass template_dir as base_path for images
        import sys
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
            template_dir = os.path.join(base_path, "domain", "templates")
        else:
            template_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates")
            
        html_content = template.render(boleta=boleta, base_path=template_dir)

        # 3. Crear buffer en memoria para el PDF
        pdf_buffer = BytesIO()

        # 4. Convertir HTML a PDF
        pisa_status = pisa.CreatePDF(html_content, dest=pdf_buffer)

        if pisa_status.err:
            raise Exception("Error al generar el PDF")

        # 5. Volver al inicio del buffer para que pueda ser leído
        pdf_buffer.seek(0)
        return pdf_buffer
