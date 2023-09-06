import math
from typing import List

from shapely.geometry import Point, Polygon


def point_in_polygon(
    point_coords: List[float],
    polygon_coords: List[List[float]]
) -> bool:
    """
    Определяет, находится ли точка внутри полигона.

    :param point_coords: Координаты точки в формате [lat, lon].
    :type point_coords: List[float]

    :param polygon_coords: Координаты вершин полигона.
    :type polygon_coords: List[List[float]]

    :return: True, если точка находится внутри полигона, иначе False.
    :rtype: bool
    """
    # Создаем объекты Point и Polygon
    point = Point(point_coords)
    polygon = Polygon(polygon_coords)

    # Проверяем, находится ли точка внутри полигона
    if polygon.contains(point):
        return True
    else:
        return False


def _calc_distance_between_points(
    coords_first_point: List[float],
    coords_second_point: List[float]
) -> float:
    """
    Рассчитывает расстояние между двумя точками на поверхности Земли,
    используя формулу Haversine.

    :param coords_first_point: Координаты первой точки [lat, lon].
    :type coords_first_point: List[float]

    :param coords_second_point: Координаты второй точки [lat, lon].
    :type coords_second_point: List[float]

    :return: Расстояние между двумя точками в километрах.
    :rtype: float
    """

    # Радиус Земли в километрах
    radius_earth = 6371.0

    # Переводим координаты из градусов в радианы
    lat1 = math.radians(coords_first_point[0])
    lon1 = math.radians(coords_first_point[1])
    lat2 = math.radians(coords_second_point[0])
    lon2 = math.radians(coords_second_point[1])

    # Разница между широтами и долготами
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # Формула Haversine
    a = (math.sin(dlat / 2)**2 + math.cos(lat1)
         * math.cos(lat2) * math.sin(dlon / 2)**2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    # Расстояние в километрах
    distance = radius_earth * c

    return distance


def get_distance_to_polygon(
    point_coords: List[float],
    polygon_coords: List[float]
) -> float:
    """
    Вычисляет минимальное расстояние между заданной точкой и полигоном
    на поверхности Земли, используя формулу Haversine.

    :param point_coords: Координаты точки [lat, lon].
    :type point_coords: List[float]

    :param polygon_coords: Список координат вершин многоугольника в формате
                           [[широта1, долгота1], [широта2, долгота2], ...].
    :type polygon_coords: List[List[float]]

    :return: Минимальное расстояние между точкой
             и многоугольником в километрах.
    :rtype: float
    """
    min_distance = float('inf')
    # проходимся в цикле по всем точкам полигона МКАД
    # и ищем самую ближайшую к интересующему адресу
    for coords in polygon_coords:
        distance = _calc_distance_between_points(point_coords, coords)
        if distance < min_distance:
            min_distance = distance
    min_distance = round(min_distance, 3)
    return min_distance
