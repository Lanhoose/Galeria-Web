from pathlib import Path
import zipfile,hashlib,json
base=Path(__file__).resolve().parent.parent
app=base/'app'
manifest=json.loads((app/'assets/integridade.json').read_text())
for name,digest in manifest['arquivos'].items():
 assert hashlib.sha256((app/name).read_bytes()).hexdigest()==digest,name
out=base/'release';out.mkdir(exist_ok=True)
archive=out/'Roleta_Pokemon_100_Offline_Completo.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for f in sorted(app.rglob('*')):
  if not f.is_file():continue
  info=zipfile.ZipInfo(f.relative_to(app).as_posix(),date_time=(2026,11,10,0,0,0))
  info.compress_type=zipfile.ZIP_DEFLATED
  info.external_attr=0o100644<<16
  info.create_system=3
  z.writestr(info,f.read_bytes(),compresslevel=6)
with zipfile.ZipFile(archive) as z:assert z.testzip() is None
sha=hashlib.sha256(archive.read_bytes()).hexdigest()
archive.with_suffix('.zip.sha256').write_text(sha+'  '+archive.name+'\n')
print(json.dumps({'arquivo':archive.name,'bytes':archive.stat().st_size,'sha256':sha,'arquivos_verificados':len(manifest['arquivos'])}))
