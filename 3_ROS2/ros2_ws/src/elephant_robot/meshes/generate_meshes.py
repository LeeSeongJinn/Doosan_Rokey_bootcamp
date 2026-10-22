#!/usr/bin/env python3
"""Procedural STL mesh generator for the elephant robot.

Every organic part of the elephant is generated from a swept cross-section
profile so the result is a smooth, continuous surface instead of a stack of
boxes.  Run this script to regenerate the meshes:

    python3 src/elephant_robot/meshes/generate_meshes.py

All dimensions are in metres and match the URDF.
"""

import os
import struct

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))


# --------------------------------------------------------------------------
# STL output
# --------------------------------------------------------------------------
def write_stl(path, verts, faces, mirror_y=False):
    """Write a binary STL file.  verts: (N,3) float, faces: (M,3) int."""
    if mirror_y:
        verts = verts.copy()
        verts[:, 1] *= -1.0
        faces = faces[:, ::-1].copy()
    tris = verts[faces]
    normals = np.cross(tris[:, 1] - tris[:, 0], tris[:, 2] - tris[:, 0])
    norms = np.linalg.norm(normals, axis=1, keepdims=True)
    norms[norms < 1e-12] = 1.0
    normals /= norms

    with open(path, "wb") as fh:
        fh.write(b"elephant robot mesh".ljust(80, b"\0"))
        fh.write(struct.pack("<I", len(faces)))
        for i in range(len(faces)):
            n = normals[i]
            fh.write(struct.pack("<3f", *n))
            for k in range(3):
                v = tris[i, k]
                fh.write(struct.pack("<3f", v[0], v[1], v[2]))
            fh.write(struct.pack("<H", 0))
    return len(faces)


# --------------------------------------------------------------------------
# Cross-section helpers
# --------------------------------------------------------------------------
def superellipse(theta, r_a, r_b, n):
    """Superellipse point.  n = 2 -> ellipse, n -> 4 -> rounded rectangle."""
    c = np.cos(theta)
    s = np.sin(theta)
    e = 2.0 / n
    a = r_a * np.sign(c) * np.abs(c) ** e
    b = r_b * np.sign(s) * np.abs(s) ** e
    return a, b


def sweep(profiles, n_sides=64, cap_start=True, cap_end=True):
    """Sweep elliptical cross sections along an arbitrary centre line.

    profiles: list of dicts with
        center : (3,) centre of the cross section
        u, v   : (3,) unit vectors spanning the cross-section plane
        ru, rv : half sizes along u and v
        n      : superellipse exponent
    """
    verts = []
    rings = []

    for p in profiles:
        theta = np.linspace(0.0, 2.0 * np.pi, n_sides, endpoint=False)
        a, b = superellipse(theta, p["ru"], p["rv"], p.get("n", 2.0))
        a = a - p.get("u_off", 0.0)
        b = b - p.get("v_off", 0.0)
        c = np.asarray(p["center"], dtype=float)
        u = np.asarray(p["u"], dtype=float)
        v = np.asarray(p["v"], dtype=float)
        ring = c[None, :] + a[:, None] * u[None, :] + b[:, None] * v[None, :]
        rings.append(ring)

    for ring in rings:
        verts.append(ring)
    verts = np.concatenate(verts, axis=0)

    faces = []
    for i in range(len(rings) - 1):
        a0 = i * n_sides
        b0 = (i + 1) * n_sides
        for k in range(n_sides):
            k2 = (k + 1) % n_sides
            faces.append([a0 + k, a0 + k2, b0 + k2])
            faces.append([a0 + k, b0 + k2, b0 + k])

    if cap_start:
        c0 = verts[[0]].mean(axis=0)
        ci = len(verts)
        verts = np.vstack([verts, c0])
        for k in range(n_sides):
            k2 = (k + 1) % n_sides
            faces.append([ci, k2, k])
    if cap_end:
        last = (len(rings) - 1) * n_sides
        c1 = verts[last:last + n_sides].mean(axis=0)
        ci = len(verts)
        verts = np.vstack([verts, c1])
        for k in range(n_sides):
            k2 = (k + 1) % n_sides
            faces.append([ci, last + k, last + k2])

    return verts, np.asarray(faces, dtype=int)


