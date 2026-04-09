from pathlib import Path
import json

from ollama_client import ask_ollama

LOG_DIR = Path("logs")


def choose_log_file(files: list[Path]) -> Path:
    for i, file in enumerate(files, start=1):
        print(f"{i}. {file.name}")

    while True:
        choice = input("Which log file do you want to analyze? ").strip()

        if not choice.isdigit():
            print("Please enter a valid number.")
            continue

        choice_num = int(choice)

        if 1 <= choice_num <= len(files):
            return files[choice_num - 1]

        print("That number is not in the list.")


def build_prompt(file_name: str, log_text: str) -> str:
    return f"""
Analyze this Linux log file: {file_name}

Tasks:
1. Summarize the main problems.
2. List confirmed errors from most critical to least critical.
3. List warnings.
4. List security-relevant events.
5. List possible high-level causes.
6. List recommended next steps.

Rules:
- Use only evidence explicitly present in the log.
- Do not invent facts.
- Do not say the system is healthy or started successfully unless the log explicitly says so.
- Do not treat normal CRON activity, normal systemd start/finish messages, or successful logins as errors.
- Treat failed SSH logins as security-relevant.
- Treat OOM kills, filesystem errors, repeated HTTP 500 errors, PostgreSQL connection errors, and Docker/container failures as important when present.
- possible_causes must be short explanations, not copied log lines.
- If a section has no items, return an empty list.
- Keep the response concise.

Log contents:
{log_text}
""".strip()


def normalize_list(items) -> list[str]:
    if not isinstance(items, list):
        return []

    normalized = []
    for item in items:
        if isinstance(item, str):
            cleaned = item.strip()
            if cleaned and cleaned.lower() != "string":
                normalized.append(cleaned)
        elif isinstance(item, dict):
            parts = [str(value).strip() for value in item.values() if str(value).strip()]
            if parts:
                joined = " | ".join(parts)
                if joined.lower() != "string":
                    normalized.append(joined)
        else:
            cleaned = str(item).strip()
            if cleaned and cleaned.lower() != "string":
                normalized.append(cleaned)

    return normalized


def dedupe_list(items: list[str]) -> list[str]:
    seen = set()
    deduped = []

    for item in items:
        key = item.strip().lower()
        if key and key not in seen:
            seen.add(key)
            deduped.append(item)

    return deduped


def clean_possible_causes(items: list[str]) -> list[str]:
    cleaned = []

    for item in items:
        lower_item = item.lower().strip()

        if lower_item == "string":
            continue

        if any(token in lower_item for token in [
            "cron[",
            "systemd[",
            "sshd[",
            "nginx[",
            "postgres[",
            "docker[",
            "kernel:",
            "cmd (",
            "accepted password",
            "connection closed by authenticating user"
        ]):
            continue

        cleaned.append(item)

    if not cleaned:
        return ["Unclear from the log"]

    return cleaned


def normalize_result(result: dict) -> dict:
    summary = str(result.get("summary", "No summary provided.")).strip()
    if summary.lower() == "string":
        summary = "Model returned placeholder text instead of real analysis."

    normalized = {
        "summary": summary,
        "confirmed_errors": dedupe_list(normalize_list(result.get("confirmed_errors", []))),
        "warnings": dedupe_list(normalize_list(result.get("warnings", []))),
        "security_events": dedupe_list(normalize_list(result.get("security_events", []))),
        "possible_causes": clean_possible_causes(
            dedupe_list(normalize_list(result.get("possible_causes", [])))
        ),
        "recommended_next_steps": dedupe_list(
            normalize_list(result.get("recommended_next_steps", []))
        ),
    }

    return normalized


def print_section(title: str, items: list[str]) -> None:
    print(f"\n{title}:")
    if items:
        for i, item in enumerate(items, start=1):
            print(f"{i}. {item}")
    else:
        print("None")


def print_report(result: dict) -> None:
    print("\n=== Analysis Result ===\n")

    print("Summary:")
    print(result["summary"] if result["summary"] else "No summary provided.")

    print_section("Confirmed Errors", result["confirmed_errors"])
    print_section("Warnings", result["warnings"])
    print_section("Security Events", result["security_events"])
    print_section("Possible Causes", result["possible_causes"])
    print_section("Recommended Next Steps", result["recommended_next_steps"])


def main() -> None:
    if not LOG_DIR.exists():
        print(f"Error: '{LOG_DIR}' folder does not exist.")
        return

    files = [file for file in LOG_DIR.iterdir() if file.is_file()]

    if not files:
        print(f"No log files found in '{LOG_DIR}'.")
        return

    selected_file = choose_log_file(files)
    log_text = selected_file.read_text(encoding="utf-8", errors="replace")

    max_chars = 12000
    if len(log_text) > max_chars:
        log_text = log_text[:max_chars]

    prompt = build_prompt(selected_file.name, log_text)

    print("\nAnalyzing log file...\n")
    reply = ask_ollama(prompt)

    print("=== Raw Model Reply ===")
    print(reply)
    print("=== End Raw Model Reply ===")

    try:
        result = json.loads(reply)
        normalized_result = normalize_result(result)
        print_report(normalized_result)
    except json.JSONDecodeError:
        print("\nModel did not return valid JSON.")
        print("Raw response above could not be parsed.")


if __name__ == "__main__":
    main()