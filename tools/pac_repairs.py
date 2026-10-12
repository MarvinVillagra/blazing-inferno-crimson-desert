#!/usr/bin/env python3
"""Offline, reversible repairs for decoded PAC 3/9 files using CDMW parsers."""
import argparse
import hashlib
import json
from pathlib import Path
import struct


def sha(data):
    return hashlib.sha256(data).hexdigest()


def read_checked(path, expected=None):
    data = path.read_bytes()
    if expected and sha(data) != expected:
        raise ValueError('Input SHA-256 does not match the selected reference.')
    return data


def write_new(path, data):
    # Exclusive creation prevents overwriting inputs or an earlier candidate.
    with path.open('xb') as stream:
        stream.write(data)


def parsers():
    try:
        from cdmw.modding.pac_cloth import pac_cloth_lods, decode_pac_cloth_binding
        from cdmw.modding.pac_cloth_guides import decode_pac_cloth_guides
    except ImportError as exc:
        raise RuntimeError('Put a compatible CDMW package root on PYTHONPATH.') from exc
    return pac_cloth_lods, decode_pac_cloth_binding, decode_pac_cloth_guides


def hide_skin(data, name, low, high, half_width):
    lods, _, _ = parsers()
    if not low < high or half_width <= 0:
        raise ValueError('Select a valid covered-skin bounding region.')
    patched = bytearray(data)
    allowed, counts = set(), []
    for lod in lods(data):
        matches = [s for s in lod.submeshes if s.name.casefold() == name.casefold()]
        if len(matches) != 1:
            raise ValueError('Select one exact skin subsection name in every LOD.')
        sm, count = matches[0], 0
        for k in range(0, sm.source_index_count, 3):
            off = sm.source_index_offset + 2*k
            f = struct.unpack_from('<3H', data, off)
            if len(set(f)) < 3:
                continue
            if any(j >= len(sm.vertices) for j in f):
                raise ValueError('Out-of-range face index.')
            if all(low < sm.vertices[j][1] < high and abs(sm.vertices[j][0]) < half_width for j in f):
                struct.pack_into('<3H', patched, off, f[0], f[0], f[0])
                allowed.update(range(off, off+6))
                count += 1
        counts.append(count)
    if not counts or not min(counts):
        raise ValueError('Selection hides no triangles in at least one LOD.')
    result = bytes(patched)
    if any(a != b and i not in allowed for i, (a, b) in enumerate(zip(data, result))):
        raise ValueError('Mutation escaped selected index records.')
    for old, new in zip(lods(data), lods(result)):
        for a, b in zip(old.submeshes, new.submeshes):
            for field in ('vertices', 'uvs', 'normals', 'bone_indices', 'bone_weights'):
                if getattr(a, field) != getattr(b, field):
                    raise ValueError('Skin hiding changed vertex attributes.')
            if a.name.casefold() != name.casefold() and a.faces != b.faces:
                raise ValueError('Skin hiding changed another subsection.')
    return result, {'hidden_triangles_per_lod': counts}


def restore_skeletal(data, reference, name, first, count):
    lods, binding, guides = parsers()
    from cdmw.modding.pabv_parser import decode_pac_embedded_volumes
    current, original = lods(data), lods(reference)
    if len(current) != len(original) or first < 0 or count <= 0:
        raise ValueError('Invalid LOD count or vertex range.')
    if decode_pac_embedded_volumes(data).bone_palette != decode_pac_embedded_volumes(reference).bone_palette:
        raise ValueError('Skeleton palettes differ.')
    patched = bytearray(data)
    counts = []
    for a, b in zip(current, original):
        left = [s for s in a.submeshes if s.name.casefold() == name.casefold()]
        right = [s for s in b.submeshes if s.name.casefold() == name.casefold()]
        if len(left) != 1 or len(right) != 1:
            raise ValueError('Select one exact subsection in every LOD.')
        sm, source = left[0], right[0]
        for field in ('vertices', 'faces', 'uvs'):
            if getattr(sm, field) != getattr(source, field):
                raise ValueError('Reference topology/geometry differs.')
        if first+count > len(sm.vertices):
            raise ValueError('Vertex range exceeds the selected subsection.')
        counts.append(sum(binding(data, o) is not None for o in sm.source_vertex_offsets[first:first+count]))
        for x, y in zip(sm.source_vertex_offsets[first:first+count], source.source_vertex_offsets[first:first+count]):
            if binding(reference, y) is not None:
                raise ValueError('Reference range must use ordinary skeletal encoding.')
            for start, end in ((12, 16), (20, 36)):
                patched[x+start:x+end] = reference[y+start:y+end]
            patched[x+39] = (data[x+39] & 0xc0) | 63
    result = bytes(patched)
    if guides(data) != guides(result):
        raise ValueError('Guide metadata changed.')
    for a, b in zip(current, lods(result)):
        for sm, new in zip(a.submeshes, b.submeshes):
            for j, (x, y) in enumerate(zip(sm.source_vertex_offsets, new.source_vertex_offsets)):
                selected = sm.name.casefold() == name.casefold() and first <= j < first+count
                if selected:
                    if binding(result, y) is not None:
                        raise ValueError('Selected vertex still uses guide deformation.')
                elif data[x:x+40] != result[y:y+40]:
                    raise ValueError('Unselected vertex changed.')
    return result, {'restored_vertices_per_lod': count, 'removed_bindings_per_lod': counts}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--expected-sha256', help='Refuse a different input file')
    sub = parser.add_subparsers(dest='command', required=True)
    inspect = sub.add_parser('inspect')
    inspect.add_argument('input', type=Path)
    for name in ('hide-skin', 'restore-skeletal'):
        command = sub.add_parser(name)
        command.add_argument('input', type=Path)
        command.add_argument('output', type=Path)
        command.add_argument('--submesh', required=True)
        if name == 'hide-skin':
            command.add_argument('--y-min', type=float, required=True)
            command.add_argument('--y-max', type=float, required=True)
            command.add_argument('--half-width', type=float, required=True)
        else:
            command.add_argument('--reference', type=Path, required=True)
            command.add_argument('--first', type=int, required=True)
            command.add_argument('--count', type=int, required=True)
    args = parser.parse_args()
    data = read_checked(args.input, args.expected_sha256)
    if args.command == 'inspect':
        lods, binding, guides = parsers()
        g = guides(data)
        report = {'sha256': sha(data), 'guides': len(g.vertices) if g else 0, 'lods': [
            [{'name': sm.name, 'vertices': len(sm.vertices), 'triangles': len(sm.faces),
              'cloth_bound': sum(binding(data, o) is not None for o in sm.source_vertex_offsets)} for sm in lod.submeshes]
            for lod in lods(data)]}
    else:
        if args.command == 'hide-skin':
            result, report = hide_skin(data, args.submesh, args.y_min, args.y_max, args.half_width)
        else:
            result, report = restore_skeletal(data, read_checked(args.reference), args.submesh, args.first, args.count)
        write_new(args.output, result)
        report.update(before_sha256=sha(data), after_sha256=sha(result), runtime_verified=False)
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
