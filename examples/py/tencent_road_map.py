#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 腾讯地图示意图
from __future__ import print_function
import random
import folium
from folium.features import DivIcon
from folium.plugins import MarkerCluster


def tencent_marker(out_dir="../../out"):
    """
    腾讯地图，打点
    :param out_dir:
    :return:
    """
    map_osm = folium.Map(location=[31.32, 120.63], zoom_start=12)
    folium.Marker(location=[31.35742, 120.94784], icon=folium.Icon(color='blue', icon='ok-sign')).add_to(
        map_osm)
    folium.Marker(location=[31.32, 120.63], icon=folium.Icon(color='red', icon='info-sign')).add_to(map_osm)

    file_path = "{}/tencent_roadmap.html".format(out_dir)
    map_osm.save(file_path)


def tencent_polyline(out_dir="../../out"):
    """腾讯地图，多边形"""
    map_osm = folium.Map(location=[31.32, 120.63], zoom_start=12)

    locs = [[31.387113, 120.929393], [31.364861, 120.609265], [31.226864, 120.511118],
            [31.269273, 120.750024], [31.264751, 120.598769], [31.299345, 120.742185],
            ]
    for loc in locs:
        folium.Marker(loc).add_to(map_osm)

    folium.PolyLine(
        locs,
        fill_color='high',
        fill=True,
        fill_opacity=0.6,
        stroke=False).add_to(map_osm)

    file_path = "{}/tencent_polyline.html".format(out_dir)
    map_osm.save(file_path)


def tencent_marker_with_number(out_dir="../../out"):
    """腾讯地图，marker 上标记数字"""
    map_osm = folium.Map(location=[31.32, 120.63], zoom_start=12, subdomains="012")

    locs = [[31.387113, 120.929393], [31.364861, 120.609265], [31.226864, 120.511118],
            [31.269273, 120.750024], [31.264751, 120.598769], [31.299345, 120.742185],
            ]
    for loc in locs:
        value = random.randint(0, 100)
        # 字符
        folium.Marker(loc,
                           icon=DivIcon(icon_size=(150, 36),
                                        icon_anchor=(7, 20),
                                        html='<div style="font-size: 18pt; color : black">{}</div>'.format(value),
                                        )
                           ).add_to(map_osm)
        # 圆圈
        map_osm.add_child(folium.CircleMarker(loc, radius=20))

    file_path = "{}/tencent_marker_with_number.html".format(out_dir)
    map_osm.save(file_path)


def tencent_marker_cluster(out_dir="../../out"):
    """腾讯地图，marker 集合"""
    map_osm = folium.Map(location=[31.32, 120.63], zoom_start=12, subdomains="012")

    locs = [[31.387113, 120.929393], [31.364861, 120.609265], [31.226864, 120.511118],
            [31.269273, 120.750024], [31.264751, 120.598769], [31.299345, 120.742185],
            ]

    marker_cluster = MarkerCluster().add_to(map_osm)

    for loc in locs:
        folium.Marker(loc,
                           popup='Add popup text here.',
                           ).add_to(marker_cluster)

    file_path = "{}/tencent_marker_cluster.html".format(out_dir)
    map_osm.save(file_path)

def gaode_arrow(out_dir="../../out"):
    """
    高德地图 箭头
    :param out_dir:
    :return:
    """
    map_osm = folium.Map(location=[31.32, 120.63], zoom_start=12, tiles="Gaode")


    folium.RegularPolygonMarker(location=(31.25, 120.742185), fill_color='red', number_of_sides=3, radius=10,
                                rotation=0).add_to(map_osm)

    file_path = "{}/gaode_arrow.html".format(out_dir)
    map_osm.save(file_path)

    return

def tencent_hexagon_with_number(out_dir="../../out"):
    """腾讯地图，带数字的六边形集合"""
    map_osm = folium.Map(location=[31.32, 120.63], zoom_start=12, subdomains="012")

    locs = [[31.387113, 120.929393], [31.364861, 120.609265], [31.226864, 120.511118],
            [31.269273, 120.750024], [31.264751, 120.598769], [31.299345, 120.742185],
            ]

    marker_cluster = MarkerCluster().add_to(map_osm)

    for loc in locs:
        folium.Marker(loc,
                           popup='Add popup text here.',
                           ).add_to(marker_cluster)

    file_path = "{}/tencent_hexagon_with_number.html".format(out_dir)
    map_osm.save(file_path)


def tencent_hello(out_dir="../../out"):
    """腾讯地图，带数字的六边形集合"""
    map_osm = folium.Map(location=[31.32, 120.63], zoom_start=12)

    locs = [[31.387113, 120.929393], [31.364861, 120.609265], [31.226864, 120.511118],
            [31.269273, 120.750024], [31.264751, 120.598769], [31.299345, 120.742185],
            ]
    for loc in locs:
        folium.Marker(loc).add_to(map_osm)

    folium.PolyLine(
        locs,
        fill_color='high',
        fill=True,
        fill_opacity=0.6,
        stroke=False).add_to(map_osm)

    file_path = "{}/tencent_hello.html".format(out_dir)
    map_osm.save(file_path)


if __name__ == "__main__":
    print()
    tencent_marker()
    tencent_polyline()
    tencent_marker_with_number()
    tencent_marker_cluster()
    tencent_hexagon_with_number()
    gaode_arrow()
    tencent_hello()