def profile_along_x(sections, n_sides=64):
    """sections: (x, ru_halfwidth_y, rv_halfheight_z, z_center, n_exponent)."""
    profiles = []
    for x, ru, rv, zc, n in sections:
        profiles.append(
            {
                "center": (x, 0.0, zc),
                "u": (0.0, 1.0, 0.0),
                "v": (0.0, 0.0, 1.0),
                "ru": ru,
                "rv": rv,
                "n": n,
            }
        )
    return sweep(profiles, n_sides=n_sides)


def profile_along_z(sections, n_sides=48, plane="yz"):
    """sections: (z, ru, rv, x_center, y_center, n_exponent)."""
    profiles = []
    for z, ru, rv, xc, yc, n in sections:
        if plane == "yz":
            profiles.append(
                {
                    "center": (xc, yc, z),
                    "u": (0.0, 1.0, 0.0),
                    "v": (1.0, 0.0, 0.0),
                    "ru": ru,
                    "rv": rv,
                    "n": n,
                }
            )
        else:  # plane == "xy"  (thickness along z)
            profiles.append(
                {
                    "center": (xc, yc, z),
                    "u": (1.0, 0.0, 0.0),
                    "v": (0.0, 1.0, 0.0),
                    "ru": ru,
                    "rv": rv,
                    "n": n,
                }
            )
    return sweep(profiles, n_sides=n_sides)


# --------------------------------------------------------------------------
# Part builders
# --------------------------------------------------------------------------
def build_body():
    """Torso: rounded barrel, high shoulder dome, sloping rump."""
    sections = [
        (-0.720, 0.020, 0.020, 1.020, 2.0),
        (-0.706, 0.090, 0.095, 1.020, 2.2),
        (-0.685, 0.160, 0.170, 1.020, 2.4),
        (-0.650, 0.225, 0.235, 1.021, 2.6),
        (-0.595, 0.272, 0.280, 1.024, 2.7),
        (-0.520, 0.305, 0.308, 1.031, 2.7),
        (-0.420, 0.324, 0.322, 1.041, 2.8),
        (-0.300, 0.334, 0.330, 1.052, 2.8),
        (-0.160, 0.339, 0.338, 1.062, 2.8),
        (-0.020, 0.340, 0.350, 1.070, 2.8),
        (0.110, 0.337, 0.366, 1.074, 2.8),
        (0.230, 0.330, 0.378, 1.074, 2.8),
        (0.330, 0.318, 0.384, 1.070, 2.8),
        (0.420, 0.300, 0.372, 1.062, 2.8),
        (0.500, 0.276, 0.348, 1.050, 2.7),
        (0.565, 0.240, 0.312, 1.032, 2.6),
        (0.620, 0.192, 0.264, 1.008, 2.5),
        (0.665, 0.134, 0.198, 0.978, 2.4),
        (0.700, 0.072, 0.116, 0.948, 2.2),
        (0.720, 0.022, 0.036, 0.932, 2.0),
    ]
    # an elephant is distinctly long bodied -> stretch along x
    sx = 1.12
    sections = [(x * sx, ru, rv, zc, n) for (x, ru, rv, zc, n) in sections]
    return profile_along_x(sections, n_sides=72)


def build_head():
    """Head: tall domed skull tapering into a short blunt face."""
    sections = [
        (-0.085, 0.018, 0.018, 0.000, 2.0),
        (-0.070, 0.110, 0.120, 0.000, 2.2),
        (-0.048, 0.180, 0.200, 0.008, 2.4),
        (-0.018, 0.225, 0.248, 0.018, 2.4),
        (0.028, 0.246, 0.266, 0.022, 2.4),
        (0.082, 0.253, 0.270, 0.022, 2.4),
        (0.135, 0.250, 0.264, 0.016, 2.4),
        (0.185, 0.241, 0.252, 0.006, 2.4),
        (0.232, 0.226, 0.235, -0.008, 2.4),
        (0.278, 0.204, 0.212, -0.026, 2.4),
        (0.320, 0.176, 0.184, -0.048, 2.3),
        (0.358, 0.140, 0.148, -0.072, 2.2),
        (0.390, 0.098, 0.104, -0.092, 2.1),
        (0.415, 0.055, 0.058, -0.106, 2.0),
        (0.430, 0.018, 0.020, -0.112, 2.0),
    ]
    return profile_along_x(sections, n_sides=64)


