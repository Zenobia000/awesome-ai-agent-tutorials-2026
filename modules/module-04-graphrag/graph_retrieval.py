"""Lab 4-02 的圖檢索（networkx 走訪＋超級節點展開規則），整理成檔案給 Lab 4-04 重用。

    from graph_retrieval import load_graph, graph_context, graph_answer

每個函式在 02_graph_networkx.ipynb 裡都有一步一步的版本。
"""

from __future__ import annotations

import json
from pathlib import Path

import networkx as nx

from course_utils.llm import chat

# 每種關係怎麼念成一句中文；小模型讀句子比讀 (A, REL, B) 準
PHRASES = {
    "CAPTAIN_OF": "{s} 是 {o} 的船長（帶頭的人）",
    "MEMBER_OF": "{s} 是 {o} 的成員",
    "OWNS": "{s} 擁有 {o}",
    "DREAMS_OF": "{s} 的夢想是 {o}",
    "FROM": "{s} 出身 {o}",
    "HAS_FATHER": "{s} 的父親是 {o}",
    "BROTHER_OF": "{s} 是 {o} 的結拜哥哥",
    "DEFEATED": "{s} 打倒了 {o}",
}

ANSWER_SYSTEM = "只根據提供的資料回答，用一句話。資料沒有就說「資料不足」。"


def load_graph(path: str | Path = "data/triples.json") -> nx.MultiDiGraph:
    """讀 triples.json，建成有向多重圖；節點帶 label 與 aliases，邊帶 relation。"""
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    graph = nx.MultiDiGraph()
    for node in data["nodes"]:
        graph.add_node(node["name"], label=node["label"], aliases=node["aliases"])
    for t in data["triples"]:
        graph.add_edge(t["subject"], t["object"], relation=t["relation"])
    return graph


def link_entities(graph: nx.MultiDiGraph, question: str) -> list[str]:
    """找出問題裡提到的節點（含別名）；被更長名字蓋住的短名字不算。"""
    hits = {}
    for name, attrs in graph.nodes(data=True):
        for surface in [name, *attrs.get("aliases", [])]:
            if surface in question:
                hits[surface] = name
    surfaces = [s for s in hits if not any(s != o and s in o for o in hits)]
    return sorted({hits[s] for s in surfaces})


def expansion_graph(graph: nx.MultiDiGraph, hub_rule: bool = True) -> nx.DiGraph:
    """可以往哪走：出邊一律可走；入邊反著走時，hub_rule=True 的話海賊團（Crew）只能走回船長。

    這條規則避免一個大團體把整張圖都拉進來（超級節點）。
    """
    expand = nx.DiGraph()
    for node, label in graph.nodes(data="label"):
        expand.add_node(node)
        expand.add_edges_from((node, v) for v in graph.successors(node))
        expand.add_edges_from((node, u) for u, _, rel in graph.in_edges(node, data="relation")
                              if not (hub_rule and label == "Crew" and rel != "CAPTAIN_OF"))
    return expand


def bfs_edges(graph: nx.MultiDiGraph, starts: list[str], hops: int,
              hub_rule: bool = True) -> list[tuple[str, str, str, int]]:
    """從起點往外走 hops 步，回傳 (主體, 關係, 客體, 第幾步)。走訪交給 nx.bfs_layers。"""
    expand = expansion_graph(graph, hub_rule)
    edges: dict[tuple[str, str, str], int] = {}
    for depth, layer in enumerate(nx.bfs_layers(expand, starts)):
        if depth >= hops:
            break
        for node in layer:
            incident = list(graph.out_edges(node, data="relation")) + list(graph.in_edges(node, data="relation"))
            for u, v, rel in incident:
                other = v if u == node else u
                if expand.has_edge(node, other):
                    edges.setdefault((u, rel, v), depth + 1)
    return [(*e, hop) for e, hop in edges.items()]


def to_text(edges: list[tuple]) -> str:
    return "\n".join(PHRASES[r].format(s=s, o=o) for s, r, o, *_ in edges)


def graph_context(graph: nx.MultiDiGraph, question: str, hops: int = 4) -> str:
    return to_text(bfs_edges(graph, link_entities(graph, question), hops))


def graph_answer(graph: nx.MultiDiGraph, question: str, hops: int = 4) -> str:
    context = graph_context(graph, question, hops)
    return chat([
        {"role": "system", "content": ANSWER_SYSTEM},
        {"role": "user", "content": f"資料：\n{context}\n\n問題：{question}"},
    ])
