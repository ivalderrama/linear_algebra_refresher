from math import sqrt, acos, pi
from decimal import Decimal, getcontext

getcontext().prec = 30


class Vector:
    
    CANNOT_NORMALIZE_ZERO_VECTOR_MSG = 'Cannot normalize the zero vector'
    NO_UNIQUE_PARALLEL_COMPONENT_MSG = 'No Unique parallel component'
    NO_UNIQUE_ORTHOGONAL_COMPONENT_MSG = 'NO Unique Orthogonal component'

    def __init__(self, coordinates):
        try:
            if not coordinates:
                raise ValueError
            self.coordinates = tuple([Decimal(x) for x in coordinates])
            self.dimension = len(self.coordinates)

        except ValueError:
            raise ValueError('The coordinates must be nonempty')

        except TypeError:
            raise TypeError('The coordinates must be an iterable')

    def __str__(self):
        return 'Vector: {}'.format(self.coordinates)

    def __eq__(self, v):
        return self.coordinates == v.coordinates

    def magnitude(self):
        coordinates_squared = [x ** 2 for x in self.coordinates]
        # return sqrt(sum(coordinates_squared))
        return Decimal(sum(coordinates_squared)).sqrt()

    def normalised(self):
        try:
            magnitude = self.magnitude()
            return self.times_scalar(Decimal(1.0) / magnitude)

        except ZeroDivisionError:
            raise Exception('Cannot normalize the zero vector')

    def plus(self, v):
        # new_coordinates = [x + y for x, y in zip(self.coordinates, v.coordinates)]
        new_coordinates = []
        n = len(self.coordinates)
        for i in range(n):
            new_coordinates.append(self.coordinates[i] + v.coordinates[i])
        return Vector(new_coordinates)

    def minus(self, v):
        new_coordinates = [x - y for x, y in zip(self.coordinates, v.coordinates)]
        return Vector(new_coordinates)

    def times_scalar(self, c):
        new_coordinates = [Decimal(c) * x for x in self.coordinates]
        return Vector(new_coordinates)

    def dot(self, v):
        return sum([x * y for x, y in zip(self.coordinates, v.coordinates)])

    def angle_with(self, v, in_degrees=False):
        try:
            u1 = self.normalised()
            u2 = v.normalised()
            angle_in_radians = acos(u1.dot(u2))

            if in_degrees:
                degrees_per_radian = 180. / pi
                return angle_in_radians * degrees_per_radian
            else:
                return angle_in_radians

        except Exception as e:
            if str(e) == self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG:
                raise Exception('Cannot comput an angle with a zero vector')
            else:
                raise e
                
    def is_orthogonal_to(self, v, tolerance=1e-10):
        return abs(self.dot(v)) < tolerance

    def is_parallel_to(self, v):
        return self.is_zero() or v.is_zero() or self.angle_with(v) == 0 or self.angle_with(v) == pi

    def is_zero(self, tolerance=1e-10):
        return self.magnitude() < tolerance
    
    def component_parallel_to(self, basis):
        try:
            u = basis.normalised()
            weight = self.dot(u)
            return u.times_scalar(weight)
        
        except Exception as e:
            if str(e) == self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG:
                raise Exception(self.NO_UNIQUE_PARALLEL_COMPONENT_MSG)
            else:
                raise e
    
    def component_orthogonal_to(self, basis):
        try:
            projection = self.component_parallel_to(basis)
            return self.minus(projection)
        except Exception as e:
            if str(e) == self.NO_UNIQUE_PARALLEL_COMPONENT_MSG:
                raise Exception(self.NO_UNIQUE_ORTHOGONAL_COMPONENT_MSG)
            else:
                raise e
                
    def cross(self,v):
        try:
            x1,y1,z1 = self.coordinates
            x2,y2,z2 = v.coordinates
            new_coordinates = [y1*z2-y2*z1,-(x1*z2-x2*z1),x1*y2-x2*y1]
            return Vector(new_coordinates)
        
        except ValueError as e:
            msg = str(e)
            if msg == ('need more than 2 values to unpack'):
                self_make_R3 = Vector(self.coordinates + ('0',))
                v_make_R3 = Vector(v.coordinates + ('0',))
                return self_make_R3.cross(v_make_R3)
            
            elif(msg == 'too many values to unpack' or
                 msg == 'need more than 1 value to unpack'):
                raise Exception('Only defined in two dimension')
            else:
                raise e


    def area_of_parallelogram_with(self,v):
        cross_product = self.cross(v)
        return cross_product.magnitude()

    def area_of_triangle_with(self,v):
        return self.area_of_parallelogram_with(v)/Decimal('2.0')
