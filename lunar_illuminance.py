import time
import sys
from skyfield.api import load, Topos
import numpy as np

eph = load('de440s.bsp')
earth = eph['earth']
moon = eph['moon']
sun = eph['sun']

observer = Topos(latitude_degrees=38.478752, longitude_degrees=-107.877739)
observer_location = earth + observer

ts = load.timescale()

SOLAR_CONSTANT = 1361
MOON_ALBEDO = 0.12
MOON_DIAMETER_KM = 3474.8

while True:
    t = ts.now()
    moon_pos = observer_location.at(t).observe(moon).apparent()
    sun_pos = observer_location.at(t).observe(sun).apparent()

    phase_angle = moon_pos.separation_from(sun_pos).degrees
    moon_distance_km = moon_pos.distance().km

    illuminated_fraction = (1 + np.cos(np.radians(phase_angle))) / 2
    moon_area = np.pi * (MOON_DIAMETER_KM / 2) ** 2
    reflected_solar_flux = SOLAR_CONSTANT * MOON_ALBEDO * illuminated_fraction
    illuminance = reflected_solar_flux * (moon_area / (4 * np.pi * moon_distance_km ** 2))
    illuminance_lux = illuminance * 683

    altitude_degrees = moon_pos.altaz()[0].degrees

    output = f"\rLunar illuminance: {illuminance_lux:.2f} lux @ {altitude_degrees:.2f}°"
    sys.stdout.write(output)
    sys.stdout.flush()

    time.sleep(1)