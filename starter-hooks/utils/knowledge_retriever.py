#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# ///

"""
Knowledge Retriever - Query engine with TF-IDF scoring and context-aware boosting.

This module provides semantic retrieval of knowledge fragments based on
user prompts. It uses TF-IDF scoring with additional boosting for:
- Tag matching (fragments with relevant tags rank higher)
- Recency weighting (recently accessed fragments get slight boost)
- Scope priority (shared > personal for project knowledge)

Returns formatted context injection suitable for Claude prompts.
"""

import re
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple

from .knowledge_store import (
    DualKnowledgeStore,
    Fragment,
    SCOPE_SHARED,
    SCOPE_PERSONAL
)


# Context rules for tag boosting based on detected prompt patterns
CONTEXT_TAG_RULES: List[Dict[str, Any]] = [
    {
        "name": "forms",
        "keywords": ["form", "input", "validation", "submit", "field", "formgen", "zod"],
        "boost_tags": ["forms", "react-forms", "validation", "zod", "formgen"]
    },
    {
        "name": "tables",
        "keywords": ["table", "grid", "ag-grid", "datagrid", "columns", "sorting"],
        "boost_tags": ["tables", "ag-grid", "grid", "data-grid"]
    },
    {
        "name": "api",
        "keywords": ["api", "fetch", "query", "mutation", "tanstack", "react-query"],
        "boost_tags": ["api", "data-fetching", "tanstack-query", "react-query"]
    },
    {
        "name": "components",
        "keywords": ["component", "modal", "dialog", "button", "page", "view"],
        "boost_tags": ["components", "react", "ui", "design-patterns"]
    },
    {
        "name": "styling",
        "keywords": ["style", "css", "tailwind", "design", "layout", "responsive"],
        "boost_tags": ["styling", "tailwind", "css", "design"]
    },
    {
        "name": "testing",
        "keywords": ["test", "spec", "playwright", "e2e", "unit", "browser"],
        "boost_tags": ["testing", "playwright", "e2e", "unit-tests"]
    },
    {
        "name": "state",
        "keywords": ["state", "zustand", "redux", "context", "store"],
        "boost_tags": ["state", "zustand", "state-management"]
    },
    {
        "name": "backend",
        "keywords": ["service", "controller", "entity", "dotnet", "csharp", "api endpoint"],
        "boost_tags": ["backend", "dotnet", "csharp", "services", "api"]
    },
    {
        "name": "database",
        "keywords": ["database", "migration", "sql", "query", "entity"],
        "boost_tags": ["database", "sql", "migrations", "entity-framework"]
    },
    {
        "name": "workflow",
        "keywords": ["workflow", "preference", "setting", "configure"],
        "boost_tags": ["workflow", "preference", "personal", "settings"]
    }
]


def detect_context_tags(prompt: str) -> List[str]:
    """
    Detect relevant tags based on prompt content.

    Analyzes the prompt for keywords that indicate what context
    the user is working in, returns tags to boost.
    """
    prompt_lower = prompt.lower()
    boost_tags: List[str] = []

    for rule in CONTEXT_TAG_RULES:
        if any(kw in prompt_lower for kw in rule["keywords"]):
            boost_tags.extend(rule["boost_tags"])

    # Deduplicate while preserving order
    seen = set()
    unique_tags = []
    for tag in boost_tags:
        if tag not in seen:
            seen.add(tag)
            unique_tags.append(tag)

    return unique_tags


def calculate_recency_boost(fragment: Fragment, max_boost: float = 0.2) -> float:
    """
    Calculate recency boost based on last access time.

    Fragments accessed recently get a small boost.
    Returns a multiplier between 1.0 and (1.0 + max_boost).
    """
    if not fragment.last_accessed:
        return 1.0

    try:
        last_accessed = datetime.fromisoformat(fragment.last_accessed)
        now = datetime.now()
        age = now - last_accessed

        # Fragments accessed in last hour get full boost
        # Boost decays over 7 days
        if age < timedelta(hours=1):
            return 1.0 + max_boost
        elif age < timedelta(days=1):
            decay = age.total_seconds() / (24 * 3600)
            return 1.0 + max_boost * (1 - decay)
        elif age < timedelta(days=7):
            decay = age.days / 7
            return 1.0 + max_boost * 0.5 * (1 - decay)
        else:
            return 1.0
    except (ValueError, TypeError):
        return 1.0


