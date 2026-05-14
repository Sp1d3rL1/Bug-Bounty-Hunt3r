#!/usr/bin/env python3
"""Create line-based diffs for recon outputs."""
from __future__ import annotations
import argparse
from pathlib import Path

def read_set(path: Path) -> set[str]:
    if not path.exists():
        return set()
    return {line.strip() for line in path.read_text(errors='ignore').splitlines() if line.strip()}

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--old', required=True)
    ap.add_argument('--new', required=True)
    ap.add_argument('--out', required=True)
    args = ap.parse_args()
    old = read_set(Path(args.old))
    new = read_set(Path(args.new))
    added = sorted(new - old)
    removed = sorted(old - new)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    lines = []
    lines.append(f'# Diff: {Path(args.old).name} -> {Path(args.new).name}')
    lines.append('')
    lines.append(f'Added: {len(added)}')
    lines.extend(f'+ {x}' for x in added[:500])
    if len(added) > 500:
        lines.append(f'+ ... truncated {len(added)-500} more')
    lines.append('')
    lines.append(f'Removed: {len(removed)}')
    lines.extend(f'- {x}' for x in removed[:200])
    out.write_text('\n'.join(lines) + '\n')
    print(out)
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
