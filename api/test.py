import argparse
import json
import sys
import requests


def run_non_streaming_query_sequence(
    api_url: str = "https://sight-achlzwosfa-ul.a.run.app/query",
    first_question: str = "How can I turn on the machine?",
    follow_up_question: str = "What was my previous question?",
) -> str | None:
    """
    Send two non-streaming requests: an initial question and a follow-up
    that reuses the returned conversation_id.

    Returns:
        The conversation_id from the first response (if available), else None.
    """
    payload = {"question": first_question}

    response = requests.post(api_url, json=payload)
    print("Status:", response.status_code)
    print("Body:", response.text)

    conv_id = None
    try:
        conv_id = response.json().get("conversation_id")
    except ValueError:
        pass

    payload = {"question": follow_up_question, "conversation_id": conv_id}
    response = requests.post(api_url, json=payload)
    print("Status:", response.status_code)
    print("Body:", response.text)

    return conv_id



def stream_query(
    api_url: str = "https://sight-142484475712.us-east5.run.app/stream",
    question: str = "What safety checks should I perform before jogging a UR5e robot?",
    conversation_id: str | None = None,
) -> str | None:
    """
    Send a POST to the streaming endpoint and print tokens as they arrive.

    Returns:
        The new or reused conversation_id (from the final 'done' event), or None on error.
    """
    payload = {
        "question": question,
        "conversation_id": conversation_id,
    }

    print(f"--> Sending request to {api_url}")
    print(f"--> Payload: {payload}")
    print("\n--- Streaming response ---\n")

    try:
        with requests.post(api_url, json=payload, stream=True) as resp:
            if resp.status_code != 200:
                print(f"Error: HTTP {resp.status_code}")
                print(resp.text)
                return None

            conv_id_from_server = None

            # SSE: each event is separated by a blank line; each line starting with 'data:'
            for raw_line in resp.iter_lines(decode_unicode=True):
                if raw_line is None:
                    continue

                line = raw_line.strip()
                if not line:
                    # blank line between SSE events
                    continue

                if not line.startswith("data:"):
                    # ignore comments or other SSE fields
                    continue

                try:
                    data_str = line[5:].strip()  # remove "data:"
                    event = json.loads(data_str)
                except json.JSONDecodeError:
                    print(f"\n[WARN] Could not parse JSON from line: {line}")
                    continue

                event_type = event.get("type")

                if event_type == "token":
                    token = event.get("token", "")
                    # Print token as it arrives
                    sys.stdout.write(token)
                    sys.stdout.flush()

                elif event_type == "done":
                    # Final message: contains full answer + conversation_id
                    answer = event.get("answer", "")
                    conv_id_from_server = event.get("conversation_id")
                    print("\n\n--- Stream complete ---")
                    print(f"Full answer length: {len(answer)} characters")
                    print(f"Conversation ID: {conv_id_from_server}")

                else:
                    # Any other event types (if you add them later)
                    print(f"\n[INFO] Other event: {event}")

            return conv_id_from_server

    except KeyboardInterrupt:
        print("\nInterrupted by user.")
        return None
    except Exception as e:
        print(f"\n[ERROR] Exception while streaming: {e}")
        return None


def main():
    conv_id_1 = run_non_streaming_query_sequence()
    conv_id_2 = stream_query()

if __name__ == "__main__":
    main()
