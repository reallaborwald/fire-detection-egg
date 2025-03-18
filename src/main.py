import visualizer
# Todo:
# Pfeile aktualisieren, im Bild lassen und Farbe ändern je nachdem, ob es im Bild ist
# Infos vom digitalen Kompass abrufen
# Himmelsrichtungsinfos hinzufügen
# LoRa Daten dekodieren und ID (Feuergps) aus Datenbank interpretieren 
# eigene GPS Koordinaten auslesen
# 

if __name__ == '__main__':
    own_pos = "$GPGGA,123519,4157.038,N,00901.000,E,1,08,0.9,545.4,M,46.9,M,,*47"
    fire_pos1 = "$GPGGA,123519,4158.038,N,00901.000,E,1,08,0.9,545.4,M,46.9,M,,*47"
    fire_pos2 = "$GPGGA,123519,4157.038,N,00903.000,E,1,08,0.9,545.4,M,46.9,M,,*47"
    visualizer.make_map(visualizer.parse_gpgga(own_pos), [visualizer.parse_gpgga(fire_pos1), visualizer.parse_gpgga(fire_pos2)])