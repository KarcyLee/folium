#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/1/29 4:32 PM
# @Author  : Karl
# @File    : rotated_marker.py

from __future__ import (absolute_import, division, print_function)

import json

from branca.element import Figure, JavascriptLink

from folium.map import Marker
from folium.utilities import _validate_location

from jinja2 import Template


class RotatedMarker(Marker):
    """
    """
    _template = Template(u"""
            {% macro script(this, kwargs) %}
                var {{this.get_name()}} = L.marker(
                    [{{this.location[0]}},{{this.location[1]}}],
                    {{this.kwargs}}).addTo({{this._parent.get_name()}});
                {% if this.wind_heading is not none -%}
                {{this.get_name()}}.setHeadingWind({{this.heading}}, {{this.wind_speed}}, {{this.wind_heading}});
                {% else -%}
                {{this.get_name()}}.setHeading({{this.heading}});
                {% endif -%}
            {% endmacro %}
            """)  # noqa

    def __init__(self, location, popup=None, icon=None,
                 rotation_angle=0, rotation_origin='center center', **kwargs):
        super(RotatedMarker, self).__init__(
            _validate_location(location),
            popup=popup,
            icon=icon
        )
        self._name = 'RotatedMarker'
        self._rotation_angle = rotation_angle
        self._rotation_origin = rotation_origin

        _kwargs = {}
        _kwargs["rotationAngle"] = rotation_angle
        _kwargs["rotationOrigin"] = rotation_origin
        _kwargs.update(kwargs)
        self.kwargs = json.dumps(_kwargs)


        return

    def render(self, **kwargs):
        super(RotatedMarker, self).render(**kwargs)

        figure = self.get_root()
        assert isinstance(figure, Figure), ('You cannot render this Element '
                                            'if it is not in a Figure.')

        figure.header.add_child(
            JavascriptLink('https://cdn.jsdelivr.net/gh/bbecquet/Leaflet.RotatedMarker@0.2.0/leaflet.rotatedMarker.js'),  # noqa
            name='rotatedmarkerjs')
