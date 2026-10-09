import json
from pathlib import Path
import release_asset_matrix as m
p=json.loads(Path('contract.json').read_text());good=m.audit(json.loads(Path('release.json').read_text()),p);bad=m.audit(json.loads(Path('bad-release.json').read_text()),p)
assert not good['findings'] and bad['findings']
print(json.dumps({'good':good,'violation':bad},indent=2))
