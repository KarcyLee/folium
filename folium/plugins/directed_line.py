#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/2/12 6:02 PM
# @Author  : Karl
# @File    : directed_line.py

from __future__ import absolute_import, division, print_function

import json
from jinja2 import Template
from branca.element import Figure, JavascriptLink
from folium.map import Marker


def path_options(line=False, radius=False, **kwargs):
    """
    Contains options and constants shared between vector overlays
    (Polygon, Polyline, Circle, CircleMarker, and Rectangle).

    Parameters
    ----------
    stroke: Bool, True
        Whether to draw stroke along the path.
        Set it to false to disable borders on polygons or circles.
    color: str, '#3388ff'
        Stroke color.
    weight: int, 3
        Stroke width in pixels.
    opacity: float, 1.0
        Stroke opacity.
    line_cap: str, 'round' (lineCap)
        A string that defines shape to be used at the end of the stroke.
        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/stroke-linecap
    line_join: str, 'round' (lineJoin)
        A string that defines shape to be used at the corners of the stroke.
        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/stroke-linejoin
    dash_array: str, None (dashArray)
        A string that defines the stroke dash pattern.
        Doesn't work on Canvas-powered layers in some old browsers.
        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/stroke-dasharray
    dash_offset:, str, None (dashOffset)
        A string that defines the distance into the dash pattern to start the dash.
        Doesn't work on Canvas-powered layers in some old browsers.
        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/stroke-dashoffset
    fill: Bool, False
        Whether to fill the path with color.
        Set it to false to disable filling on polygons or circles.
    fill_color: str, default to `color` (fillColor)
        Fill color. Defaults to the value of the color option.
    fill_opacity: float, 0.2 (fillOpacity)
        Fill opacity.
    fill_rule: str, 'evenodd' (fillRule)
        A string that defines how the inside of a shape is determined.
        https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/fill-rule
    bubbling_mouse_events: Bool, True (bubblingMouseEvents)
        When true a mouse event on this path will trigger the same event on the
        map (unless L.DomEvent.stopPropagation is used).

    Note that the presence of `fill_color` will override `fill=False`.

    See https://leafletjs.com/reference-1.4.0.html#path

    """

    extra_options = {}
    if line:
        extra_options = {
            'smoothFactor': kwargs.pop('smooth_factor', 1.0),
            'noClip': kwargs.pop('no_clip', False),
        }
    if radius:
        extra_options.update({'radius': radius})

    color = kwargs.pop('color', '#3388ff')
    fill_color = kwargs.pop('fill_color', False)
    if fill_color:
        fill = True
    elif not fill_color:
        fill_color = color
        fill = kwargs.pop('fill', False)

    default = {
        'stroke': kwargs.pop('stroke', True),
        'color': color,
        'weight': kwargs.pop('weight', 3),
        'opacity': kwargs.pop('opacity', 1.0),
        'lineCap': kwargs.pop('line_cap', 'round'),
        'lineJoin': kwargs.pop('line_join', 'round'),
        'dashArray': kwargs.pop('dash_array', None),
        'dashOffset': kwargs.pop('dash_offset', None),
        'fill': fill,
        'fillColor': fill_color,
        'fillOpacity': kwargs.pop('fill_opacity', 0.2),
        'fillRule': kwargs.pop('fill_rule', 'evenodd'),
        'bubblingMouseEvents': kwargs.pop('bubbling_mouse_events', True),
    }
    default.update(extra_options)
    return default


def reverse_vector(line):
    """
    reverse vector. (a, b) ---> (b, a)
    :param line:
    :return:
    """
    if line is None or len(line) != 2:
        raise ValueError("input param should contain 2 elements!")
    return (line[1], line[0])


class DirectedLine(Marker):
    """
    Class for drawing directed line overlays on a map.

    Parameters
    ----------
    locations: list of points (latitude, longitude)
        Latitude and Longitude of line (Northing, Easting)
    popup: str or folium.Popup, default None
        Input text or visualization for object displayed when clicking.
    tooltip: str or folium.Tooltip, default None
        Display a text when hovering over the object.
    smooth_factor: float, default 1.0
        How much to simplify the polyline on each zoom level.
        More means better performance and smoother look,
        and less means more accurate representation.
    no_clip: Bool, default False
        Disable polyline clipping.


    See https://leafletjs.com/reference-1.4.0.html#polyline

    """

    _template = Template(u"""
            {% macro script(this, kwargs) %}
            
                var {{this.get_name()}} = L.polyline(
                    {{this.location}},
                    {{this.options}}
                    )
                    .addTo({{this._parent.get_name()}});
                    
                 {{this.get_name()}}.setText("{{this.text}}", {
                    repeat: {{'true' if this.repeat else 'false'}},
                    center: {{'true' if this.center else 'false'}},
                    below: {{'true' if this.below else 'false'}},
                    offset: {{this.offset}},
                    orientation: 180,
                    attributes: { 'font-size': '{{this.font_size}}', 'fill': "{{this.color}}" }
                });  
                              
            {% endmacro %}
            """)  # noqa

    def __init__(self, src, dst, popup=None, tooltip=None, weight=3,
                 repeat=False, center=False, below=False,
                 offset=0, attributes=None, color='black',
                 **kwargs):
        _location = [dst, src]
        super(DirectedLine, self).__init__(location=_location,
                                           popup=popup,
                                           tooltip=tooltip)

        self.location = _location
        self._name = 'DirectedLine'
        self.options = self._parse_options(color, weight, line=True, **kwargs)

        self.text = "►"
        self.repeat = bool(repeat)
        self.center = bool(center)
        self.below = bool(below)
        self.font_size = weight * 4
        # self.offset = int(self.font_size / 2)
        self.offset = (self.font_size - weight) / 2
        # self.attributes = attributes
        self.color = color

        return

    def render(self, **kwargs):
        super(DirectedLine, self).render(**kwargs)

        figure = self.get_root()
        assert isinstance(figure, Figure), ('You cannot render this Element '
                                            'if it is not in a Figure.')

        figure.header.add_child(
            JavascriptLink("https://cdn.jsdelivr.net/gh/makinacorpus/Leaflet.TextPath@1.2.1/leaflet.textpath.js"),
            name='polylinetextpath'
        )

    def _parse_options(self, color, weight, line=False, radius=False, **kwargs):
        options = path_options(line=line, radius=radius, **kwargs)
        options['color'] = color
        options['weight'] = weight
        return json.dumps(options, sort_keys=True, indent=2)
