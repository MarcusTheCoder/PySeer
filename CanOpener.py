from Graphics import *
from OpenGL.GL import *
import xml.etree.ElementTree as ET
import numpy
import pywavefront


def openShader(filepath):
    ''' 
    Will open a shader .xml file and return the Shader object

    filepath [string]: Filepath of the shader file

    Returns [Shader]: A shader object
    '''
    def getEquivType(stageType):
        if stageType == "vertex_shader":
            return GL_VERTEX_SHADER
        elif stageType == "fragment_shader":
            return GL_FRAGMENT_SHADER
        else:
            return None
    tree = ET.parse(filepath)
    root = tree.getroot()
    
    shaderName = root.tag
    
    prog_id = glCreateProgram()
    uniforms = {} # Should be a name [string] as key and an integer as value
    stages = []
    for child in root:
        if child.tag == "stage":            
            shadd = glCreateShader(getEquivType(child.attrib["type"]))
            content = str(child.text).strip()
            glShaderSource(shadd,content)
            glCompileShader(shadd)
            
            llen = glGetShaderiv(shadd,GL_INFO_LOG_LENGTH,None)
            if llen > 0:           
                print(glGetShaderInfoLog(shadd))
            stages.append(shadd)
        elif child.tag == "uniforms":
            ulist = str(child.text).strip().split(";")
            for e in ulist:
                uniforms[e] = -1
            pass
    for stage in stages:
        glAttachShader(prog_id,stage)
    glLinkProgram(prog_id)
    
    llen = glGetProgramiv(prog_id,GL_INFO_LOG_LENGTH,None)
    if llen > 0:
        print(glGetProgramInfoLog(shadd))

    return Shader(prog_id,uniforms,shaderName,filepath)
    
def openModelData(filepath):
    scene = pywavefront.Wavefront(filepath)
    print(scene)

    #TODO: Fix importing so that arrays go into vao
    
    vao = glGenVertexArrays(1)
    glBindVertexArray(vao)
    vbuff = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER,vbuff)
    #glBufferData(GL_ARRAY_BUFFER, <insert array of data here>)
    #glVertexAttribPointer()
    uvbuff = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER,uvbuff)
    #glBufferData(GL_ARRAY_BUFFER, <insert array of data here>)
    #glVertexAttribPointer()
    normbuff = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER,normbuff)
    #glBufferData(GL_ARRAY_BUFFER, <insert array of data here>)
    #glVertexAttribPointer()

    glBindBuffer(GL_ARRAY_BUFFER,0)
    glBindVertexArray(0)

    return ModelData(vao,vbuff,uvbuff,normbuff)
    
def createModel(modelDataDict,name,shaderDict,name):


