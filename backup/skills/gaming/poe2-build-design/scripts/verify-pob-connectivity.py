#!/usr/bin/env python3
"""Verify all nodes in a proposed POB tree are connected to the class start node.

Usage:
    python3 scripts/verify-pob-connectivity.py <node1,node2,...> <class_start_node> [tree_json_path]

Example:
    python3 scripts/verify-pob-connectivity.py 7120,20830,37078,46535 50986
    python3 scripts/verify-pob-connectivity.py 9994,17268,7621 44683 /tmp/tree.json

Behavior:
    - If ALL nodes connected: exit 0, print "OK: N nodes connected"
    - If ANY disconnected: exit 1, print "FAIL: X nodes disconnected" + list of IDs
    - Always print the count of connected vs disconnected
"""

import json, sys
from collections import deque

def main():
    if len(sys.argv) < 3:
        print("Usage: verify-pob-connectivity.py <node_ids_csv> <start_node> [tree_json]")
        sys.exit(2)
    
    node_csv = sys.argv[1]
    start_node = sys.argv[2]
    tree_json = sys.argv[3] if len(sys.argv) > 3 else '/tmp/PathOfBuilding-PoE2/src/TreeData/0_5/tree.json'
    
    my_nodes = set(node_csv.split(','))
    my_nodes.add(start_node)  # Ensure start is included
    
    with open(tree_json) as f:
        tree = json.load(f)
    nodes = tree['nodes']
    
    # Build full bidirectional adjacency from ALL nodes (target set may need intermediate nodes)
    adj = {}
    for nid_s in nodes:
        adj[nid_s] = set()
    for nid_s in nodes:
        for c in nodes[nid_s].get('connections', []):
            cid = str(c['id']) if isinstance(c, dict) else str(c)
            if cid in nodes:
                adj[nid_s].add(cid)
                adj[cid].add(nid_s)
    
    # BFS from start — consider ALL nodes, then intersect with target set
    visited = set()
    q = deque([start_node])
    while q:
        nid = q.popleft()
        if nid in visited:
            continue
        visited.add(nid)
        for nxt in adj.get(nid, set()):
            if nxt not in visited:
                q.append(nxt)
    
    target_connected = visited & my_nodes
    disconnected = my_nodes - visited
    
    print(f"Total target nodes: {len(my_nodes)}")
    print(f"Connected from {start_node}: {len(target_connected)}")
    print(f"Disconnected: {len(disconnected)}")
    
    if disconnected:
        # Show which nodes and why
        for nid in sorted(disconnected, key=int):
            n = nodes.get(str(nid), {})
            name = n.get('name', '?')
            an = n.get('ascendancyName', '')
            tag = f"[{an}]" if an else ""
            conns = [c.get('id', c) for c in n.get('connections', [])]
            print(f"  {nid} {tag} {name}: connects to {conns}")
        sys.exit(1)
    
    print("OK: All nodes connected")
    sys.exit(0)

if __name__ == '__main__':
    main()
