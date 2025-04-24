# pip install reportlab astral pytz
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Table, TableStyle
from datetime import datetime, timedelta
from astral import LocationInfo
from astral.sun import sun
import pytz
import os

FONT_NAME = "DejaVu"
pdfmetrics.registerFont(TTFont(FONT_NAME, "DejaVuSans.ttf"))

ESSENE_TO_HEBREW = {
    "Nisan": "נִיסָן", "Iyyar": "אִיָּר", "Sivan": "סִיוָן",
    "Tammuz": "תַּמּוּז", "Av": "אָב", "Elul": "אֱלוּל",
    "Tishri": "תִּשְׁרֵי", "Marheshvan": "מַרְחֶשְׁוָן", "Kislev": "כִּסְלֵו",
    "Tevet": "טֵבֵת", "Shevat": "שְׁבָט", "Adar": "אֲדָר",
    "Intercalary": "יום ביניים"
}

SEASON_COVERS = {
    "Nisan": "Spring",
    "Tammuz": "Summer",
    "Tishri": "Fall",
    "Tevet": "Winter"
}

ESSENE_MONTHS = [
    "Nisan", "Iyyar", "Sivan", "Tammuz", "Av", "Elul",
    "Tishri", "Marheshvan", "Kislev", "Tevet", "Shevat", "Adar"
]

INTERCALARY_POSITIONS = [91, 182, 273, 364]

FEAST_DAYS = {
    14: "Passover",
    15: "Feast of Unleavened Bread",
    21: "Wave Sheaf",
    75: "Pentecost",
    182: "Day of Trumpets",
    189: "Day of Atonement",
    196: "Feast of Tabernacles",
    203: "Last Great Day"
}


def draw_cover_page(c, season):
    c.setFillColor(colors.lightgrey)
    c.rect(0, 0, LETTER[0], LETTER[1], fill=1)
    c.setFillColor(colors.black)
    c.setFont(FONT_NAME, 36)
    c.drawCentredString(4.25*inch, 6.5*inch, f"{season} Season")
    c.setFont(FONT_NAME, 18)
    c.drawCentredString(4.25*inch, 6.0*inch, "Essene Calendar 2025-2026")
    c.showPage()

def draw_month_page(c, month_name, days):
    hebrew = ESSENE_TO_HEBREW.get(month_name, "")
    
    # Leave margin space
    c.setFont(FONT_NAME, 16)
    c.drawString(1 * inch, 10.5 * inch, f"{month_name} / {hebrew}")
    
    data = [["Gregorian", "Essene/Hebrew", "Weekday", "Sunrise", "Sunset", "Feast"]]
    for day in days:
        hebrew_month = ESSENE_TO_HEBREW.get(day["Essene Month"], "")
        row = [
            day["Gregorian Date"],
            f'{day["Essene Month"]} {day["Day"]} / {day["Day"]} {hebrew_month}',
            day["Weekday"],
            day["Sunrise"],
            day["Sunset"],
            ', '.join(day["Feast"]) if day["Feast"] else ""
        ]
        data.append(row)
    
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('GRID', (0, 0), (-1, -1), 0.25, colors.grey),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('FONTNAME', (0, 0), (-1, -1), FONT_NAME),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ])
    
    # Chunk data to fit on page (~30 rows per page)
    rows_per_page = 30
    for i in range(0, len(data[1:]), rows_per_page):
        chunk = [data[0]] + data[i+1:i+1+rows_per_page]
        table = Table(chunk, colWidths=[1.1*inch]*6)
        table.setStyle(style)
        table.wrapOn(c, 0, 0)
        table.drawOn(c, 0.7 * inch, 9.8*inch - table._height)
        c.showPage()

def generate_pdf(calendar_data, filename):
    c = canvas.Canvas(filename, pagesize=LETTER)
    c.setFont(FONT_NAME, 10)
    
    months = {}
    for day in calendar_data:
        key = day["Essene Month"]
        months.setdefault(key, []).append(day)
    
    added_seasons = set()
    for month in ESSENE_MONTHS:
        if month in months:
            season = SEASON_COVERS.get(month)
            if season and season not in added_seasons:
                draw_cover_page(c, season)
                added_seasons.add(season)
            draw_month_page(c, month, months[month])
    
    if "Intercalary" in months:
        draw_month_page(c, "Intercalary", months["Intercalary"])
    
    c.save()
    print(f"PDF saved: {filename}")


def generate_essene_calendar(start_date, end_date, location):
    current_date = start_date
    days = []
    essene_day_of_year = 1
    month_index = 0
    day_in_month = 1
    tz = pytz.timezone(location.timezone)
    
    while current_date <= end_date:
        if essene_day_of_year in INTERCALARY_POSITIONS:
            essene_month = "Intercalary"
            day_in_month = 1
        else:
            essene_month = ESSENE_MONTHS[month_index % 12]
        
        s = sun(location.observer, date=current_date, tzinfo=tz)
        
        feast = FEAST_DAYS.get(essene_day_of_year, "")
        days.append({
            "Gregorian Date": current_date.strftime("%Y-%m-%d"),
            "Essene Month": essene_month,
            "Day": day_in_month,
            "Weekday": current_date.strftime("%A"),
            "Sunrise": s["sunrise"].strftime("%H:%M"),
            "Sunset": s["sunset"].strftime("%H:%M"),
            "Feast": [feast] if feast else []
        })
        
        current_date += timedelta(days=1)
        essene_day_of_year += 1
        
        if essene_month == "Intercalary":
            month_index += 1
        else:
            day_in_month += 1
            if day_in_month > 30:
                day_in_month = 1
                month_index += 1
    
    return days

if __name__ == "__main__":
    location = LocationInfo("Jerusalem", "Israel", "Asia/Jerusalem", 31.7683, 35.2137)
    start_date = datetime(2025, 3, 20)
    end_date = datetime(2026, 3, 19)
    calendar_data = generate_essene_calendar(start_date, end_date, location)
    generate_pdf(calendar_data, "Essene_Calendar_Year7.pdf")


