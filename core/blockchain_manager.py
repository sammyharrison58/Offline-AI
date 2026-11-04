import os
import json
import time
import hmac
import hashlib
import secrets
from typing import Dict, Any, List, Optional
WALLETS_DIR = os.path.join(os.path.dirname(__file__), '..', 'wallets')
LEDGER_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'blockchain_ledger.json')

class BlockchainManager:

    def __init__(self, wallets_dir: str=WALLETS_DIR, ledger_file: str=LEDGER_FILE):
        self.wallets_dir = os.path.abspath(wallets_dir)
        self.ledger_file = os.path.abspath(ledger_file)
        os.makedirs(self.wallets_dir, exist_ok=True)
        os.makedirs(os.path.dirname(self.ledger_file), exist_ok=True)
        self.active_wallet: Optional[Dict[str, str]] = None
        self.ledger: List[Dict[str, Any]] = []
        self._load_ledger()
        self._init_default_wallet()

    @staticmethod
    def _keccak_or_sha256(data: bytes) -> str:
        return hashlib.sha256(data).hexdigest()

    def generate_wallet(self, label: str='primary', passphrase: str='') -> Dict[str, str]:
        priv_key_bytes = secrets.token_bytes(32)
        priv_hex = priv_key_bytes.hex()
        pub_digest = hashlib.sha256(b'PUB_KEY_SALT:' + priv_key_bytes).digest()
        address_raw = hashlib.sha256(pub_digest).hexdigest()[-40:]
        address = '0x' + address_raw
        wallet_data = {'label': label, 'address': address, 'created_at': time.time(), 'chain_compatibility': ['Ethereum', 'Polygon', 'Arbitrum', 'LocalChain']}
        if passphrase:
            salt = secrets.token_hex(16)
            kdf = hashlib.pbkdf2_hmac('sha256', passphrase.encode(), salt.encode(), 100000)
            stream_key = hashlib.sha256(kdf).digest()
            encrypted_priv = bytes((a ^ b for a, b in zip(priv_key_bytes, stream_key))).hex()
            wallet_data['encrypted_private_key'] = encrypted_priv
            wallet_data['salt'] = salt
            wallet_data['encrypted'] = True
        else:
            wallet_data['private_key'] = priv_hex
            wallet_data['encrypted'] = False
        keystore_path = os.path.join(self.wallets_dir, f'{label}_wallet.json')
        with open(keystore_path, 'w', encoding='utf-8') as f:
            json.dump(wallet_data, f, indent=2)
        self.active_wallet = {'label': label, 'address': address, 'private_key': priv_hex}
        return {'label': label, 'address': address, 'status': 'Wallet created and secured', 'keystore_path': keystore_path}

    def _init_default_wallet(self):
        default_file = os.path.join(self.wallets_dir, 'primary_wallet.json')
        if os.path.exists(default_file):
            try:
                with open(default_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.active_wallet = {'label': data.get('label', 'primary'), 'address': data.get('address', '0x0000000000000000000000000000000000000000'), 'private_key': data.get('private_key', '')}
            except Exception:
                self.generate_wallet('primary')
        else:
            self.generate_wallet('primary')

    def _load_ledger(self):
        if os.path.exists(self.ledger_file):
            try:
                with open(self.ledger_file, 'r', encoding='utf-8') as f:
                    self.ledger = json.load(f)
            except Exception:
                self.ledger = []
        else:
            self.ledger = []
        if not self.ledger:
            genesis_block = {'block_index': 0, 'timestamp': time.time(), 'transactions': [], 'previous_hash': '0' * 64, 'nonce': 42, 'block_hash': hashlib.sha256(b'GENESIS_BLOCK_NEXUS_226').hexdigest()}
            self.ledger.append(genesis_block)
            self._save_ledger()

    def _save_ledger(self):
        with open(self.ledger_file, 'w', encoding='utf-8') as f:
            json.dump(self.ledger, f, indent=2)

    def get_balance(self, address: Optional[str]=None) -> Dict[str, Any]:
        target_addr = address or (self.active_wallet['address'] if self.active_wallet else None)
        if not target_addr:
            return {'address': None, 'balance': 0.0}
        balance = 1000.0
        for block in self.ledger:
            for tx in block.get('transactions', []):
                if tx.get('to', '').lower() == target_addr.lower():
                    balance += float(tx.get('amount', 0.0))
                if tx.get('from', '').lower() == target_addr.lower():
                    balance -= float(tx.get('amount', 0.0)) + float(tx.get('fee', 0.0))
        return {'address': target_addr, 'balance': round(balance, 4), 'symbol': 'AETH (Nexus Autonomous Token)'}

    def create_and_sign_transaction(self, to_address: str, amount: float, memo: str='', fee: float=0.001) -> Dict[str, Any]:
        if not self.active_wallet:
            return {'success': False, 'error': 'No active wallet loaded.'}
        sender = self.active_wallet['address']
        priv_key = self.active_wallet.get('private_key', '')
        curr_balance = self.get_balance(sender)['balance']
        total_debit = amount + fee
        if curr_balance < total_debit:
            return {'success': False, 'error': f'Insufficient funds: Balance is {curr_balance}, required {total_debit}'}
        tx_payload = {'from': sender, 'to': to_address, 'amount': float(amount), 'fee': float(fee), 'timestamp': time.time(), 'nonce': len(self.ledger), 'memo': memo}
        payload_str = json.dumps(tx_payload, sort_keys=True)
        tx_hash = hashlib.sha256(payload_str.encode()).hexdigest()
        sig = hmac.new(priv_key.encode() if priv_key else b'offline_key', tx_hash.encode(), hashlib.sha256).hexdigest()
        tx_payload['signature'] = sig
        tx_payload['tx_hash'] = tx_hash
        new_block = self._mine_block([tx_payload])
        return {'success': True, 'tx_hash': tx_hash, 'signature': sig, 'block_index': new_block['block_index'], 'block_hash': new_block['block_hash'], 'from': sender, 'to': to_address, 'amount': amount, 'new_balance': self.get_balance(sender)['balance'], 'memo': memo}

    def _mine_block(self, transactions: List[Dict[str, Any]]) -> Dict[str, Any]:
        prev_block = self.ledger[-1]
        prev_hash = prev_block['block_hash']
        block_index = len(self.ledger)
        nonce = 0
        while True:
            candidate = f'{block_index}:{prev_hash}:{json.dumps(transactions)}:{nonce}'
            b_hash = hashlib.sha256(candidate.encode()).hexdigest()
            if b_hash.startswith('00'):
                break
            nonce += 1
        block = {'block_index': block_index, 'timestamp': time.time(), 'transactions': transactions, 'previous_hash': prev_hash, 'nonce': nonce, 'block_hash': b_hash}
        self.ledger.append(block)
        self._save_ledger()
        return block

    def get_transaction_history(self, limit: int=10) -> List[Dict[str, Any]]:
        all_txs = []
        for block in reversed(self.ledger):
            for tx in block.get('transactions', []):
                tx_copy = dict(tx)
                tx_copy['block_index'] = block['block_index']
                all_txs.append(tx_copy)
                if len(all_txs) >= limit:
                    return all_txs
        return all_txs
if __name__ == '__main__':
    bm = BlockchainManager()
    print('Active Wallet:', bm.active_wallet)
    print('Initial Balance:', bm.get_balance())
    res = bm.create_and_sign_transaction('0x71C8360537B882E130420666060021b59E874da7', 25.5, memo='Autonomous Cloud Compute Payment')
    print('Transaction Result:', res)
    print('Updated Balance:', bm.get_balance())
