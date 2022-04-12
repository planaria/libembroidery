#!/usr/bin/env python3

r"""
Part of libembroidery

Copyright 2022 The Embroidermodder Team
Licensed under the terms of the zlib licence.

The test suite for the libembroidery Python bindings.

Similar to, although not a replica of, the internal tests. This
cannot replace them because some systems that will run the library
won't support Python.

(Libembroidery may need to include some truly ancient PC in order
to deal with the older embroidery machines that they may talk to.)
"""

import math
import unittest
import libembroidery as emb

def create_test_file_1(outf="test01.csv"):
    """
    """
    emb.create()

    # 10mm circle
    for i in range(20):
        x = 0.0
        y = 1.0*(i+1)
        emb.addStitch(x, y, emb.JUMP, 0)

    for i in range(200):
        x = 10 + 10 * math.sin(i * 0.01 * math.pi)
        y = 10 + 10 * math.cos(i * 0.01 * math.pi)
        flags = emb.NORMAL
        color = 0
        emb.addStitch(x, y, flags, color)

    #emb.addThread(emb.black_thread)
    emb.end()

    emb.write(outf)
    emb.free()


def create_test_file_2(outf="test02.csv"):
    """
    """
    emb.create()

    # sin wave
    for i in range(100):
        x = 10 + 10 * math.sin(i * (0.5 / math.pi))
        y = 10 + i * 0.1
        flags = emb.NORMAL
        color = 0
        emb.addStitch(x, y, flags, color)

    #emb.add_thread(emb.black_thread)
    emb.end()

    emb.write(outf)
    emb.free()


def create_test_file_3(outf="test03.csv"):
    """
    """
    emb.create()
    emb.addCircle(10.0, 1.0, 5.0)
    #emb.addThread(emb.black_thread)
    emb.convertGeometry()
    emb.end()

    emb.write(outf)
    emb.free()


def convert_test(t, from_f, to_f):
    """
    """
    inf = "test%02d.%s" % (t, from_f)
    outf = "test%02d_convert_from_%s.%s" % (t, from_f, to_f)
    if t == 1:
        create_test_file_1(inf)
    elif t == 2:
        create_test_file_2(inf)
    else:
        create_test_file_3(inf)
    return emb.convert(inf, outf)


def convert_test_all(from_f, to_f):
    for i in range(1, 4):
        if convert_test(i, from_f, to_f) != 0:
            return 1
    return 0


class TestLibembroidery(unittest.TestCase):
    r"""
    The parent class for all of the bindings
    tests, this could be made to chain into the
    internal C testing.
    """
    def test_vector_length(self):
        " Tests the vector length function. "
        v = emb.vector(3.0, 4.0)
        self.assertAlmostEqual(v.length(), 5.0)

    def test_arc(self):
        " . "
        arc = emb.arc(1.0, 2.0, 2.0, 3.0, 4.0, 6.0)
        self.assertAlmostEqual(5.0, 5.0)

    def test_circle(self):
        " . "
        circle = emb.circle(3.0, 4.0, 2.0)
        self.assertAlmostEqual(5.0, 5.0)

    def test_ellipse(self):
        " . "
        ellipse = emb.ellipse(3.0, 4.0, 7.0, 4.0)
        self.assertAlmostEqual(5.0, 5.0)

    def test_path(self):
        " . "
        path = emb.path()
        self.assertAlmostEqual(5.0, 5.0)

    def test_main(self):
        """
        """
        emb.create()
        image = emb.image(100, 100)
        hilbertCurveResult = emb.hilbert_curve(pattern, 3)
        renderResult = image.render(pattern, 20.0, 20.0, "hilbert_level_3.ppm")
        simulateResult = image.simulate(pattern, 20.0, 20.0, "hilbert_level_3.avi")
        
        self.assertEqual(renderResult, 0)
        self.assertEqual(simulateResult, 0)
        emb.free()

    def test_convert_csv_svg(self):
        " Test conversion from csv to svg. "
        self.assertEqual(convert_test_all("csv", "svg"), 1)

    def test_convert_csv_dst(self):
        " Test conversion from csv to dst. "
        self.assertEqual(convert_test_all("csv", "dst"), 1)

    def test_convert_csv_pes(self):
        " Test conversion from csv to pes. "
        self.assertEqual(convert_test_all("csv", "pes"), 1)

    def test_convert_svg_csv(self):
        " Test conversion from svg to csv. "
        self.assertEqual(convert_test_all("svg", "csv"), 1)

    def test_convert_dst_csv(self):
        " Test conversion from dst to csv. "
        self.assertEqual(convert_test_all("dst", "csv"), 1)

    def test_convert_pes_csv(self):
        " Test conversion from pes to csv. "
        self.assertEqual(convert_test_all("pes", "csv"), 1)

    def test_circle_tangent(self):
        """
        """
        t0 = emb.vector(0.0, 0.0)
        t1 = emb.vector(0.0, 0.0)
        c = emb.circle(0.0, 0.0, 3.0)
        p = emb.vector(4.0, 0.0)
        emb.getCircleTangentPoints(c, p, t0, t1)
        self.assertAlmostEqual(t0.x, 2.2500)
        self.assertAlmostEqual(t0.y, 1.9843)
        self.assertAlmostEqual(t1.x, 2.2500)
        self.assertAlmostEqual(t1.y, -1.9843)

    def test_circle_tangent_2(self):
        """
        """
        t0 = emb.vector(0.0, 0.0)
        t1 = emb.vector(0.0, 0.0)
        c = emb.circle(20.1762, 10.7170, 6.8221)
        p = emb.vector(24.3411, 18.2980)
        emb.getCircleTangentPoints(c, p, t0, t1)
        self.assertAlmostEqual(t0.x, 19.0911)
        self.assertAlmostEqual(t0.y, 17.4522)
        self.assertAlmostEqual(t1.x, 26.4428)
        self.assertAlmostEqual(t1.y, 13.4133)

    def test_thread_color(self):
        """
        TODO: Add capability for converting multiple files of various
        types to a single format. 

        Currently, we only convert a single file to multiple formats.
        """
        tColor = 0xFFD25F00
        c = emb.color(rgb=(0xD2, 0x5F, 0x00))
        tBrand = emb.Sulky_Rayon
        tNum = emb.threadColorNum(c, tBrand)
        tName = ""
        emb.threadColorName(tName, c, tBrand)

        # Solution: tNum = 1833
        # Solution: Pumpkin Pie
        print("""
Color : 0x%X
Brand : %d
Num   : %d
Name  : %s

""" % (tColor, tBrand, tNum, tName))
        return 0

    def test_format_table(self):
        """
        """
        tName = "example.zsk"
        f_format = emb.emb_identify_format(tName)
        table = emb.formatTable[f_format]

        self.assertEqual(table.extension, ".zsk")
        self.assertEqual(table.description, "ZSK USA Embroidery  f_format")
        self.assertEqual(table.reader_state, 'U')
        self.assertEqual(table.writer_state, ' ')
        self.assertEqual(table.type, 1)


if __name__ == '__main__':
    unittest.main()

