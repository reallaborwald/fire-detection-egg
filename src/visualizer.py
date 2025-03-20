import folium
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.patheffects as PathEffects
import numpy as np
from math import radians, cos, sin, sqrt, atan2, degrees

#SKYCODE = ["E", "ENE", "NE", "NNE", "N", "NNW", "NW", "WNW", "W", "WSW", "SW", "SSW", "S", "SSE", "SE", "ESE"]
SKYCODE = ["W", "WSW", "SW", "SSW", "S", "SSE", "SE", "ESE", "E", "ENE", "NE", "NNE", "N", "NNW", "NW", "WNW"]

def make_html_map(lat, lon):
    map = folium.Map(location=[lat, lon], zoom_start=12)
    folium.Marker([lat, lon], popup="Mein Standort", icon=folium.Icon(color="red")).add_to(map)
    map.save("karte.html")

# Visualize as semi-interactive map

class ZoomPan:
    def __init__(self, ax, zoom_center, initial_zoom):
        self.ax = ax
        self.cid_scroll = ax.figure.canvas.mpl_connect('scroll_event', self.on_scroll)
        self.cid_press = ax.figure.canvas.mpl_connect('button_press_event', self.on_press)
        self.cid_release = ax.figure.canvas.mpl_connect('button_release_event', self.on_release)
        self.cid_motion = ax.figure.canvas.mpl_connect('motion_notify_event', self.on_motion)
        self.press_event = None
        self.annotations = []
        self.arrows = []
        self.cid = ax.figure.canvas.mpl_connect('draw_event', self.on_draw)
        self.set_initial_zoom(zoom_center, initial_zoom)

    def set_initial_zoom(self, zoom_center, zoom_factor):
        xlim = self.ax.get_xlim()
        ylim = self.ax.get_ylim()
        
        new_xlim = [zoom_center[0] + (x - zoom_center[0]) / zoom_factor for x in xlim]
        new_ylim = [zoom_center[1] + (y - zoom_center[1]) / zoom_factor for y in ylim]
        
        self.ax.set_xlim(new_xlim)
        self.ax.set_ylim(new_ylim)
        self.ax.figure.canvas.draw()
        
    def add_annotation(self, annotation):
        """Adds an annotation to be managed."""
        self.annotations.append(annotation)
        
    def add_arrow(self, arrow):
        """Adds an arrow to be managed."""
        self.arrows.append(arrow)

    def on_scroll(self, event):
        scale_factor = 1.2 if event.step > 0 else 0.8
        xlim = self.ax.get_xlim()
        ylim = self.ax.get_ylim()
        xdata, ydata = event.xdata, event.ydata

        new_xlim = [xdata + (x - xdata) * scale_factor for x in xlim]
        new_ylim = [ydata + (y - ydata) * scale_factor for y in ylim]
        
        self.ax.set_xlim(new_xlim)
        self.ax.set_ylim(new_ylim)
        self.ax.figure.canvas.draw()

    def on_press(self, event):
        if event.button == 1:
            self.press_event = event

    def on_release(self, event):
        self.press_event = None

    def on_motion(self, event):
        if self.press_event is None:
            return
        dx = self.press_event.xdata - event.xdata
        dy = self.press_event.ydata - event.ydata
        
        xlim = self.ax.get_xlim()
        ylim = self.ax.get_ylim()
        
        self.ax.set_xlim([x + dx for x in xlim])
        self.ax.set_ylim([y + dy for y in ylim])
        self.ax.figure.canvas.draw()
        
    def on_draw(self, event):
        """Toggle visibility of annotations based on zoom level and pan."""
        xlim, ylim = self.ax.get_xlim(), self.ax.get_ylim()
        #for ann in self.annotations:
        #    x, y = ann.xy
        #    #ann.set_visible(xlim[0] <= x <= xlim[1] and ylim[0] <= y <= ylim[1])
        #    color = 'red' if (xlim[0] <= x <= xlim[1] and ylim[0] <= y <= ylim[1]) else 'orange'
        #    ann.arrow_patch.set_color(color)
        for arrow, target, origin in self.arrows:
            x, y = target
            x0, y0 = origin
            color = 'red' if (xlim[0] <= x <= xlim[1] and ylim[0] <= y <= ylim[1]) else 'orange'
            arrow.arrow_patch.set_color(color)
            '''if ylim[0] <= y <= ylim[1]:
                if xlim[0] > x:
                    x_clip = xlim[0]
                    dy = sqrt(np.power(x-x0, 2)/(np.linalg.norm(np.array((x,y))-np.array((x0, y0)))/(y - y0) - 1))
                    y_clip = y0+dy
                elif xlim[1] < x:
                    x_clip = xlim[1]
                    y_clip = ...
                else:
                    x_clip = x
                y_clip = y
            else:            
                y_clip = ylim[1]
                
            arrow.xy = (x_clip, y_clip)
            '''
            #arrow.arrow_patch.set_shrinkA(0.8)
        self.ax.figure.canvas.draw_idle()

