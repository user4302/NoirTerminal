#!/usr/bin/env python3
"""
NoirTerminal Commands Module

Defines command templates and mappings for noir commentary generation.
"""

from typing import List, Dict


# Generic command template values (extracted from NOIR_COMMENTARY)
GENERIC_COMMANDS: Dict[str, List[str]] = {
    # File operations (Linux)
    "file_reveal": [
        "👻 *The shadows reveal their secrets...* I'll read this file aloud...",
        "🎭 *Peering through the cracks of reality*... what treasures await within?",
        "💀 *A portal to hidden knowledge opens*... let's take a peek.",
    ],
    "directory_listing": [
        "👻 *The contents materialize from nothingness*...",
        "🎭 *Let me show you what lurks in this directory*...",
        "💀 *Here they come, the digital denizens*...",
    ],
    "path_change": [
        "🎭 *Ah, stepping into new territory*...",
        "👻 *The path changes... where to next?*",
        "💀 *A portal opens... welcome to the void*...",
    ],
    "file_deletion": [
        "💀 *Don't do it!* Those files have stories... but if you must destroy them...",
        "🎭 *Erasing history, one byte at a time*...",
        "👻 *Poof! Gone forever...* Can you hear the echoes?",
    ],
    "file_copy": [
        "👻 *Copying memories to another place*...",
        "🎭 *Digital immortality achieved*...",
        "💀 *The same file, twice... redundancy is safety*...",
    ],
    "file_move": [
        "🎭 *One more name change...* The files have new identities.",
        "👻 *Relocating data through the ether*...",
        "💀 *Moved again... never to be found*...",
    ],
    "directory_create": [
        "👻 *A new chamber is being forged in the digital realm*...",
        "🎭 *Another room opens up in this digital mansion*...",
        "💀 *Yet another folder waiting for secrets*...",
    ],
    "file_touch": [
        "👻 *Birth of something new...* Empty but full of potential.",
        "🎭 *An empty vessel awaits*...",
        "💀 *Created... yet unborn files, waiting to be filled*...",
    ],
    "search_pattern": [
        "🎭 *Searching the archives for hidden truth*...",
        "👻 *The needles in digital haystacks emerge*...",
        "💀 *Patterns emerge from chaos...*...",
    ],
    "find_files": [
        "🎭 *Calling forth lost data from the shadows*...",
        "👻 *Let's explore the dark corners of your filesystem*...",
        "💀 *Every file has a story... let me tell you theirs*...",
    ],
    "process_list": [
        "🎭 *A parade of processes...* Each one with its own purpose.",
        "👻 *The digital workforce at work*...",
        "💀 *They keep your system alive*...",
    ],
    "process_top": [
        "🎭 *The digital spirits dance...* Here they are, alive and processing.",
        "👻 *A parade of processes...* Each one with its own purpose.",
        "💀 *They work while you sleep... thank you*...",
    ],
    "process_kill": [
        "💀 *Don't disturb them yet...* Those spirits are still at work.",
        "🎭 *Sending a message to the digital entities*...",
        "👻 *Will they hear your call?*",
    ],
    "nano_editor": ["👻 *A simple editor, an old friend*..."],
    "vim_editor": [
        "💀 *Vi/motion heaven awaits*...",
        "🎭 *Enter the cathedral of code...* Vim will guide you.",
    ],
    "less_viewer": [
        "🎭 *Scrolling through frozen time*...",
        "👻 *Pages from yesterday, still fresh*...",
    ],
    "more_viewer": ["👻 *An old-school page turner*..."],
    "download_wget": [
        "🎭 *Fetching from the digital ether*...",
        "💀 *Download complete...* The shadows now hold another file.",
    ],
    "curl_request": [
        "👻 *Making requests to the API spirits*...",
        "🎭 *Data flows from the void*...",
    ],
    "ssh_connect": [
        "👻 *Opening a portal to another realm*...",
        "💀 *Who waits on that machine?*",
    ],
    "git_clone": [
        "👻 *Summoning code from the void*...",
        "💀 *A new repository enters existence*...",
    ],
    "git_commit": [
        "🎭 *Preserving a moment in time*...",
        "👻 *History is being written*...",
    ],
    "git_push": ["💀 *Sending your work to the world*..."],
    "git_pull": ["👻 *Bringing down changes from above*..."],
}


# Command mappings
NOIR_COMMENTARY: Dict[str, List[str]] = {
    # File operations (Linux)
    "cat": ["file_reveal"],
    "ls": ["directory_listing"],
    "cd": ["path_change"],
    "rm": ["file_deletion"],
    "cp": ["file_copy"],
    "mv": ["file_move"],
    "mkdir": ["directory_create"],
    "touch": ["file_touch"],
    "grep": ["search_pattern"],
    "find": ["find_files"],
    "ps aux": ["process_list"],
    "top": ["process_top"],
    "kill": ["process_kill"],
    "nano": ["nano_editor"],
    "vim": ["vim_editor"],
    "less": ["less_viewer"],
    "more": ["more_viewer"],
    "wget": ["download_wget"],
    "curl": ["curl_request"],
    "ssh": ["ssh_connect"],
    
    # Git commands
    "git clone": ["git_clone"],
    "git commit": ["git_commit"],
    "git push": ["git_push"],
    "git pull": ["git_pull"],
}


def get_command_templates(command: str) -> List[str]:
    """
    Get noir commentary templates for a given command.
    
    Args:
        command: Command string
    
    Returns:
        List of noir commentary strings
    
    Raises:
        KeyError: If command is not found in NOIR_COMMENTARY
    """
    # Try exact match first
    if command in NOIR_COMMENTARY:
        generic_keys = NOIR_COMMENTARY[command]
        templates: List[str] = []
        for key in generic_keys:
            if key in GENERIC_COMMANDS:
                templates.extend(GENERIC_COMMANDS[key])
        return templates
    
    raise KeyError(f"No templates found for command: {command}")


def get_random_template(command: str) -> str:
    """
    Get a random noir commentary template for a given command.
    
    Args:
        command: Command string
    
    Returns:
        Random noir commentary string
    
    Raises:
        KeyError: If command is not found in NOIR_COMMENTARY
    """
    templates = get_command_templates(command)
    import random
    return random.choice(templates)


# Ghost story narrative templates (fallback for unknown commands)
GHOST_STORY_TEMPLATES: Dict[str, List[str]] = {
    "random": [
        "*The monitor flickers and whispers back at you*",
        "*You can almost hear the code typing itself*, but is it really?",
        "*A cold chill runs through your keyboard*, just as someone touches yours",
        "*Your reflection in the screen seems... different today*",
        "*The terminal cursor blinks with a rhythm only ghosts know*",
    ],
}