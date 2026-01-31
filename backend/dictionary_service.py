from typing import Optional

# Mock dictionary with sample definitions
# In a real app, this would call an external API
MOCK_DEFINITIONS = {
    "extraordinary": "Very unusual or remarkable.",
    "loquacious": "Tending to talk a great deal; talkative.",
    "comprehensive": "Complete and including everything necessary.",
    "contemporary": "Living or occurring at the same time.",
    "documentation": "Material that provides official information.",
    "illuminating": "Helping to clarify or explain something.",
    "comfortable": "Providing physical ease and relaxation.",
    "exceptionally": "To an unusual degree; very.",
    "particularly": "To a higher degree than is usual or average.",
    "professor": "A university teacher of the highest rank."
}

def get_definition(word: str) -> Optional[str]:
    """
    Get definition for a word.

    Args:
        word: The word to look up (can include punctuation)

    Returns:
        Definition string if found, else a default message
    """
    # Clean the word: lowercase and remove punctuation
    clean_word = word.lower().strip('.,!?;:\'"')

    # Look up in our mock dictionary
    return MOCK_DEFINITIONS.get(
        clean_word,
        "A complex word worth looking up!"
    )
