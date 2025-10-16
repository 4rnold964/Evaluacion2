import requests, urllib.parse, sys

API_KEY = "00c4b537-28f0-478e-9760-8cc0fa6e2f24"
GEOCODE_URL = "https://graphhopper.com/api/1/geocode?"
ROUTE_URL = "https://graphhopper.com/api/1/route?"

def geocoding(location, key):
    while location == "":
        location = input("Ingrese nuevamente la ubicación: ")
    url = GEOCODE_URL + urllib.parse.urlencode({"q":location, "limit":"1", "key":key})
    reply = requests.get(url)
    data = reply.json()
    status = reply.status_code
    if status == 200 and len(data["hits"]) != 0:
        lat = data["hits"][0]["point"]["lat"]
        lng = data["hits"][0]["point"]["lng"]
        name = data["hits"][0]["name"]
        return status, lat, lng, name
    else:
        print("⚠️ Error en geocodificación:", data.get("message","Ubicación no encontrada"))
        return status, None, None, location

while True:
    print("\n🚗 Planificador de rutas con GraphHopper")
    print("Ingrese 's' o 'salir' para terminar.")

    origen = input("🔸 Origen: ")
    if origen.lower() in ["s","salir"]:
        sys.exit()

    destino = input("🔸 Destino: ")
    if destino.lower() in ["s","salir"]:
        sys.exit()

    orig = geocoding(origen, API_KEY)
    dest = geocoding(destino, API_KEY)

    if orig[0] == 200 and dest[0] == 200:
        op = f"&point={orig[1]}%2C{orig[2]}"
        dp = f"&point={dest[1]}%2C{dest[2]}"
        url = ROUTE_URL + urllib.parse.urlencode({"key":API_KEY,"vehicle":"car","locale":"es"}) + op + dp
        r = requests.get(url)
        data = r.json()
        if r.status_code == 200:
            path = data["paths"][0]
            km = path["distance"]/1000
            tiempo = path["time"]/60000
            print(f"\n📏 Distancia total: {km:.2f} km")
            print(f"⏱️ Tiempo estimado: {tiempo:.2f} minutos")
            print("\n🧭 Instrucciones paso a paso:")
            for step in path["instructions"]:
                print(f"➡️ {step['text']} ({step['distance']/1000:.2f} km, {step['time']/60000:.2f} min)")
        else:
            print("❌ Error en la API de rutas:", data.get("message",""))