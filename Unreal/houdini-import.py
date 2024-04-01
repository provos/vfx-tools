# (c) 2023 Niels Provos
import hou
import pickle

def applyValues(node, data, negate=False):
    node.deleteAllKeyframes()

    for t, v in data:
        curKey = hou.Keyframe()
        curKey.setFrame(t + 1)
        curKey.setValue(-v if negate else v)
        node.setKeyframe(curKey)

with open('E:/UnrealEngine/Assets/Transform/translation.pkl', 'rb') as f:
  translation = pickle.load(f)
  
node = hou.parm("/obj/Mesh_FBX/Mesh/transform_test/tx")
applyValues(node, translation[0], negate=False)

node = hou.parm("/obj/Mesh_FBX/Mesh/transform_test/ty")
applyValues(node, translation[1])
  
node = hou.parm("/obj/Mesh_FBX/Mesh/transform_test/tz")
applyValues(node, translation[2], negate=False)

with open('E:/UnrealEngine/Assets/Transform/rotation.pkl', 'rb') as f:
  rotation = pickle.load(f)
  
node = hou.parm("/obj/Mesh_FBX/Mesh/transform_test/rx")
applyValues(node, rotation[0])

node = hou.parm("/obj/Mesh_FBX/Mesh/transform_test/ry")
applyValues(node, rotation[1], Negate=True)
  
node = hou.parm("/obj/Mesh_FBX/Mesh/transform_test/rz")
applyValues(node, rotation[2])