from introcs import assert_equals, assert_false, assert_true
import a1

p = a1.Point(3, 4)
l = a1.Line(0, 1, 0)
a1.findMirrorPoint(p, l)
assert_equals(-3.0, p.x)
assert_equals(4.0, p.y)

p = a1.Point(1, -1)
l = a1.Line(1, -1, 0)
a1.findMirrorPoint(p, l)
assert_equals(-1.0, p.x)
assert_equals(1.0, p.y)

p1 = a1.Point(3, 4)
p2 = a1.Point(2, 0)
l = a1.Line(1, -1, 0)
assert_true(a1.checkSides(p1, p2, l, l))

p1 = a1.Point(0, 0)
p2 = a1.Point(2, 0)
l1 = a1.Line(1, -1, 0)
l2 = a1.Line(0, 1, 4)
assert_true(a1.checkSides(p1, p2, l1, l2))

c1 = a1.Circle(0, 0, 5)
c2 = a1.Circle(10, 0, 5)
assert_true(a1.checkIntersection(c1, c2))

c1 = a1.Circle(0, 0, 5)
c2 = a1.Circle(10, 0, 20)
assert_false(a1.checkIntersection(c1, c2))

c1 = a1.Circle(0, 0, 5)
c2 = a1.Circle(0, 0, 5)
assert_true(a1.checkIntersection(c1, c2))

print('done')
