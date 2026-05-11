"""
Known Proton launch diagnostics for truckersmp-cli.

Licensed under MIT.
"""

import logging


_PROTON_OUTPUT_PATTERNS = (
    {
        "id": "steam_not_visible",
        "patterns": (
            "SteamAPI_IsSteamRunning() did not locate a running instance of Steam",
        ),
        "summary": "Steam is not visible from the Proton/Wine process.",
        "suggestion": (
            "Make sure Steam is running and that truckersmp-cli is using the "
            "same Steam installation. If Steam is installed through Snap or "
            "Flatpak, check sandbox path access and try setting "
            "--native-steam-dir explicitly."
        ),
    },
    {
        "id": "steam_ipc_universe_failure",
        "patterns": (
            "GetConnectedUniverse returned failure code 12",
            "GetSteamRealm returned failure code 12",
            "Don't know Steam universe",
        ),
        "summary": "Proton could not talk to the running Steam client correctly.",
        "suggestion": (
            "Check that the selected Steam directory matches the running Steam "
            "client, then run `truckersmp-cli doctor` to inspect Steam, Proton, "
            "and Steam Runtime paths."
        ),
    },
    {
        "id": "steam_api_pipe_failure",
        "patterns": (
            "SteamAPI_Init() failed; create pipe failed",
            "create pipe failed",
        ),
        "summary": "Steam API pipe creation failed inside Proton/Wine.",
        "suggestion": (
            "This usually means the Proton process cannot access Steam IPC. "
            "Check Steam Runtime shared paths, sandboxed Steam installs, and "
            "whether Steam is running under the same user."
        ),
    },
    {
        "id": "ge_proton_python_too_old",
        "patterns": (
            "AttributeError: 'str' object has no attribute 'removesuffix'",
        ),
        "summary": (
            "GE-Proton appears to be running with a Python version that is "
            "too old."
        ),
        "suggestion": (
            "GE-Proton 10 uses Python features that require Python 3.9 or newer. "
            "Use a newer host Python, a different Proton build, or run with a "
            "Steam Runtime/container setup that provides a compatible Python."
        ),
    },
)


def diagnose_proton_output(output):
    """
    Return known Proton launch diagnoses found in captured output.

    output: Combined stdout/stderr from the Proton helper process.
    """
    if not output:
        return []

    diagnoses = []
    for item in _PROTON_OUTPUT_PATTERNS:
        if any(pattern in output for pattern in item["patterns"]):
            diagnoses.append({
                "id": item["id"],
                "summary": item["summary"],
                "suggestion": item["suggestion"],
            })
    return diagnoses


def log_proton_diagnostics(output):
    """Log human-readable diagnostics for known Proton launch failures."""
    diagnoses = diagnose_proton_output(output)
    for diagnosis in diagnoses:
        logging.warning(
            "Detected Proton launch issue (%s): %s\n%s",
            diagnosis["id"],
            diagnosis["summary"],
            diagnosis["suggestion"],
        )
    return diagnoses