def calculate_tag_boost(fragment: Fragment, boost_tags: List[str], boost_factor: float = 0.3) -> float:
    """
    Calculate tag boost based on matching tags.

    Returns a multiplier based on how many boost tags match.
    """
    if not boost_tags or not fragment.tags:
        return 1.0

    matching_tags = set(fragment.tags) & set(boost_tags)
    if not matching_tags:
        return 1.0

    # More matching tags = higher boost (up to boost_factor)
    match_ratio = len(matching_tags) / len(boost_tags)
    return 1.0 + (boost_factor * match_ratio)


def calculate_access_boost(fragment: Fragment, max_boost: float = 0.1) -> float:
    """
    Calculate boost based on access frequency.

    Frequently accessed fragments are likely more valuable.
    """
    if fragment.accessed_count <= 0:
        return 1.0

    # Logarithmic boost to prevent runaway scores
    # 10 accesses = ~0.5 * max_boost, 100 accesses = max_boost
    import math
    normalized = math.log10(fragment.accessed_count + 1) / 2
    return 1.0 + min(normalized * max_boost, max_boost)


class KnowledgeRetriever:
    """
    Query engine for semantic knowledge retrieval.

    Combines TF-IDF scoring with context-aware boosting to find
    the most relevant knowledge fragments for a given prompt.
    """

    def __init__(self, store: Optional[DualKnowledgeStore] = None):
        """
        Initialize retriever with a knowledge store.

        Args:
            store: DualKnowledgeStore instance. Created if not provided.
        """
        self.store = store or DualKnowledgeStore()

    def retrieve(
        self,
        prompt: str,
        top_k: int = 5,
        min_score: float = 0.1,
        include_personal: bool = True
    ) -> List[Tuple[Fragment, float]]:
        """
        Retrieve relevant fragments for a prompt.

        Args:
            prompt: The user's prompt text
            top_k: Maximum number of fragments to return
            min_score: Minimum score threshold for inclusion
            include_personal: Whether to include personal fragments

        Returns:
            List of (fragment, final_score) tuples, sorted by relevance.
        """
        # Detect context for tag boosting
        boost_tags = detect_context_tags(prompt)

        # Get base results from store
        # Request more than top_k so we can re-rank
        results = self.store.search(
            query=prompt,
            top_k=top_k * 3,
            shared_boost=1.0,  # We'll apply our own boosting
            personal_tags_boost=boost_tags if include_personal else []
        )

        # Apply boosting factors
        boosted_results: List[Tuple[Fragment, float]] = []

        for fragment, base_score in results:
            # Skip personal if not included
            if not include_personal and fragment.scope == SCOPE_PERSONAL:
                continue

            final_score = base_score

            # Apply tag boost
            final_score *= calculate_tag_boost(fragment, boost_tags)

            # Apply recency boost
            final_score *= calculate_recency_boost(fragment)

            # Apply access frequency boost
            final_score *= calculate_access_boost(fragment)

            # Shared fragments get slight preference for project knowledge
            # (unless boost_tags indicate workflow/personal context)
            if fragment.scope == SCOPE_SHARED:
                if not any(t in boost_tags for t in ['workflow', 'preference', 'personal']):
                    final_score *= 1.1

            boosted_results.append((fragment, final_score))

        # Sort by final score and apply threshold
        boosted_results.sort(key=lambda x: x[1], reverse=True)
        filtered = [(f, s) for f, s in boosted_results if s >= min_score]

        return filtered[:top_k]

    def retrieve_and_format(
        self,
        prompt: str,
        top_k: int = 5,
        format_style: str = "context"
    ) -> str:
        """
        Retrieve and format fragments for context injection.

        Args:
            prompt: The user's prompt text
            top_k: Maximum number of fragments to return
            format_style: 'context' (for system prompts), 'list' (for display)

        Returns:
            Formatted string ready for injection or display.
        """
        results = self.retrieve(prompt, top_k=top_k)

        if not results:
            return ""

        if format_style == "list":
            return self._format_as_list(results)
        else:
            return self._format_as_context(results)

    def _format_as_context(self, results: List[Tuple[Fragment, float]]) -> str:
        """Format results as context injection."""
        if not results:
            return ""

        lines = [
            "",
            "-" * 50,
            "RELEVANT KNOWLEDGE",
            "-" * 50,
            ""
        ]

        for fragment, score in results:
            # Show tags if present
            tag_str = f" [{', '.join(fragment.tags)}]" if fragment.tags else ""
            scope_indicator = "📁" if fragment.scope == SCOPE_SHARED else "👤"

            lines.append(f"{scope_indicator}{tag_str}")
            lines.append(fragment.content)
            lines.append("")

        lines.append("-" * 50)

        return "\n".join(lines)

    def _format_as_list(self, results: List[Tuple[Fragment, float]]) -> str:
        """Format results as a readable list."""
        if not results:
            return "No relevant knowledge found."

        lines = ["Found knowledge fragments:", ""]

        for i, (fragment, score) in enumerate(results, 1):
            scope_label = "shared" if fragment.scope == SCOPE_SHARED else "personal"
            tags_str = ", ".join(fragment.tags) if fragment.tags else "no tags"

            lines.append(f"{i}. [{fragment.id}] ({scope_label}, {tags_str})")
            lines.append(f"   Score: {score:.3f}")
            lines.append(f"   {fragment.content[:100]}...")
            lines.append("")

        return "\n".join(lines)

    def mark_retrieved(self, fragments: List[Fragment]) -> None:
        """
        Mark fragments as accessed (updates access tracking).

        Call this after successfully using retrieved fragments.
        """
        for fragment in fragments:
            fragment.mark_accessed()
            # Get the appropriate store
            if fragment.scope == SCOPE_SHARED:
                self.store.shared.update(fragment)
            else:
                self.store.personal.update(fragment)


