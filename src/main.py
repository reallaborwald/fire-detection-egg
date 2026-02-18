import visualizer
import random
import json
# Todo:
# Pfeile aktualisieren, im Bild lassen und Farbe ändern je nachdem, ob es im Bild ist --> Polarkoordinaten??
# Infos vom digitalen Kompass abrufen
# Himmelsrichtungsinfos (Norden anzeigen auf der Karte auch bei drehendem User) hinzufügen (auch an Pfeile) (aus GPS daten) (1)
# LoRa Daten dekodieren und ID (Feuergps) aus Datenbank interpretieren 
# eigene GPS Koordinaten auslesen
# 

SEED = 300

if __name__ == '__main__':
    
    version = 0
    
    if version == 0:
        
        own_pos = "$GPGGA,123519,4157.038,N,00901.000,E,1,08,0.9,545.4,M,46.9,M,,*47"
        fire_pos1 = "$GPGGA,123519,4158.038,N,00900.400,E,1,08,0.9,545.4,M,46.9,M,,*47"
        fire_pos2 = "$GPGGA,123519,4157.038,N,00903.000,E,1,08,0.9,545.4,M,46.9,M,,*47"
        visualizer.make_map(visualizer.parse_gpgga(own_pos), [visualizer.parse_gpgga(fire_pos1), visualizer.parse_gpgga(fire_pos2)])
    
        
    elif version == 1:
        
    
        rng = random.seed(SEED)
        #rng = random.seed()
        
        own_pos_no = random.randint(0, 8)
        fire_ids = []
        no_of_fires = random.randint(1, 5)
        for i in range(no_of_fires):
            fire_ids.append(random.randint(0, 7))
        fire_ids = set(fire_ids)
        
        with open('own_locations.json', 'r') as file:
            own_pos_dict = json.load(file)
        
        with open('tx_locations.json', 'r') as file:
            fire_pos_dict = json.load(file)
        
        
        
        own_pos = own_pos_dict[str(own_pos_no)]["gpgga_location"]
        fire_pos = []
        for id in fire_ids:
            fire_pos.append(visualizer.parse_gpgga(fire_pos_dict[str(id)]["gpgga_location"]))
        
        visualizer.make_map(visualizer.parse_gpgga(own_pos), fire_pos)