
# OLd angle getter, does not work since arccos is 0,pi interval
# def get_angle_of_force(self, other_object, deg=None):
#     # force = self.get_gravity(other_object)
#     relative_x = self.pos[0] - other_object.pos[0]
#     dist = self.distance(other_object)
#     ang = np.arccos(relative_x/dist)
#
#     if not deg:
#         return ang
#
#     return ang * (180/np.pi)

#
# def get_angle(self, vector1, vector2=None, deg=False):
#     """
#     Possibly replace this with simply represnting the vectors as complex numbers and using np.angle
#     """
#     if vector2=None:
#         vector2 = self.pos[0] # x vector
#
#     ang = np.arccos((self.pos @ other_objects.pos)/(np.linalg.norm(self.pos)*np.linalg.norm(other_objects.pos)))
#     if not deg:
#         return ang
#     return ang * np.pi * 180