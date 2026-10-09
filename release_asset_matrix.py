"""Check captured GitHub release metadata against a declared platform-asset matrix."""
import argparse
import json
import re
import string
from pathlib import Path
from urllib.parse import urlsplit, unquote


def contract(p):
    required = {'repository','tag','template','cells','min_size','require_digest','allow_prerelease'}
    if not isinstance(p,dict) or set(p) != required:
        raise ValueError('invalid contract fields')
    if not isinstance(p['repository'],str) or not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+',p['repository']):
        raise ValueError('repository must be owner/name')
    if not isinstance(p['tag'],str) or not re.fullmatch(r'[A-Za-z0-9_.-]{1,100}',p['tag']):
        raise ValueError('tag must be a safe literal name')
    if type(p['min_size']) is not int or p['min_size'] < 1 or any(type(p[k]) is not bool for k in ('require_digest','allow_prerelease')):
        raise ValueError('invalid size or boolean policy')
    if not isinstance(p['template'],str) or len(p['template']) > 200:
        raise ValueError('invalid template')
    for _, field, spec, conversion in string.Formatter().parse(p['template']):
        if field is not None and (field not in ('tag','os','arch','ext') or spec or conversion):
            raise ValueError('template allows only tag/os/arch/ext without formatting')
    if not isinstance(p['cells'],list) or not 1 <= len(p['cells']) <= 1000:
        raise ValueError('one to 1000 platform cells required')
    names = set()
    targets = []
    for cell in p['cells']:
        if not isinstance(cell,dict) or set(cell) != {'os','arch','ext'} or any(not isinstance(v,str) or not re.fullmatch(r'[A-Za-z0-9_.-]{1,50}',v) for v in cell.values()):
            raise ValueError('cell needs safe literal os, arch, ext')
        filename = p['template'].format(tag=p['tag'],**cell)
        if not re.fullmatch(r'[A-Za-z0-9_.-]{1,255}',filename) or filename in names:
            raise ValueError('matrix names collide or are unsafe')
        names.add(filename)
        targets.append((cell,filename))
    return targets


def audit(release,p):
    targets = contract(p)
    if not isinstance(release,dict) or not {'tag_name','draft','prerelease','assets'} <= set(release):
        raise ValueError('release metadata missing required fields')
    if not isinstance(release['tag_name'],str) or type(release['draft']) is not bool or type(release['prerelease']) is not bool or not isinstance(release['assets'],list) or len(release['assets']) > 10000:
        raise ValueError('invalid release metadata types')
    findings = []
    def add(code,**details):
        findings.append(dict(code=code,**details))
    if release['tag_name'] != p['tag']:
        add('tag_mismatch')
    if release['draft']:
        add('draft_release')
    if release['prerelease'] and not p['allow_prerelease']:
        add('prerelease')
    assets = {}
    ids = set()
    for a in release['assets']:
        if not isinstance(a,dict) or not {'id','name','size','state','browser_download_url'} <= set(a) or type(a['id']) is not int or a['id'] < 1 or not isinstance(a['name'],str) or type(a['size']) is not int or a['size'] < 0 or not isinstance(a['state'],str) or not isinstance(a['browser_download_url'],str):
            raise ValueError('invalid asset metadata')
        if a['id'] in ids:
            add('duplicate_asset_id',id=a['id'])
        ids.add(a['id'])
        assets.setdefault(a['name'],[]).append(a)
    coverage = []
    for cell,filename in targets:
        candidates = assets.get(filename,[])
        start = len(findings)
        if len(candidates) != 1:
            add('asset_count',name=filename,actual=len(candidates))
        else:
            a = candidates[0]
            if a['state'] != 'uploaded':
                add('asset_state',name=filename,state=a['state'])
            if a['size'] < p['min_size']:
                add('asset_size',name=filename,actual=a['size'])
            u = urlsplit(a['browser_download_url'])
            expected = '/'+p['repository']+'/releases/download/'+p['tag']+'/'+filename
            if u.scheme != 'https' or u.netloc != 'github.com' or unquote(u.path) != expected or u.query or u.fragment:
                add('asset_url',name=filename)
            digest = a.get('digest')
            if p['require_digest'] and (not isinstance(digest,str) or not re.fullmatch(r'sha256:[0-9a-f]{64}',digest)):
                add('asset_digest_metadata',name=filename)
        coverage.append(dict(**cell,name=filename,covered=len(findings)==start))
    return dict(repository=p['repository'],tag=p['tag'],matrix=coverage,findings=findings,
                extra_assets=sorted(set(assets)-{filename for _,filename in targets}))


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('release')
    ap.add_argument('contract')
    args = ap.parse_args()
    try:
        raw = Path(args.release).read_bytes()
        if len(raw) > 2*1024*1024:
            raise ValueError('release snapshot exceeds 2 MiB')
        result = audit(json.loads(raw),json.loads(Path(args.contract).read_text()))
        print(json.dumps(result,sort_keys=True))
        return int(bool(result['findings']))
    except (ValueError,OSError,UnicodeError,TypeError) as e:
        print(json.dumps({'error':str(e)}))
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
