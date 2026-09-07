"""
knowledge_graph.py
--------------------
Interface to the layered skill knowledge graph (Domain -> Topic -> Concept).
This is a lightweight in-memory implementation so the AI layer can run
standalone. Swap `_GRAPH` for a real DB-backed graph (e.g. Neo4j or a
Postgres adjacency table) once the integration teammate's graph is ready —
keep the function signatures the same so nothing else has to change.
"""

from typing import List, Dict, Optional

# Example graph shape — replace/extend with the real department skill map.
# domain -> topic -> [concepts], plus a prerequisite map at concept level.
_GRAPH: Dict[str, Dict[str, List[str]]] = {
    "Cybersecurity Awareness": {
        "Network Security": ["Firewalls", "IDS/IPS", "Network Attacks"],
        "Data Security": ["Encryption", "Access Control", "Data Privacy"],
        "Incident Response": ["Detection", "Analysis", "Recovery"],
    },
    "Digital Governance": {
        "Policy Understanding": ["E-Governance Frameworks", "RTI Compliance"],
        "Data Management": ["Data Classification", "Record Keeping"],
    },
}

# concept -> list of prerequisite concepts (used for gap prioritization)
_PREREQUISITES: Dict[str, List[str]] = {
    "Incident Analysis": ["Network Attacks", "Detection"],
    "Recovery": ["Analysis"],
    "Access Control": ["Encryption"],
}


def get_concepts_for_topic(domain: str, topic: str) -> List[str]:
    return _GRAPH.get(domain, {}).get(topic, [])


def get_all_concepts() -> List[str]:
    concepts = []
    for topics in _GRAPH.values():
        for concept_list in topics.values():
            concepts.extend(concept_list)
    return concepts


def get_domain_for_concept(concept: str) -> Optional[str]:
    for domain, topics in _GRAPH.items():
        for concept_list in topics.values():
            if concept in concept_list:
                return domain
    return None


def get_topic_for_concept(concept: str) -> Optional[str]:
    for topics in _GRAPH.values():
        for topic, concept_list in topics.items():
            if concept in concept_list:
                return topic
    return None


def get_prerequisites(concept: str) -> List[str]:
    """Concepts that should be mastered before this one."""
    return _PREREQUISITES.get(concept, [])


def get_dependents(concept: str) -> List[str]:
    """Concepts that depend on this one (reverse of prerequisites)."""
    return [c for c, prereqs in _PREREQUISITES.items() if concept in prereqs]


def build_prerequisite_map(concepts: List[str]) -> Dict[str, List[str]]:
    """Helper used by gap_analyzer to pass prerequisite context to the LLM."""
    return {c: get_prerequisites(c) for c in concepts}
