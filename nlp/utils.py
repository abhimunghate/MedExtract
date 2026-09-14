from collections import defaultdict


def group_entities_by_label(entities):
    """Group entities according to their labels."""

    grouped = defaultdict(list)

    for entity in entities:
        grouped[entity["label"]].append(entity)

    return dict(grouped)