# load shapefile maps (and store them pre-loaded)

def make_map(own_pos, fire_pos = []):
    lat, lon = own_pos
    # Höhenlinien aus einer Shapefile laden
    hoehenlinien1 = gpd.read_file("./map/N41E008/N41E008.shp")
    hoehenlinien2 = gpd.read_file("./map/N41E009/N41E009.shp")
    hoehenlinien3 = gpd.read_file("./map/N42E009/N42E009.shp")
    hoehenlinien4 = gpd.read_file("./map/N42E008/N42E008.shp")

    # visualize contour lines
    fig, ax = plt.subplots(figsize=(10, 10))
    hoehenlinien1.plot(ax=ax, color="gray", linewidth=0.5, zorder = -1)
    hoehenlinien2.plot(ax=ax, color="gray", linewidth=0.5, zorder = -1)
    hoehenlinien3.plot(ax=ax, color="gray", linewidth=0.5, zorder = -1)
    hoehenlinien4.plot(ax=ax, color="gray", linewidth=0.5, zorder = -1)
    
    start_zoom = 0.0001
    ax.set_xlim(lon - start_zoom, lon + start_zoom)
    ax.set_ylim(lat - start_zoom, lat + start_zoom)

    zoom_pan = ZoomPan(ax, (lon, lat), 0.005) # TODO zoom faktor mit Kilometer in Verbindung bringen

    # Punkte hinzufügen
    plt.scatter([lon], [lat], color="blue", label="Aktueller Standort", zorder = 4)
    
    for (latf, lonf) in fire_pos:
        
        
        # TODO: Pfeil zeige auf Displaypunkt , wenn Datenpunkt nicht im Bild
        dist = round(coord_2_km(lat, lon, latf, lonf), 2)
        if dist > 10.0:
            continue
        if dist < 0.1:
            skydir = direction((lon, lat), (lonf, latf))
            txt = ax.text(lon, lat, f"CAUTION!\nFIRE DIRECTLY \n{skydir} FROM YOU", weight = "heavy", size = "x-large", zorder = 9, color = "darkred")
            txt.set_path_effects([PathEffects.withStroke(linewidth=3, foreground='w')])
            continue
        
        plt.scatter([lonf], [latf], color="red", label="Feuer", marker = "X", zorder = 6)
        x = ax.get_xlim()
        y = ax.get_ylim()
        
        
        ann = ax.annotate("", xytext=(lon, lat), xy=(lonf, latf), arrowprops=dict(color = 'blue', linewidth=3, shrink = 0.05, alpha = 0.8), annotation_clip = False)
        skydir = direction((lon, lat), (lonf, latf))
        ax.text((lonf-lon)/4 + lon, (latf-lat)/4 + lat, str(dist)+" km, " + skydir, weight = "heavy", size = "large", zorder = 8)
        '''if x[0] < lonf < x[1] and y[0] < latf < y[1] and x[0] < lon < x[1] and y[0] < lat < y[1]:
            ann = ax.annotate("", xytext=(lon, lat), xy=(lonf, latf), arrowprops=dict(color = 'red', linewidth=3, shrink = 0.1), annotation_clip = False)
            #ax.annotate(str(dist) + " km",  xy=((lonf-lon)/2 + lon, (latf-lat)/2 + lat), )
            ax.text((lonf-lon)/2 + lon, (latf-lat)/2 + lat, str(dist)+" km", weight = "heavy", size = "large", zorder = 8)
        else:
            ann = ax.annotate("", xytext=(lon, lat), xy=(lonf, latf), arrowprops=dict(color = 'orange', linewidth=3, shrink = 0.1), annotation_clip = False)
            ax.text((lonf-lon)/2 + lon, (latf-lat)/2 + lat, str(dist)+" km", weight = "heavy", size = "large", zorder = 8)
        #plot_arrow(ax, (lat, lon), (latf, lonf))
        '''
        
        #zoom_pan.add_annotation(ann)
        zoom_pan.add_arrow((ann, (lonf, latf), (lon, lat)))
    
    plt.legend()
    
    plt.show()
    
