import math

def calc_distance(point_1: dict, point_2: dict)-> float: 
    """Calculate the distance [km] from the latitude and longitude of two points

    https://qiita.com/damyarou/items/9cb633e844c78307134a

    Args:
        point_1 (dict[str:float]): Point 1. key contains latitude and longitude, value is °
        point_2 (dict[str:float]): Point 2. key contains latitude and longitude, value is °

    Returns:
        Distance: Unit=km
    """
    ra = 6378.140  # equatorial radius (km)
    rb = 6356.755  # polar radius (km)
    F = (ra - rb) / ra  # flattening of the earth
    rad_lat_point_1 = math.radians(point_1["latitude"])
    rad_lon_point_1 = math.radians(point_1["longitude"])
    rad_lat_point_2 = math.radians(point_2["latitude"])
    rad_lon_point_2 = math.radians(point_2["longitude"])
    pa = math.atan(rb / ra * math.tan(rad_lat_point_1))
    pb = math.atan(rb / ra * math.tan(rad_lat_point_2))
    xx = math.acos(math.sin(pa) * math.sin(pb) + math.cos(pa) * math.cos(pb) * math.cos(rad_lon_point_1 - rad_lon_point_2))
    c1 = (math.sin(xx) - xx) * (math.sin(pa) + math.sin(pb))**2 / math.cos(xx / 2)**2
    if c1 == 0:
        return 0
    c2 = (math.sin(xx) + xx) * (math.sin(pa) - math.sin(pb))**2 / math.sin(xx / 2)**2
    dr = F / 8 * (c1 - c2)
    rho = ra * (xx + dr)
    return rho


    
def calc_speed(time_diff: float, length_new: float, length_old: float):
    """_summary_

    Args:
        time_diff (_type_): sec
        length_0 (_type_): _description_
        length_1 (_type_): _description_
    """
    return (length_new - length_old) * 3600 / time_diff