# coding:utf-8
# meow

from decimal import Decimal, getcontext
from math import sqrt, acos, pi

getcontext().prec = 30

class Vector(object):
    def __init__(self, coordinates):

        self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG = 'cannot normalize the zero vector'
        self.NO_UNIQUE_PARALLEL_COMPONENT_MSG = 'no unique parallel component'
        self.ONLY_DEFINED_IN_TWO_THREE_DIMS_MSG = 'only defined in 2 and 3 dimensions'
        
        try:
            if not coordinates:
                raise ValueError
            self.coordinates = tuple(map(Decimal, coordinates))
            self.dimension = len(coordinates)

        except ValueError:
            raise ValueError('The coordinates must be nonempty')

        except TypeError:
            raise TypeError('The coordinates must be an iterable')

    def __iter__(self):
        self.current = -1
        return self

    def next(self):
        self.current += 1
        if self.current >= self.dimension:
            raise StopIteration
        else:
            return self.coordinates[self.current]

    def __getitem__(self, key):
        if key >= self.dimension:
            raise IndexError
        else:
            return self.coordinates[key]

    def area_of_triangle_with(self, v):
        return self.area_of_parallelogram_with(v)/Decimal('2.0')

    def area_of_parallelogram_with(self, v):
        cross_product = self.cross(v)
        return cross_product.magnitude()

    def cross(self, v):
        try:
            x_1, y_1, z_1 = self.coordinates
            x_2, y_2, z_2 = v.coordinates
            new_coordinates = [y_1*z_2 - y_2*z_1,
                               -(x_1*z_2 - x_2*z_1),
                               x_1*y_2 - x_2*y_1]
            return Vector(new_coordinates)

        except ValueError as e:
            msg = str(e)
            if msg == 'need more than two values to unpack':
                self_embedded_in_R3 = Vector(self.coordinates + ('0',))
                v_embedded_in_R3 = Vector(v.coordinates + ('0',))
                return self_embedded_in_R3.cross(v_embedded_in_R3)
            elif msg == 'too many values to unpack' or msg == 'need more than 1 value to unpack':
                raise Exception(self.ONLY_DEFINED_IN_TWO_THREE_DIMS_MSG)
            else:
                raise e

    def component_orthogonal_to(self, basis):
        try:
            projection = self.component_parallel_to(basis)
            return self.minus(projection)

        except Exception as e:
            if str(e) == self.NO_UNIQUE_PARALLEL_COMPONENT_MSG:
                raise Exception(self.NO_UNIQUE_PARALLEL_COMPONENT_MSG)
            else:
                raise e

    def component_parallel_to(self, basis):
        try:
            u = basis.normalized()
            weight = self.dot(u)
            return u.times_scalar(weight)

        except Exception as e:
            if str(e) == self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG:
                raise Exception(self.NO_UNIQUE_PARALLEL_COMPONENT_MSG)
            else:
                raise e

    # 判断正交
    def is_orthogonal_to(self, v, tolerance=1e-10):
        return abs(self.dot(v)) < tolerance

    def is_zero(self, tolerance=1e-10):
        return self.magnitude() < tolerance

    # 判断平行
    def is_paralle_to(self, v):
        return (self.is_zero() or
                v.is_zero() or
                self.angle_with(v) == 0 or 
                self.angle_with(v) == pi)

    # 点乘
    def dot(self, v):
        return sum([x * y for x, y in zip(self.coordinates, v.coordinates)])

    # 夹角
    def angle_with(self, v, in_degrees=False):
        try:
            u1 = self.normalized()
            u2 = v.normalized()
            d = u1.dot(u2)
            angle_in_radians = acos(d)

            if in_degrees:
                degrees_per_radian = 180. / pi
                return angle_in_radians * degrees_per_radian
            else:
                return angle_in_radians

        except Exception as e:
            if str(e) == self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG:
                raise Exception('Cannot computer an angel with the zero vector')
            else:
                raise e

    # 向量大小
    def magnitude(self):
        coordinates_squared = [x ** 2 for x in self.coordinates]
        return Decimal.sqrt(sum(coordinates_squared))
    
    # 向量方向
    def normalized(self):
        try:
            magnitude = self.magnitude()
            # return self.times_scalar(Decimal('1.0')/magnitude)
            return self.times_scalar(Decimal('1.0') / Decimal(magnitude))

        except ZeroDivisionError:
            raise Exception('Cannot normalize the zero vector')

    # 向量加法
    def plus(self, v):
        new_coordinates = [x + y for x, y in zip(self.coordinates, v.coordinates)]
        return Vector(new_coordinates)
    
    # 向量减法
    def minus(self, v):
        new_coordinates = [x - y for x, y in zip(self.coordinates, v.coordinates)]
        return Vector(new_coordinates)
    
    # 向量与标量相乘
    def times_scalar(self, c):
        new_coordinates = [Decimal(c) * x for x in self.coordinates]
        # new_coordinates = [c * x for x in self.coordinates]
        return Vector(new_coordinates)

    def __str__(self):
        return 'Vector: {}'.format(self.coordinates)

    def __eq__(self, v):
        return self.coordinates == v.coordinates


