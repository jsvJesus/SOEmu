# Embedded file name: scripts/client/Victim.py
import BigWorld
from generic.victimdamager import GenericVictim

class Victim(GenericVictim):

    def attach_collider_box(self, box_name, node_name, body_zone, min_bounds, max_bounds):
        box = BigWorld.BoxAttachment()
        box.name = box_name
        box.minBounds = min_bounds
        box.maxBounds = max_bounds
        node = self.model.node(node_name)
        node.attach(box)
        self.skeletonCollider.addCollider(box)
        self.colliderNames[box_name] = body_zone
        self.collider_nodes[box_name] = (node_name, node)

    def add_collider(self):
        if getattr(self, 'skeletonCollider', None):
            self.skeletonCollider = None
        self.skeletonCollider = BigWorld.SkeletonCollider()
        self.colliderNames = {}
        self.collider_nodes = {}
        return

    def get_node_by_body_zone(self, body_zone):
        for box_name, box_body_zone in self.colliderNames.iteritems():
            if box_body_zone == body_zone:
                node_name, node = self.collider_nodes[box_name]
                return node

        return None