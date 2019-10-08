from OpenGL.GL import *


class Shader(object):
    def __init__(self,programID,uniforms,name="unnamedShader",sourceFP = "HIDDEN"):
        self.programID = programID
        self.uniforms = uniforms
        self.name = name
        self.srcFP = sourceFP


class ModelData(object):
    def __init__(self,vao,vbuff,uvbuff,nbuff):
        self.vao = vao
        self.vbuff = vbuff
        self.uvbuff = uvbuff
        self.nbuff = nbuff

class Model(object):
    def __init__(self,md,x,y,z):
        pass