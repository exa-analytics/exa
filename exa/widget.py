# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
##################
"""
from pythreejs import ParametricGeometry, LambertMaterial
from pythreejs import DirectionalLight, AmbientLight
from pythreejs import Scene, Renderer, Mesh
from pythreejs import PerspectiveCamera, TrackballControls


func = """function f(origu,origv) {
    var u = 2*Math.PI*origu;
    var v = 2*Math.PI*origv;
    var x = Math.sin(u);
    var y = Math.cos(v);
    var z = Math.cos(u+v);
    return new THREE.Vector3(x,y,z)
}"""

class ContainerRenderer:
    """
    """
    def render(self):
        """
        """
        kwargs = {'camera': self.camera, 'scene': self.scene,
                  'controls': [TrackballControls(controlling=self.camera)],
                  'width': self.width,
                  'height': self.height}
        return Renderer(**kwargs)

    def __init__(self, container, width=850, height=500):
        self.container = container
        self.width = width
        self.height = height
        self.pgeom = ParametricGeometry(func=func)
        print(self.pgeom)
        mat1 = LambertMaterial(color='green', side='FrontSide')
        mat2 = LambertMaterial(color='yellow', side='BackSide')
        print(mat1)
        print(mat2)
        self.surf = Mesh(geometry=self.pgeom, material=mat1)
        self.surf2 = Mesh(geometry=self.pgeom, masterial=mat2)
        self.scene = Scene(children=[self.surf, self.surf2, AmbientLight(color='#777777')])
        self.camera = PerspectiveCamera(position=[5, 5, 3], up=[0, 0, 1],
                                        children=[DirectionalLight(color='white',
                                                                   position=[3, 5, 1],
                                                                   intensity=0.6)])
    def _repr_html_(self):
        return self.render()