def build_ear():
    """Ear: thin fan shaped shell, wide in the middle, rounded lower rim."""
    # (z, thickness_half, width_half, x_center, y_center, n)
    sections = [
        (0.000, 0.016, 0.030, 0.000, 0.000, 2.4),
        (-0.045, 0.018, 0.098, 0.004, 0.010, 2.6),
        (-0.100, 0.019, 0.156, 0.010, 0.026, 2.8),
        (-0.170, 0.019, 0.196, 0.016, 0.048, 3.0),
        (-0.250, 0.018, 0.215, 0.020, 0.072, 3.0),
        (-0.330, 0.017, 0.219, 0.020, 0.092, 3.0),
        (-0.400, 0.015, 0.205, 0.017, 0.104, 2.9),
        (-0.455, 0.013, 0.170, 0.010, 0.108, 2.8),
        (-0.495, 0.010, 0.118, 0.000, 0.104, 2.6),
        (-0.518, 0.007, 0.060, -0.012, 0.094, 2.4),
        (-0.528, 0.004, 0.016, -0.024, 0.082, 2.2),
    ]
    return profile_along_z(sections, n_sides=56, plane="yz")


def tapered_segment(length, r0, r1, cap=0.14, n_sides=44, bulge=0.0):
    """Capsule-like tapered segment running down -Z from the origin."""
    n_sec = 26
    ts = np.linspace(0.0, 1.0, n_sec)
    cap_len = cap * length
    radii = np.zeros_like(ts)
    for i, t in enumerate(ts):
        z = t * length
        if z < cap_len:
            k = 1.0 - z / cap_len
            radii[i] = r0 * np.sqrt(max(0.0, 1.0 - k * k))
        elif z > length - cap_len:
            k = (z - (length - cap_len)) / cap_len
            radii[i] = r1 * np.sqrt(max(0.0, 1.0 - k * k))
        else:
            f = (z - cap_len) / max(1e-9, length - 2.0 * cap_len)
            radii[i] = r0 + (r1 - r0) * f
        radii[i] += bulge * np.sin(np.pi * t)

    sections = []
    for t, r in zip(ts, radii):
        sections.append(
            {
                "center": (0.0, 0.0, -t * length),
                "u": (1.0, 0.0, 0.0),
                "v": (0.0, 1.0, 0.0),
                "ru": r,
                "rv": r,
                "n": 2.0,
            }
        )
    return sweep(sections, n_sides=n_sides)


def build_tusk(side=1.0, length=0.40, r0=0.038, r1=0.008):
    """Tusk: curved tapering tube sweeping forward then upward."""
    p0 = np.array([0.290, 0.105 * side, -0.145])
    t0 = np.array([0.940, 0.0, -0.342])
    n0 = np.array([0.342, 0.0, 0.940])
    R = 0.51
    delta = np.deg2rad(48.0)

    n_sec = 30
    profiles = []
    for i in range(n_sec):
        s = i / (n_sec - 1.0)
        a = delta * s
        pos = p0 + R * (np.sin(a) * t0 + (1.0 - np.cos(a)) * n0)
        tan = np.cos(a) * t0 + np.sin(a) * n0
        # orthonormal frame around the tangent
        helper = np.array([0.0, 1.0, 0.0])
        u = np.cross(tan, helper)
        u /= np.linalg.norm(u)
        v = np.cross(tan, u)
        v /= np.linalg.norm(v)
        f = s
        r = r0 + (r1 - r0) * f
        if s > 0.90:  # rounded tip
            k = (s - 0.90) / 0.10
            r = r1 * np.sqrt(max(0.0, 1.0 - k * k)) + 1e-4
        profiles.append(
            {
                "center": tuple(pos),
                "u": tuple(u),
                "v": tuple(v),
                "ru": r,
                "rv": r,
                "n": 2.0,
            }
        )
    return sweep(profiles, n_sides=36)


def build_foot(r=0.108, height=0.060):
    """Foot pad: flattened cylinder with a rounded bottom rim."""
    sections = []
    n_sec = 18
    for i in range(n_sec):
        t = i / (n_sec - 1.0)
        z = -t * height
        if t < 0.18:
            k = 1.0 - t / 0.18
            rr = r * np.sqrt(max(0.0, 1.0 - k * k)) * 0.55 + r * 0.45
        elif t > 0.86:
            k = (t - 0.86) / 0.14
            rr = r * (1.0 - 0.16 * k * k)
        else:
            rr = r
        sections.append(
            {
                "center": (0.0, 0.0, z),
                "u": (1.0, 0.0, 0.0),
                "v": (0.0, 1.0, 0.0),
                "ru": rr,
                "rv": rr,
                "n": 2.0,
            }
        )
    return sweep(sections, n_sides=48)