def retrieve_for_prompt(prompt: str, top_k: int = 5) -> str:
    """
    Convenience function to retrieve and format knowledge for a prompt.

    Returns formatted context string or empty string if no matches.
    """
    retriever = KnowledgeRetriever()
    return retriever.retrieve_and_format(prompt, top_k=top_k)


def search_knowledge(query: str, top_k: int = 10) -> List[Tuple[Fragment, float]]:
    """
    Convenience function to search knowledge store.

    Returns list of (fragment, score) tuples.
    """
    retriever = KnowledgeRetriever()
    return retriever.retrieve(query, top_k=top_k, min_score=0.0)


if __name__ == "__main__":
    import sys

    print("Knowledge Retriever Test")
    print("=" * 50)

    if len(sys.argv) < 2:
        print("Usage: knowledge_retriever.py <query>")
        print("Example: knowledge_retriever.py 'how to create a react form'")
        sys.exit(1)

    query = " ".join(sys.argv[1:])
    print(f"Query: {query}")
    print()

    # Detect context
    boost_tags = detect_context_tags(query)
    if boost_tags:
        print(f"Detected context tags: {', '.join(boost_tags)}")
        print()

    # Search
    results = search_knowledge(query)

    if not results:
        print("No matching knowledge found.")
    else:
        print(f"Found {len(results)} matching fragments:")
        print()

        for fragment, score in results:
            scope_label = "shared" if fragment.scope == SCOPE_SHARED else "personal"
            print(f"[{score:.3f}] {fragment.id} ({scope_label})")
            print(f"  Tags: {', '.join(fragment.tags) if fragment.tags else 'none'}")
            print(f"  {fragment.content[:100]}...")
            print()
