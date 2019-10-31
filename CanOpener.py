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
def readOBJFile(filepath,printComments=False):
    ''' Will read an object .OBJ file and return
    information about the vertex positions, UV coords,
    normals, and elements (Face-vertex indices)
    '''
    f = open(filepath)
    if f is None:
        return None

    s = ""
    v = []
    vt = []
    vn = []
    vertsComplete = {} # 5/1/1 : [vert data]
    vertCounter = 0
    indices = []
    while s != "END":
        s = f.readline()
        if not s:
            s = "END"
            continue
        # Process the first element
        splits = s.split(" ")
        if len(splits >= 3):
            # This is one of the valid tags
            if splits[0] == "v":
                v.append([float(splits[1]),float(splits[2]),float(splits[3])])
            elif splits[0] == "vt":
                vt.append([float(splits[1]),float(splits[2])])
            elif splits[0] == "vn":
                vn.append([float(splits[1]),float(splits[2]),float(splits[3])])
            elif splits[0] == "f":                
                for i in range(1,4):
                    if not splits[i] in vertsComplete.keys():
                        subs = splits[i].split("/")
                        vertsComplete[splits[i]] = (vertCounter,v[int(subs[0])],vt[int(subs[1])],vn[int(subs[2])])
                        vertCounter += 1                    
                    indices.append(vertsComplete[splits[i]][0])
            else:
                # Unknown command
                continue
        else:
            if splits[0].startswith("#") and printComments:
                # We have a comment, print it out
                print(s)
    
    return [vertsComplete,indices]

def openModelData(filepath):
    
    objData = readOBJFile(filepath)
    if objData is None:
        raise Exception("openModelData() [Error]: Filepath invalid or invalid format")
    
    vao = glGenVertexArrays(1)
    glBindVertexArray(vao)

    vertBuff = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER,vertBuff)
    totalSize = len(objData[1]) * (3 * sizeof(float))
    l = []
    for vert in objData[1]:
        # Skip the numbering, just raw geometry
        l.append(vert[1])
        l.append(vert[2])
        l.append(vert[3])
    npArr = numpy.array(l)
    glBufferData(GL_ARRAY_BUFFER,totalSize,npArr,GL_STATIC_DRAW)
    
    glBindBuffer(GL_ARRAY_BUFFER,0)
    glBindVertexArray(0)

    return ModelData(vao,vbuff,uvbuff,normbuff)
    
def createModel(modelDataDict,mname,shaderDict,sname):
    pass

