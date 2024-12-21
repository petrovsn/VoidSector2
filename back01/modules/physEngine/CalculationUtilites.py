import numpy as np
import math
from modules.physEngine.WorldPhysConstants import WorldPhysConstants

class CalculationUtilites:
    def get_projections(F, vector):
        dx = vector[0]
        dy = vector[1]
        r = np.linalg.norm(vector)
        if r == 0:
            return np.array([0, 0], dtype=np.float32)
        Fx = F*dx/r
        Fy = F*dy/r
        return np.array([Fx, Fy], dtype=np.float32)

    def get_stable_velocity(pos, hbody):
        #hbody = hBodies().get_gravity_affected_body(pos)
        if not hbody:
            return np.array([0, 0])
        mass = hbody.mass
        radius = pos-hbody.position
        radius_scalar = max(1, np.linalg.norm(radius))
        tangent = CalculationUtilites.rotate_vector(radius, 90)
        V_scalar = math.sqrt(WorldPhysConstants().get_Gconst()*mass/radius_scalar)
        V_vector = CalculationUtilites.get_projections(V_scalar, tangent)
        #if np.linalg.norm(vec) != 0:
        #    cos_alpha = CalculationUtilites.get_cosangle_between(V_vector, vec)
        #    if cos_alpha < 0:
        #        V_vector = V_vector*-1
        return V_vector

    def rotate_vecto_rad(vector, angler):
        x = vector[0]
        y = vector[1]
        newx = x*math.cos(angler) - y*math.sin(angler)
        newy = x*math.sin(angler) + y*math.cos(angler)
        return np.array([newx, newy])

    def rotate_vector(vector, angle):
        x = vector[0]
        y = vector[1]
        angler = angle*math.pi/180
        newx = x*math.cos(angler) - y*math.sin(angler)
        newy = x*math.sin(angler) + y*math.cos(angler)
        return np.array([newx, newy])

    def get_cosangle_between(vector1, vector2):
        cos_alpha = np.dot(vector1, vector2) / \
            (np.linalg.norm(vector1)*np.linalg.norm(vector2))
        return cos_alpha

    def get_radangle_between(vector1, vector2):
        cos_alpha = CalculationUtilites.get_cosangle_between(vector1, vector2)
        alpha_rad = np.arccos(cos_alpha)
        vector3_ort = CalculationUtilites.rotate_vector(vector2, 90)
        cos_alpha_ort = CalculationUtilites.get_cosangle_between(
            vector1, vector3_ort)
        if cos_alpha_ort < 0:
            alpha_rad = -alpha_rad

        return alpha_rad

    def get_abs_angle_degrees_from_zero(vector1):
        vector2 = np.array([1, 0])
        cos_alpha = CalculationUtilites.get_cosangle_between(vector1, vector2)
        alpha_rad = np.arccos(cos_alpha)
        vector3_ort = CalculationUtilites.rotate_vector(vector2, 90)
        cos_alpha_ort = CalculationUtilites.get_cosangle_between(
            vector1, vector3_ort)
        if cos_alpha_ort < 0:
            alpha_rad = 3.14*2-alpha_rad

        return alpha_rad*180/3.14

    def degress2rads(value):
        return value*3.14/180

    def is_in_sector(value, arc1, arc2):
        arc1 = (arc1+360*2) % 360
        arc2 = (arc2+360*2) % 360
        value = (value+360*2) % 360
        if arc1 < arc2:
            arc2 = arc2-360
        if arc1 < value:
            value = value-360
        return arc2 < value < arc1

    def get_intersection_for_2_circles(pos1, rad1, pos2, rad2):
        # https://algolist.ru/maths/geom/intersect/circlecircle2d.php#:~:text=%2D2ax%2D2by%20%3D%20R2,%2D%20a2%20%2D%20b2.&text=ax%2Bby%3DC%2C%20%D0%B3%D0%B4%D0%B5,%D0%A1%20%2D%20%D0%BD%D0%BE%D0%B2%D0%BE%D0%B5%20%D0%BE%D0%B1%D0%BE%D0%B7%D0%BD%D0%B0%D1%87%D0%B5%D0%BD%D0%B8%D0%B5%20%D0%B2%D1%8B%D1%80%D0%B0%D0%B6%D0%B5%D0%BD%D0%B8%D1%8F%20%D1%81%D0%BF%D1%80%D0%B0%D0%B2%D0%B0.
        d = np.linalg.norm(pos1-pos2)
        if d == 0:
            return None
        a = (rad1**2 - rad2**2 + d**2)/(2*d)
        discr = rad1**2 - a**2
        if discr < 0:
            return None
        h = math.sqrt(discr)
        pos3 = pos1+a*(pos2-pos1)/d
        p4_1_x = pos3[0]+h*(pos2[1]-pos1[1])/d
        p4_1_y = pos3[1]-h*(pos2[0]-pos1[0])/d

        p4_2_x = pos3[0]-h*(pos2[1]-pos1[1])/d
        p4_2_y = pos3[1]+h*(pos2[0]-pos1[0])/d

        return np.array([p4_1_x, p4_1_y]), np.array([p4_2_x, p4_2_y])
