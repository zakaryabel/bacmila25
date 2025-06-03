from flask import Flask, request, send_file
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import arabic_reshaper
from bidi.algorithm import get_display
import io
from datetime import datetime

app = Flask(__name__)

pdfmetrics.registerFont(TTFont('Arial', 'arial.ttf'))

def draw_arabic_text(c, text, x, y, fontname='Arial', fontsize=12):
    reshaped_text = arabic_reshaper.reshape(text)
    bidi_text = get_display(reshaped_text)
    c.setFont(fontname, fontsize)
    c.drawRightString(x, y, bidi_text)

@app.route('/generate_pdf', methods=['POST'])
def generate_pdf():
    data = request.json

    buffer = io.BytesIO()
    c = canvas.Canvas(buffer)
    width, height = 595, 842  # A4 size

    c.setFont('Arial', 16)
    c.drawCentredString(width/2, height - 50, "استمارة معلومات خاصة بموظفي مركز البكالوريا - 2025")

    draw_arabic_text(c, f"اللقب: {data.get('lastName','')}", 550, 750)
    draw_arabic_text(c, f"الاسم: {data.get('firstName','')}", 550, 730)
    draw_arabic_text(c, f"اللقب والاسم باللاتينية: {data.get('latinName','')}", 550, 710)
    birth_date = f"{data.get('birthDay','')}/{data.get('birthMonth','')}/{data.get('birthYear','')}"
    draw_arabic_text(c, f"تاريخ الازدياد: {birth_date}", 550, 690)
    draw_arabic_text(c, f"مكان الازدياد: {data.get('birthPlace','')}", 550, 670)
    draw_arabic_text(c, f"الرتبة: {data.get('rank','')}", 550, 650)
    draw_arabic_text(c, f"مؤسسة العمل: {data.get('institution','')}", 550, 630)
    draw_arabic_text(c, f"الوظيفة في المركز: {data.get('function','')}", 550, 610)
    draw_arabic_text(c, f"المادة: {data.get('subject','')}", 550, 590)
    draw_arabic_text(c, f"رقم الحساب البريدي: {data.get('postalAccountNumber','')}", 550, 570)
    draw_arabic_text(c, f"المفتاح: {data.get('postalKey','')}", 550, 550)

    today_str = datetime.now().strftime("%d/%m/%Y")
    draw_arabic_text(c, f"حرر بميلة في: {today_str}", 550, 520)

    c.showPage()
    c.save()

    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name="استمارة_معلومات.pdf", mimetype='application/pdf')

if __name__ == "__main__":
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