# # 测试用例
# print '测试用例开始'
# my_vector = Vector(['1','2','3'])
# print my_vector
# print '\n'


# print '4.加减和标量乘法'
# v = Vector(['8.218', '-9.341'])
# w = Vector(['-1.129', '2.111'])
# print v.plus(w)

# v = Vector(['7.119', '8.125'])
# w = Vector(['-8.223', '0.878'])
# print v.minus(w)

# v = Vector(['1.671', '-1.012', '-0.318'])
# c = 7.41
# print v.times_scalar(c)

# print '''
#       answer:
#       Vector:[7.089,-7.2299]
#       Vector:[15.342,7.337]
#       Vector:[12.38211,-7.49892,-2.35638]

#       '''


# print '6.大小和方向'

# v = Vector(['-0.221', '7.437'])
# print v.magnitude()

# v = Vector(['8.813', '-1.331', '-6.247'])
# print v.magnitude()

# v = Vector(['5.581', '-2.136'])
# print v.normalized()

# v = Vector(['1.996', '3.108', '-4.554'])
# print v.normalized()

# print '''
#       answer:
#       7.44028292473
#       10.8841875673
#       Vector:[0.9339352140866403 -0.35744232526233]
#       Vector: [0.3404012959433014, 0.5300437012984873, -0.7766470449528029]

#       '''

# print '8.点积和夹角'
# v = Vector(['7.887', '4.138'])
# w = Vector(['-8.802', '6.776'])
# print v.dot(w)

# v = Vector(['-5.955', '-4.904', '-1.874'])
# w = Vector(['-4.496', '-8.775', '7.103'])
# print v.dot(w)

# v = Vector(['3.183', '-7.627'])
# w = Vector(['-2.668', '5.319'])
# print v.angle_with(w)

# v = Vector(['7.35', '0.221', '5.188'])
# w = Vector(['2.751', '8.259', '3.985'])
# print v.angle_with(w, in_degrees=True)

# print '''
#       -41.382
#       56.397
#       3.072rad
#       60.276rad
#       '''

# print '10.平行或正交'
# print 'first pair...'
# v = Vector(['-7.579', '-7.88'])
# w = Vector(['22.737', '23.64'])
# print 'is parallel:', v.is_paralle_to(w)
# print 'is orthogonal:', v.is_orthogonal_to(w)

# print 'second pair...'
# v = Vector(['-2.029', '9.97', '4.172'])
# w = Vector(['-9.231', '-6.639', '-7.245'])
# print 'is parallel:', v.is_paralle_to(w)
# print 'is orthogonal:', v.is_orthogonal_to(w)

# print 'third pair'
# v = Vector(['-2.328', '-7.284', '-1.214'])
# w = Vector(['-1.821', '1.072', '-2.94'])
# print 'is parallel:', v.is_paralle_to(w)
# print 'is orthogonal:', v.is_orthogonal_to(w)

# print 'fourth pair...'
# v = Vector(['2.118', '4.827'])
# w = Vector(['0', '0'])
# print 'is parallel:', v.is_paralle_to(w)
# print 'is orthogonal:', v.is_orthogonal_to(w)

# print '''
#       first pair...
#       is parallel: True
#       is orthogonal: False
#       first pair...
#       is parallel: False
#       is orthogonal: False
#       first pair...
#       is parallel: False
#       is orthogonal: True
#       first pair...
#       is parallel: True
#       is orthogonal: True
#       '''

print '12.向量投影'
print '#1'
v = Vector(['3.039', '1.879'])
w = Vector(['0.825', '2.036'])
print v.component_parallel_to(w)


# print '#2'
# v = Vector(['-9.88', '-3.264', '-8.158'])
# w = Vector(['-2.155', '-9.353', '-9.473'])
# print v.component_orthogonal_to(w)

# print '#3'
# v = Vector(['3.009', '-6.172', '3.692', '-2.51'])
# w = Vector(['6.404', '-9.144', '2.759', '8.718'])
# print v.component_parallel_to(w)
# print v.component_orthogonal_to(w)

# print '''
#       answer:
#       Vector:[1.0826, 2.6717]
#       Vector:[-8.3500, 3.3760. -1.4337]
#       Vector:[1.9685, -2.8107, 0.8480, 2.6798]
#       Vector:[1.0404, -3.3612, 2.8439, -5.1898]

#       '''

# print '14.向量积'
# v = Vector(['8.462', '7.893', '-8.187'])
# w = Vector(['6.984', '-5.975', '4.778'])
# print '#1:', v.cross(w)


# v = Vector(['-8.987', '-9.838', '5.031'])
# w = Vector(['-4.268', '-1.861', '-8.866'])
# print '#2:', v.area_of_parallelogram_with(w)

# v = Vector(['1.5', '9.547', '3.691'])
# w = Vector(['-6.007', '0.124', '5.772'])
# print '#3:', v.area_of_triangle_with(w)

# print '''
#       answer:
#       #1: Vector:[-11.204571, -97.609444, -105.685162]
#       #2: 142.1222
#       #3: 42.5649
#       '''

# print '测试用例结束'






