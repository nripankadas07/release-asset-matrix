import json
import unittest
from pathlib import Path
import release_asset_matrix as m


class Tests(unittest.TestCase):
    def setUp(self):
        self.r=json.loads(Path('release.json').read_text());self.p=json.loads(Path('contract.json').read_text())
    def codes(self):return {x['code'] for x in m.audit(self.r,self.p)['findings']}
    def test_valid(self):self.assertEqual(self.codes(),set())
    def test_missing(self):self.r['assets'].pop();self.assertIn('asset_count',self.codes())
    def test_duplicate_name(self):self.r['assets'].append(self.r['assets'][0].copy());self.assertIn('asset_count',self.codes())
    def test_duplicate_id(self):self.r['assets'][1]['id']=1;self.assertIn('duplicate_asset_id',self.codes())
    def test_state(self):self.r['assets'][0]['state']='starter';self.assertIn('asset_state',self.codes())
    def test_size(self):self.r['assets'][0]['size']=0;self.assertIn('asset_size',self.codes())
    def test_digest(self):self.r['assets'][0]['digest']='sha256:invalid';self.assertIn('asset_digest_metadata',self.codes())
    def test_url_origin(self):self.r['assets'][0]['browser_download_url']='https://github.com.evil.test/x';self.assertIn('asset_url',self.codes())
    def test_url_query(self):self.r['assets'][0]['browser_download_url']+='?secret=x';self.assertIn('asset_url',self.codes())
    def test_tag_draft(self):self.r['tag_name']='v0';self.r['draft']=True;self.assertTrue({'tag_mismatch','draft_release'} <= self.codes())
    def test_prerelease(self):self.r['prerelease']=True;self.assertIn('prerelease',self.codes())
    def test_collision(self):
        self.p['template']='same.zip'
        with self.assertRaises(ValueError):m.contract(self.p)
    def test_template_injection(self):
        self.p['template']='{tag.__class__}'
        with self.assertRaises(ValueError):m.contract(self.p)
    def test_bool_size(self):
        self.r['assets'][0]['size']=True
        with self.assertRaises(ValueError):m.audit(self.r,self.p)
    def test_metadata_only_digest(self):self.assertEqual(m.audit(self.r,self.p)['matrix'][0]['covered'],True)


if __name__=='__main__':unittest.main()
