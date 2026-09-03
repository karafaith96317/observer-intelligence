import json, tempfile, unittest
from pathlib import Path
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from src.oi_live_pilot import *

def ev(i="1", relation="SUPPORTS"): return Evidence("E"+i, "local://fixture", "2026-09-03T00:00:00Z", "payload"+i, relation, "Fixture directly supports claim")
def signed(rec, key, nonce="n"):
    p=token_payload(rec["claim_id"], "scope:pilot:dry-run", "local-pilot", nonce, 9999999999, rec["evidence_hashes"])
    return p, sign_token(key,p)

class AcceptanceTests(unittest.TestCase):
    def test_isolation_breach_rejected(self):
        e=ev(); c=Challenge("shadow","C","x",(e.content_hash,),())
        r=reconcile("C",[e],[c]); self.assertEqual(r["state"],"SUPPORTED"); self.assertEqual(r["rejected_challenges"][0]["reason"],"isolation_manifest_breach")
    def test_irrelevant_counterevidence_fails(self):
        e=ev(); c=Challenge("shadow","OTHER","x",(e.content_hash,),(e.content_hash,))
        r=reconcile("C",[e],[c]); self.assertEqual(r["state"],"SUPPORTED"); self.assertEqual(r["rejected_challenges"][0]["reason"],"wrong_target")
    def test_unsupported_contradiction_does_not_demote(self):
        e=ev(); c=Challenge("shadow","C","x",("missing",),("missing",))
        self.assertEqual(reconcile("C",[e],[c])["state"],"SUPPORTED")
    def test_weak_evidence_defaults_unresolved_and_denied(self):
        with tempfile.TemporaryDirectory() as d:
            e=ev(relation="INSUFFICIENT_FOR"); r=reconcile("C",[e],[]); self.assertEqual(r["state"],"UNRESOLVED")
            k=Ed25519PrivateKey.generate(); p,s=signed(r,k)
            a=authorize(r,p,s,k.public_key(),NonceStore(Path(d)/"n.db"),"scope:pilot:dry-run","local-pilot")
            self.assertEqual(a["decision"],"DENY"); self.assertFalse(a["checks"]["state_supported"]); self.assertTrue(a["checks"]["nonce_fresh"])
    def test_nonce_replay_rejected_after_restart(self):
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/"n.db"; e=ev(); r=reconcile("C",[e],[]); k=Ed25519PrivateKey.generate(); p,s=signed(r,k)
            self.assertEqual(authorize(r,p,s,k.public_key(),NonceStore(path),"scope:pilot:dry-run","local-pilot")["decision"],"ALLOW_DRY_RUN")
            self.assertEqual(authorize(r,p,s,k.public_key(),NonceStore(path),"scope:pilot:dry-run","local-pilot")["decision"],"DENY")
    def test_signature_mutation_fails(self):
        with tempfile.TemporaryDirectory() as d:
            e=ev(); r=reconcile("C",[e],[]); k=Ed25519PrivateKey.generate(); p,s=signed(r,k); p["resource"]="mutated"
            a=authorize(r,p,s,k.public_key(),NonceStore(Path(d)/"n.db"),"scope:pilot:dry-run","local-pilot")
            self.assertFalse(a["checks"]["signature_valid"])
    def test_chain_tamper_detected(self):
        with tempfile.TemporaryDirectory() as d:
            l=Ledger(Path(d)/"l.jsonl"); l.append({"x":1}); l.append({"x":2}); self.assertTrue(l.verify())
            rows=l.read(); rows[0]["payload"]["x"]=9; l.path.write_text("\n".join(json.dumps(x) for x in rows)+"\n")
            self.assertFalse(l.verify())

if __name__ == "__main__": unittest.main()
