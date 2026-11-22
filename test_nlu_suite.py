import sys
import os

sys.path.insert(0, r"F:\vscode projects\offline AI")
from core.agent import Nexus226Agent

def run_nlu_suite():
    agent = Nexus226Agent()
    passed = 0
    total = 0

    test_cases = [
        ("can you please open files", lambda r: "File Explorer" in r),
        ("could you launch vscode", lambda r: "Visual Studio Code" in r),
        ("please pull up my files", lambda r: "File Explorer" in r),
        ("can you pop open chrome", lambda r: "Google Chrome" in r or "browser" in r),
        ("would you fire up terminal", lambda r: "PowerShell Terminal" in r),
        ("file", lambda r: "File Explorer" in r),
        ("files", lambda r: "File Explorer" in r),
        ("vscode", lambda r: "Visual Studio Code" in r),
        ("code editor", lambda r: "Visual Studio Code" in r),
        ("how much juice is left", lambda r: "Battery" in r or "Hardware" in r),
        ("how much ram do i have", lambda r: "RAM" in r or "Hardware" in r),
        ("is my pc lagging", lambda r: "CPU" in r or "Hardware" in r),
        ("can you take a pic of my screen", lambda r: "Screenshot" in r),
        ("snap the screen", lambda r: "Screenshot" in r),
        ("can you make it louder", lambda r: "Volume increased" in r),
        ("shut up", lambda r: "mute" in r.lower()),
        ("turn down the noise", lambda r: "Volume decreased" in r),
        ("sounds good", lambda r: "Awesome" in r),
        ("catch you later", lambda r: "Take care" in r),
        ("can you understand natural language", lambda r: "natural human language" in r),
        ("what does bite the bullet mean", lambda r: "courage" in r or "bullet" in r),
        ("this bug is driving me crazy", lambda r: "frustration" in r or "debugging" in r)
    ]

    print("======================================================================")
    print(" >>> RUNNING COMPREHENSIVE NATURAL LANGUAGE UNDERSTANDING (NLU) SUITE")
    print("======================================================================")

    for query, validator in test_cases:
        total += 1
        res = agent.process_request(query)
        ok = validator(res)
        status = "[PASS]" if ok else "[FAIL]"
        if ok:
            passed += 1
        print(f"{status} Query: '{query}' -> {res[:75]}...")

    print("======================================================================")
    print(" >>> TESTING MULTI-TURN CONTEXTUAL PRONOUN RESOLUTION")
    print("======================================================================")

    total += 1
    t1 = agent.process_request("how much ram do i have")
    t2 = agent.process_request("what about cpu")
    if "CPU:" in t2:
        passed += 1
        print(f"[PASS] Multi-turn Follow-up: 'what about cpu' -> {t2}")
    else:
        print(f"[FAIL] Multi-turn Follow-up: 'what about cpu' -> {t2}")

    total += 1
    t3 = agent.process_request("what about battery")
    if "Battery:" in t3:
        passed += 1
        print(f"[PASS] Multi-turn Follow-up: 'what about battery' -> {t3}")
    else:
        print(f"[FAIL] Multi-turn Follow-up: 'what about battery' -> {t3}")

    print("======================================================================")
    print(f" >>> NLU TEST RESULTS: {passed}/{total} PASSED ({passed/total*100:.1f}%)")
    print("======================================================================")
    return passed == total

if __name__ == "__main__":
    success = run_nlu_suite()
    sys.exit(0 if success else 1)
