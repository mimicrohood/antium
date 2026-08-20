#!/usr/bin/env python3
"""Lossless Framer CMS index codec.

The index is a sequence of sections. Within it, the only things that reference
the chunk are 10-byte record pointers: [u16 0x0000][u32 chunkOffset][u32 recordLen].
Everything else is: length-prefixed strings (bare u32-len key names, and 0x0c-tagged
value strings) plus structural bytes.

Strategy for a lossless, editable model:
  tokenize into a flat list of tokens:
    ('ptr', record_id)                      # a 10-byte pointer -> resolved to a record id
    ('str0c', bytes)                        # 0x0c-tagged value string
    ('strbare', bytes)                      # bare u32-len string (>=2 printable) NOT preceded by 0x0c
    ('raw', bytes)                          # literal bytes
Re-emit reproduces the file exactly.

For editing: pointers are re-resolved from a {record_id: (off,len)} map produced by the
new chunk; 0x0c value strings that equal an OLD content string are swapped for the NEW one.
"""
import sys, struct

def build_tokens(data, ptr_index):
    """ptr_index: dict mapping (off,len)->record_id for ORIGINAL records."""
    n=len(data); i=0; toks=[]
    rawbuf=bytearray()
    def flush():
        if rawbuf:
            toks.append(('raw', bytes(rawbuf))); rawbuf.clear()
    while i < n:
        # try 10-byte pointer: 00 00 <off u32> <len u32>
        if i+10<=n and data[i]==0 and data[i+1]==0:
            off=struct.unpack('>I',data[i+2:i+6])[0]
            ln =struct.unpack('>I',data[i+6:i+10])[0]
            if (off,ln) in ptr_index:
                flush(); toks.append(('ptr', ptr_index[(off,ln)])); i+=10; continue
        # try 0x0c-tagged string
        if data[i]==0x0c and i+5<=n:
            ln=struct.unpack('>I',data[i+1:i+5])[0]
            if 0<ln<=100000 and i+5+ln<=n:
                s=data[i+5:i+5+ln]
                flush(); toks.append(('str0c', s)); i+=5+ln; continue
        rawbuf.append(data[i]); i+=1
    flush()
    return toks

def emit(toks, ptr_map):
    out=bytearray()
    for t in toks:
        if t[0]=='raw': out+=t[1]
        elif t[0]=='str0c':
            out+=b'\x0c'+struct.pack('>I',len(t[1]))+t[1]
        elif t[0]=='ptr':
            off,ln=ptr_map[t[1]]
            out+=b'\x00\x00'+struct.pack('>II',off,ln)
        else: raise ValueError(t[0])
    return bytes(out)

if __name__=='__main__':
    sys.path.insert(0, r"C:\Users\Administrator\Desktop\rayoid")
    from cms_codec import parse, serialize
    chunk=open(sys.argv[1],'rb').read()
    index=open(sys.argv[2],'rb').read()
    rc,recs,end=parse(chunk)
    # original record ranges
    off=4; ptr_index={}; ptr_map={}
    for fields in recs:
        rid=[v for k,t,v in fields if k=='id'][0].decode()
        rb=serialize(1,[fields])[4:]
        ptr_index[(off,len(rb))]=rid
        ptr_map[rid]=(off,len(rb))
        off+=len(rb)
    toks=build_tokens(index, ptr_index)
    re=emit(toks, ptr_map)
    ok = re==index
    print(f"tokens={len(toks)} roundtrip={'OK' if ok else 'MISMATCH'} origlen={len(index)} newlen={len(re)}")
    if not ok:
        for k in range(min(len(re),len(index))):
            if re[k]!=index[k]:
                print(f"first diff @{k}: orig={index[max(0,k-4):k+8].hex()} new={re[max(0,k-4):k+8].hex()}")
                break
    else:
        nptr=sum(1 for t in toks if t[0]=='ptr')
        nstr=sum(1 for t in toks if t[0]=='str0c')
        print(f"pointers={nptr} str0c={nstr}")
