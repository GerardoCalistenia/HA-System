import datetime

def fecha_actual(request):
    meses = [
        "enero", "febrero", "marzo", "abril", "mayo", "junio",
        "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"
    ]

    hoy = datetime.date.today()
    fecha = f"{hoy.day} de {meses[hoy.month - 1]} de {hoy.year}"
    return {"fecha_actual": fecha}
