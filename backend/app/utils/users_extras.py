import random


FIRST_PARTS = ["Pixel", "Cyber", "Neon", "Quantum", "Binary", "Synth", "Volt", "Data", "Node", "Hex"]
LAST_PARTS  = ["Walker", "Coder", "Runner", "Watcher", "Seeker", "Tracer", "Rider", "Drifter", "Scout", "Spark"]

def generate_test_username() -> str:
    """Generate a unique readable username like 'PixelWalker_4821'."""
    first = random.choice(FIRST_PARTS)
    last  = random.choice(LAST_PARTS)
    suffix = random.randint(1000, 9999)
    return f"{first}{last}_{suffix}"