import sys
import os
import argparse
import subprocess
root_dir = os.path.dirname(os.path.abspath(__file__))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)
from core.agent import Nexus226Agent
from core.voice_loop import ConversationalCallLoop

def run_text_loop(agent: Nexus226Agent):
    print('\n' + '=' * 65)
    print(' [NEXUS-226] AUTONOMOUS OFFLINE AI (TEXT TERMINAL)')
    print(' 226 AI Paradigms | Machine Control | Blockchain Transactions')
    print(" Type 'exit' or 'quit' to terminate session.")
    print('=' * 65 + '\n')
    while True:
        try:
            query = input('\n[Nexus-226 User] >> ')
            if not query.strip():
                continue
            if query.strip().lower() in ['exit', 'quit', 'shutdown']:
                print('Terminating Nexus-226 session.')
                break
            response = agent.process_request(query)
            print(f'\n[Nexus-226 AI]:\n{response}')
        except (KeyboardInterrupt, EOFError):
            print('\nSession interrupted. Exiting.')
            break

def run_voice_loop(agent: Nexus226Agent):
    call = ConversationalCallLoop(agent_responder=agent.process_request)
    call.start_call()

def run_gui():
    print('[Nexus-226] Launching Streamlit Web Cockpit...')
    script_path = os.path.join(root_dir, 'web_ui.py')
    subprocess.run([sys.executable, '-m', 'streamlit', 'run', script_path])

def main():
    parser = argparse.ArgumentParser(description='Nexus-226: Autonomous Offline AI Agent')
    parser.add_argument('--mode', choices=['voice', 'text', 'gui'], default='voice', help='Operating mode: voice (Always-On Call), text (CLI), or gui (Streamlit Cockpit)')
    parser.add_argument('query', nargs='*', help='Optional single-shot query/command to run immediately')
    args = parser.parse_args()
    if args.query:
        agent = Nexus226Agent()
        full_query = ' '.join(args.query)
        result = agent.process_request(full_query)
        print(result)
        return
    if args.mode == 'gui':
        run_gui()
    elif args.mode == 'text':
        agent = Nexus226Agent()
        run_text_loop(agent)
    else:
        agent = Nexus226Agent()
        run_voice_loop(agent)
if __name__ == '__main__':
    main()
