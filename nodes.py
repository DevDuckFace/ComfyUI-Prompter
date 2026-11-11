import os
import random

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
MODES = ["🔀 random", "🔒 locked"]
MAX_JOIN_INPUTS = 64

_cache = {}


def load_prompts(filename):
    if filename not in _cache:
        with open(os.path.join(DATA_DIR, filename), encoding="utf-8") as f:
            _cache[filename] = [line.strip() for line in f if line.strip()]
    return _cache[filename]


class _PrompterBase:
    FILE = None
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("prompt",)
    FUNCTION = "run"
    CATEGORY = "Prompter"
    OUTPUT_NODE = True

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "mode": (MODES, {"default": MODES[0]}),
                "text": ("STRING", {"multiline": True, "default": ""}),
            }
        }

    @classmethod
    def IS_CHANGED(cls, mode, text):
        # Random mode: force re-execution on every queue
        if mode == MODES[0]:
            return float("nan")
        return text

    def run(self, mode, text):
        if mode == MODES[0] or not text.strip():
            text = random.choice(load_prompts(self.FILE))
        return {"ui": {"text": [text]}, "result": (text,)}


class Prompter(_PrompterBase):
    FILE = "prompter.txt"


class PrompterWomans(_PrompterBase):
    FILE = "prompterwomans.txt"


class PrompterJoin:
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("prompt",)
    FUNCTION = "run"
    CATEGORY = "Prompter"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {
                f"prompt_{i}": ("STRING", {"forceInput": True})
                for i in range(1, MAX_JOIN_INPUTS + 1)
            },
        }

    def run(self, **kwargs):
        keys = sorted((k for k in kwargs if k.startswith("prompt_")),
                      key=lambda k: int(k.split("_")[1]))
        parts = []
        for k in keys:
            p = (kwargs[k] or "").strip().strip(",").strip()
            if p:
                parts.append(p)
        return (", ".join(parts),)


NODE_CLASS_MAPPINGS = {
    "Prompter": Prompter,
    "PrompterWomans": PrompterWomans,
    "PrompterJoin": PrompterJoin,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Prompter": "Prompter ► (73k random)",
    "PrompterWomans": "Prompter ♀ Womans (50k random)",
    "PrompterJoin": "Prompter Join ✚",
}
