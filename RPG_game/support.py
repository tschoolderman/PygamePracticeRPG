from csv import reader
from os import walk

import pygame as pg


def import_csv_layout(path):
    terrain_map = []
    with open(path) as lvl_map:
        layout = reader(lvl_map, delimiter=",")
        for row in layout:
            terrain_map.append(list(row))
        return terrain_map


def import_folder(path):
    surface_list = []
    for _, __, img_files in walk(path):
        for image in img_files:
            full_path = path + "/" + image
            image_surface = pg.image.load(full_path).convert_alpha()
            surface_list.append(image_surface)
    return surface_list
