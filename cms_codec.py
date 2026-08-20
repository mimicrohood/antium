#!/usr/bin/env python3
"""Framer CMS chunk codec — parse to model and re-serialize byte-exact.

Grammar (reverse engineered):
  chunk = [u32 recordCount] record*
  record = [0x00 marker] [u8 fieldCount] field*
  field  = KEY VALUE
  KEY    = [u32 len][utf8 bytes]           (bare, no tag)
  VALUE  = [tag byte][payload]:
     0x0c string : [u32 len][utf8 bytes]
     0x04 date   : [8 bytes]
     0x08 double : [8 bytes]
     0x0b rich   : [1 byte kind][u32 len][utf8 bytes]
     0x01 ??? we will detect payload length empirically
"""
import sys, struct

def u32(d,p): return struct.unpack('>I', d[p:p+4])[0]

def parse(data):
    n=len(data)
    recCount = u32(data,0)
    i=4
    records=[]
    while i < n and data[i]==0x00:
        i+=1
        fc=data[i]; i+=1
        fields=[]
        for _ in range(fc):
            klen=u32(data,i); i+=4
            key=data[i:i+klen].decode('utf-8'); i+=klen
            tag=data[i]; i+=1
            if tag==0x0c:
                vlen=u32(data,i); i+=4
                val=data[i:i+vlen]; i+=vlen
                fields.append([key,'str',val])
            elif tag==0x04:
                val=data[i:i+8]; i+=8
                fields.append([key,'date',val])
            elif tag==0x08:
                val=data[i:i+8]; i+=8
                fields.append([key,'dbl',val])
            elif tag==0x0b:
                kind=data[i]; i+=1
                vlen=u32(data,i); i+=4
                val=data[i:i+vlen]; i+=vlen
                fields.append([key,'rich',(kind,val)])
            elif tag==0x01:
                # relation field: [u16 count] then count * (0x0c str-ref)
                cnt=struct.unpack('>H', data[i:i+2])[0]; i+=2
                refs=[]
                for _ in range(cnt):
                    rtag=data[i]; i+=1
                    assert rtag==0x0c, f"relation entry tag 0x{rtag:02x} @{i-1}"
                    rlen=u32(data,i); i+=4
                    refs.append(data[i:i+rlen].decode('utf-8')); i+=rlen
                fields.append([key,'rel',refs])
            else:
                raise ValueError(f"unknown tag 0x{tag:02x} at {i-1}, ctx={data[i-1:i+11].hex()}")
        records.append(fields)
    return recCount, records, i

def serialize(recCount, records):
    out=bytearray()
    out+=struct.pack('>I', recCount)
    for fields in records:
        out+=b'\x00'
        out+=bytes([len(fields)])
        for key,typ,val in fields:
            kb=key.encode('utf-8')
            out+=struct.pack('>I',len(kb)); out+=kb
            if typ=='str':
                out+=b'\x0c'; out+=struct.pack('>I',len(val)); out+=val
            elif typ=='date':
                out+=b'\x04'; out+=val
            elif typ=='dbl':
                out+=b'\x08'; out+=val
            elif typ=='rich':
                kind,v=val
                out+=b'\x0b'; out+=bytes([kind]); out+=struct.pack('>I',len(v)); out+=v
            elif typ=='rel':
                out+=b'\x01'; out+=struct.pack('>H',len(val))
                for r in val:
                    rb=r.encode('utf-8')
                    out+=b'\x0c'; out+=struct.pack('>I',len(rb)); out+=rb
            else:
                raise ValueError(typ)
    return bytes(out)

if __name__=='__main__':
    data=open(sys.argv[1],'rb').read()
    rc,recs,end=parse(data)
    re=serialize(rc,recs)
    ok = (re==data)
    print(f"recCount={rc} records={len(recs)} parsed_end={end}/{len(data)} roundtrip={'OK' if ok else 'MISMATCH'}")
    if not ok:
        # find first diff
        for k in range(min(len(re),len(data))):
            if re[k]!=data[k]:
                print(f"first diff @{k}: orig={data[k-4:k+8].hex()} new={re[k-4:k+8].hex()}")
                break
        print(f"len orig={len(data)} new={len(re)}")
    else:
        # dump field summary
        for ri,fields in enumerate(recs):
            print(f"--- record {ri} ---")
            for key,typ,val in fields:
                if typ in ('str','rich'):
                    v = val if typ=='str' else val[1]
                    s = v.decode('utf-8',errors='replace')
                    print(f"   {key} [{typ}] ({len(v)}B) {s[:70]!r}")
                elif typ=='rel':
                    print(f"   {key} [rel] {val}")
                else:
                    print(f"   {key} [{typ}] {val.hex() if isinstance(val,bytes) else val}")
