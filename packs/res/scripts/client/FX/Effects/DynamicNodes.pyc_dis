# Embedded file name: scripts/client/FX/Effects/DynamicNodes.py
__author__ = 'monitorius'
import BigWorld
from FX.Joints import Node, LightSource
NODE_DEPENDENT_JOINTS = (Node.Node, LightSource.LightSource)
KEYWORD_DYNAMIC = '__dynamic__'

class iDynamicNodes:
    """ Interface for joints, allowing nodes changing in runtime.
    
            __dynamic__ keyword is used to mark what nodes should be changed by set_node_name
    
            Example:
            <Joint> particles
                    <Node> __dynamic__ </Node>
            </Joint>
            <Joint> light
                    <LightSource>  __dynamic__ </LightSource>
            </Joint>
    """

    def __init__(self):
        pass

    def set_node_name(self, name, joint_name = None):
        if joint_name is None:
            for joint in self.joints.values():
                if isinstance(joint, NODE_DEPENDENT_JOINTS) and joint.nodeName == KEYWORD_DYNAMIC:
                    joint.nodeName = name

        else:
            for j_name, joint in self.joints.items():
                if j_name == joint_name and isinstance(joint, NODE_DEPENDENT_JOINTS) and joint.nodeName == KEYWORD_DYNAMIC:
                    joint.set_node_name(name)
                    return

        return