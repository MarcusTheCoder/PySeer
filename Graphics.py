from OpenGL.GL import *


class Shader(object):
    def __init__(self,programID,uniforms,name="unnamedShader",sourceFP = "HIDDEN"):
        self.programID = programID
        self.uniforms = uniforms
        self.name = name
        self.srcFP = sourceFP


class ModelData(object):
    def __init__(self,vao,vertBuff,eleBuff):
        self.vao = vao
        self.vertBuff = vertBuff
        self.eleBuff = eleBuff

class Model(object):
    def __init__(self,md,x,y,z):
        self.md = md
        self.modelMatrix = 