def build_nail(r=0.020, h=0.030):
    """Toenail: small rounded nub."""
    sections = []
    n_sec = 10
    for i in range(n_sec):
        t = i / (n_sec - 1.0)
        z = -t * h
        rr = r * np.sqrt(max(0.05, 1.0 - (1.0 - t) ** 2))
        sections.append(
            {
                "center": (0.0, 0.0, z),
                "u": (1.0, 0.0, 0.0),
                "v": (0.0, 1.0, 0.0),
                "ru": rr,
                "rv": rr * 1.25,
                "n": 2.0,
            }
        )
    return sweep(sections, n_sides=24)


def build_tuft(r=0.044, h=0.160):
    """Tail tuft: teardrop blob."""
    sections = []
    n_sec = 16
    for i in range(n_sec):
        t = i / (n_sec - 1.0)
        z = -t * h
        rr = r * np.sin(np.pi * (0.18 + 0.72 * t))
        sections.append(
            {
                "center": (0.0, 0.0, z),
                "u": (1.0, 0.0, 0.0),
                "v": (0.0, 1.0, 0.0),
                "ru": rr,
                "rv": rr,
                "n": 2.0,
            }
        )
    return sweep(sections, n_sides=28)


def build_neck():
    """Neck: short tapered collar between body and head."""
    sections = []
    n_sec = 14
    for i in range(n_sec):
        t = i / (n_sec - 1.0)
        x = t * 0.260
        r = 0.205 - 0.030 * t
        sections.append(
            {
                "center": (x, 0.0, 0.0),
                "u": (0.0, 1.0, 0.0),
                "v": (0.0, 0.0, 1.0),
                "ru": r,
                "rv": r * 0.95,
                "n": 2.3,
            }
        )
    return sweep(sections, n_sides=48)


# --------------------------------------------------------------------------
def main():
    jobs = {
        "body.stl": build_body,
        "head.stl": build_head,
        "ear.stl": build_ear,
        "neck.stl": build_neck,
        "tusk_left.stl": lambda: build_tusk(side=1.0),
        "tusk_right.stl": lambda: build_tusk(side=-1.0),
        "foot.stl": build_foot,
        "nail.stl": build_nail,
        "tuft.stl": build_tuft,
        "trunk_seg1.stl": lambda: tapered_segment(0.240, 0.088, 0.076, bulge=0.002),
        "trunk_seg2.stl": lambda: tapered_segment(0.240, 0.076, 0.062, bulge=0.002),
        "trunk_seg3.stl": lambda: tapered_segment(0.220, 0.062, 0.049, bulge=0.001),
        "trunk_seg4.stl": lambda: tapered_segment(0.180, 0.049, 0.037),
        "trunk_tip.stl": lambda: tapered_segment(0.140, 0.037, 0.023),
        "tail_seg.stl": lambda: tapered_segment(0.420, 0.038, 0.026),
        "leg_upper_front.stl": lambda: tapered_segment(0.380, 0.118, 0.100, bulge=0.010),
        "leg_lower_front.stl": lambda: tapered_segment(0.340, 0.098, 0.086),
        "leg_upper_rear.stl": lambda: tapered_segment(0.380, 0.128, 0.108, bulge=0.012),
        "leg_lower_rear.stl": lambda: tapered_segment(0.340, 0.104, 0.092),
    }

    for name, fn in jobs.items():
        verts, faces = fn()
        path = os.path.join(HERE, name)
        n = write_stl(path, verts, faces)
        print("%-22s %6d triangles  %8.1f kB" % (name, n, os.path.getsize(path) / 1024.0))

    # mirrored right ear (y -> -y, winding reversed)
    verts, faces = build_ear()
    path = os.path.join(HERE, "ear_right.stl")
    n = write_stl(path, verts, faces, mirror_y=True)
    print("%-22s %6d triangles  %8.1f kB" % ("ear_right.stl", n,
                                              os.path.getsize(path) / 1024.0))


if __name__ == "__main__":
    main()
