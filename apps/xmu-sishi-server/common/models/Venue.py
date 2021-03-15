#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Venue():
    def __init__(self, venue):
        # self.id= venue['id']
        self.name= venue['name']
        self.cloud= venue['cloud']
        self.score= venue['score']
        self.open_time= venue['open_time']
        self.must_know= venue['must_know']
        self.intro_text= venue['intro_text']
        self.intro_audio= venue['intro_audio']
        self.intro_video= venue['intro_video']