def plot_arrow(ax, A, B, display_point=None):
    """
    Draws an arrow from point A to point B if B is within the data limits.
    If B is outside, an arrow points towards B up to the display_point using ax.annotate().
    """
    xlim, ylim = ax.get_xlim(), ax.get_ylim()
    color = 'red' if (xlim[0] <= B[0] <= xlim[1] and ylim[0] <= B[1] <= ylim[1]) else 'blue'
    target = B if color == 'red' else display_point if display_point else ((A[0] + B[0]) / 2, (A[1] + B[1]) / 2)
    arrow = ax.annotate("", xy=target, xytext=A, arrowprops=dict(arrowstyle="->", color=color, lw=1.5))
    return arrow

# GPGGA to lat long
def parse_gpgga(sentence):
    """
    Parses a GPGGA NMEA sentence and returns latitude and longitude in decimal degrees.
    Example GPGGA sentence:
    $GPGGA,123519,4157.038,N,00901.000,E,1,08,0.9,545.4,M,46.9,M,,*47
    """
    parts = sentence.split(",")
    if parts[0] != "$GPGGA":
        raise ValueError("Not a GPGGA sentence")
    
    try:
        # Parse latitude
        lat_raw = float(parts[2])
        lat_deg = int(lat_raw / 100)
        lat_min = lat_raw - lat_deg * 100
        lat = lat_deg + (lat_min / 60)
        if parts[3] == "S":
            lat = -lat
        
        # Parse longitude
        lon_raw = float(parts[4])
        lon_deg = int(lon_raw / 100)
        lon_min = lon_raw - lon_deg * 100
        lon = lon_deg + (lon_min / 60)
        if parts[5] == "W":
            lon = -lon
        
        return lat, lon
    except (IndexError, ValueError):
        raise ValueError("Invalid GPGGA sentence format")


def coord_2_km(lat1, lon1, lat2, lon2):
    """
    Calculates the great-circle distance between two points 
    given in decimal degrees using the Haversine formula.
    """
    R = 6378.0  # Radius of Earth in kilometers # TODO genau an Korsika anpassen?
    
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    
    return R * c 

# Himmelsrichtung

def direction(origin, target):
    alpha = calculate_angle(origin[0], origin[1], target[0], target[1])
    #for i, j in enumerate(np.arange(11.25, 360, 22.5)):
    for i, j in enumerate(np.arange(-168.75, 180, 22.5)):
        if alpha < j:
            return SKYCODE[i]
    


def calculate_angle(x1, y1, x2, y2):
    """
    Calculates the angle (in degrees) between two points relative to the positive x-axis.
    """
    delta_x = x2 - x1
    delta_y = y2 - y1
    angle_rad = atan2(delta_y, delta_x)  # atan2 handles correct quadrant
    angle_deg = degrees(angle_rad)  # Convert radians to degrees
    return angle_deg

# find own position


# visualize received coordinates as fire points

# include measured distances to nearest fire locations

# include compass

# 