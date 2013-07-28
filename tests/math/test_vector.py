import unittest
import random

from toast.math.vector import Vector2D

class TestVectorSpaceAxioms(unittest.TestCase):
    def setUp(self):
        self.u = Vector2D(random.random(), random.random())
        self.v = Vector2D(random.random(), random.random())
        self.w = Vector2D(random.random(), random.random())
    
    def test_associativity(self):
        result1 = self.u + (self.v + self.w)
        result2 = (self.u + self.v) + self.w
        self.assertAlmostEqual(result1, result2, 5, "failed associativity")
    
    def test_commutativity(self):
        result1 = self.u + self.v
        result2 = self.v + self.u
        self.assertAlmostEqual(result1, result2, 5, "failed commutativity")
    
    def test_identity_element_addition(self):
        result1 = self.v + Vector2D.Zero()
        self.assertEqual(self.v, result1, "failed identity element of addition")
    
    def test_additive_inverse(self):
        result1 = self.v + -self.v
        self.assertEqual(result1, Vector2D.Zero(), "failed additive inverse")
    
    def test_distributivity_scalar_multiplication_vector_addition(self):
        a = random.random()
        result1 = a * (self.u + self.v)
        result2 = (a * self.u) + (a * self.v)
        self.assertAlmostEqual(result1, result2, 5, "failed distributivity of scalar multiplication with vector addition")
        
    def test_distributivity_scalar_multiplication_field_addition(self):
        a = random.random()
        b = random.random()
        result1 = (a + b) * self.v
        result2 = (a * self.v) + (b * self.v)
        self.assertAlmostEqual(result1, result2, 5, "failed distributivity of scalar multiplication with field addition")
    
    def test_multiplicative_compatability(self):
        a = random.random()
        b = random.random()
        result1 = a * (b * self.v)
        result2 = (a * b) * self.v
        self.assertAlmostEqual(result1, result2, 5, "failed multiplication compatability")
    
    def test_identity_element_scalar_multiplication(self):
        self.assertEqual(self.v, self.v * 1, "failed identity element of scalar multiplication")
        
class TestVectorMethods(unittest.TestCase):
    def setUp(self):
        self.u = Vector2D(random.random(), random.random())
        self.v = Vector2D(random.random(), random.random())
        
    def test_sequence_length(self):
        self.assertEqual(len(self.v), 2, "failed incorrect sequence length")
        
    def test_get_set_index(self):
        self.v[0] = 0
        self.v[1] = 42
        
        self.assertEqual(self.v[0], 0, "failed to correctly retrieve the first element")
        self.assertEqual(self.v[1], 42, "failed to correctly retrieve the second element")
        
    def test_vector_equality(self):
        w = Vector2D(self.v[0], self.v[1])
        self.assertEqual(self.v, w, "failed vector equality")
        
    def test_vector_inequality(self):
        w = -self.v
        self.assertNotEqual(self.v, w, "failed vector inequality")
        
    def test_vector_dot_product(self):
        i = Vector2D(1, 0)
        j = Vector2D(0, 1)
        self.assertEqual(i.dot(j), 0, "failed dot product")
        self.assertEqual(i.dot(i), 1, "failed dot product")
        
    def test_vector_magnitude(self):
        i = Vector2D(1, 0)
        self.assertEqual(i.magnitude, 1, "failed incorrect magnitude")
        
    def test_vector_magnitude_squared(self):
        i = Vector2D(2, 0)
        self.assertEqual(i.magnitude_squared, 4, "failed incorrect magnitude squared")
        
    def test_vector_normalized(self):
        n = self.u.normalized()
        m = self.u.magnitude
        self.assertAlmostEqual(n.magnitude, 1, 5, "failed to normalize vector")
        self.assertAlmostEqual(n * m, self.u, 5,  "failed to normalize vector")
        
    def test_vector_get_angle(self):
        i = Vector2D(1, 0)
        j = Vector2D(0, 1)
        self.assertEqual(i.angle, 0, "failed to get angle")
        self.assertEqual(j.angle, 90, "failed to get angle")
        self.assertEqual((-i).angle, 180, "failed to get angle")
        self.assertEqual((-j).angle, 270, "failed to get angle")
        
    def test_vector_set_angle(self):
        i = Vector2D(1.0, 0)
        j = Vector2D(0, 1.0)
        a = random.random() * 360.0
        k = Vector2D.from_angle(a)
        self.assertAlmostEqual(Vector2D.from_angle(0), i, 5, "failed to set angle")
        self.assertAlmostEqual(Vector2D.from_angle(90.0), j, 5, "failed to set angle")
        self.assertAlmostEqual(Vector2D.from_angle(180.0), -i, 5, "failed to set angle")
        self.assertAlmostEqual(Vector2D.from_angle(270.0), -j, 5, "failed to set angle")
        self.assertAlmostEqual(k.angle, a, 5, "failed to set angle")
    
if __name__ == "__main__":
    unittest.main()