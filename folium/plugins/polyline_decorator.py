#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/1/29 5:14 PM
# @Author  : Karl
# @File    : polyline_decorator.py

import json

from branca.element import Figure, JavascriptLink

from folium.map import FeatureGroup
from folium.utilities import _validate_location

from jinja2 import Template


class PolylineDecorator(FeatureGroup):
    """


    """
    _template = Template(u"""
            {% macro script(this, kwargs) %}
                var {{this.get_name()}} = L.boatMarker(
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
                 heading=0, wind_heading=None, wind_speed=0, **kwargs):
        super(PolylineDecorator, self).__init__(
            _validate_location(location),
            popup=popup,
            icon=icon
        )
        self._name = 'BoatMarker'
        self.heading = heading
        self.wind_heading = wind_heading
        self.wind_speed = wind_speed
        self.kwargs = json.dumps(kwargs)

    def render(self, **kwargs):
        super(PolylineDecorator, self).render(**kwargs)

        figure = self.get_root()
        assert isinstance(figure, Figure), ('You cannot render this Element '
                                            'if it is not in a Figure.')

        figure.header.add_child(
            JavascriptLink('https://cdnjs.cloudflare.com/ajax/libs/leaflet-polylinedecorator/1.1.0/leaflet.polylineDecorator.min.js'),  # noqa
            name='polylinedecoratorjs')
