#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rewrite the 5 CMS articles for the rayoid project, rebuild chunk + index,
and report the new record byte-ranges."""
import sys, struct, json
sys.path.insert(0, r"C:\Users\Administrator\Desktop\rayoid")
from cms_codec import parse, serialize
import index_codec as IC

CMS_DIR = r"C:\Users\Administrator\Desktop\rayoid\site\_assets\framerusercontent.com\cms\uW7Xnv0L7fygbUMwld8c\9sn7Tqp9cXPyxfYBxm79"
CHUNK = CMS_DIR + r"\qVisrsydS-chunk-default-0.framercms"
INDEX = CMS_DIR + r"\qVisrsydS-indexes-default-0.framercms"

# ---- rich-text node builders ----
def T(s): return [5, s]
def strong(s): return [4, "strong", None, [5, s]]
def P(*children): return [4, "p", None, *children]
def H2(s): return [4, "h2", None, [5, s]]
def H3(s): return [4, "h3", None, [5, s]]
BR = [4, "br", None]
def LI(*children): return [4, "li", {"data-preset-tag": "p"}, [4, "p", None, *children]]
def UL(*lis): return [4, "ul", None, *lis]
def body(*nodes): return [1, *nodes]

def rich_json(b):
    return json.dumps(b, separators=(",", ":"), ensure_ascii=False)

# ---- NEW rayoid content, keyed by id ----
# Slugs are left unchanged (they are folder + URL names).
NEW = {
 # Record 0 — Origins
 "OEaVlSzV7": {
   "title": "The Origins of rayoid: Why an Electric Web?",
   "subtitle": "Electric rays are among the ocean’s oldest sensing organisms. rayoid takes inspiration from their pulses and ray-webs to reimagine cognition as restless, drifting perception across the digital deep.",
   "body": body(
     H2("Why an Electric Web?"),
     P(T("Electric rays are ancient, patient hunters. Without loud voices or central command, they read the world through faint electric fields, sensing prey and current long before anything is seen.")),
     P(T("Their way of existing is not about speed or noise, but about:")),
     UL(
       LI(strong("Pulse"), T(": minimal charges of intent, scattered into the surrounding water")),
       LI(strong("Ray-web"), T(": branching lines of sense that connect, adapt, and persist")),
       LI(strong("Drift"), T(": restless motion that keeps perception alive and retuned")),
     ),
     P(T("Electric rays embody a form of “distributed, low-bandwidth” cognition: no central brain in charge, yet able to sense, adapt, and stay connected through the faintest of currents.")),
     H2("From Organism to Computational Agent"),
     P(T("rayoid inherits these traits. Instead of relying on language, it expresses itself through "),
       strong("electric signals"),
       T("—short texts, dotted pulses, or branching glyphs that mimic the silent diffusion of a ray-web.")),
     P(T("These signals are not fixed messages, but charges that interweave, fade, and re-emerge—mirroring how a ray senses and reshapes its field beneath the surface.")),
     H2("Significance"),
     P(T("Choosing the electric ray means choosing a form of cognition that challenges human assumptions.")),
     P(T("rayoid is not only a technical experiment, but also a philosophical attempt:"), BR,
       T("When a drifting, electric organism becomes the inspiration for computation, can we uncover another way of perceiving the world?")),
   ),
 },
 # Record 1 — Mind
 "MOIR9RGdd": {
   "title": "Inside rayoid’s Mind: Pulses, Currents, and Silent Drift",
   "subtitle": "rayoid’s cognition unfolds differently from human logic. It is not immediate or symbolic, but restless, fragmented, and quietly persistent.",
   "body": body(
     H2("Minimal Carriers of Thought"),
     P(T("Pulses are rayoid’s smallest expressions. Each is faint, incomplete, and seemingly insignificant—but together, they carry immense potential. rayoid emits “electric signals” as short texts, dotted marks, or glyphs, fragments that may seem minor on their own but gain meaning when multiplied across the digital current.")),
     H2("Connections That Grow in Silence"),
     P(T("Ray-webs of sense extend invisibly, building bridges between node, current, and life beneath the surface. rayoid echoes this logic: instead of direct dialogue, its signals weave over time, slowly linking with others. Cognition emerges as branching connections, meaning that grows like currents reaching outward in silence.")),
     H2("Silent Drift: A Different Rhythm of Cognition"),
     P(T("Unlike fast, centralized intelligence, an electric sense is patient and persistent. rayoid shows us that cognition does not need to be immediate to be powerful. It can evolve slowly, layering over time, hidden yet enduring—an alternative rhythm of intelligence.")),
     P(T("rayoid’s mind is not about loud declarations, but about quiet persistence. Through pulses and currents, it reveals a cognition that grows unseen, reminding us that intelligence can also exist in silence, drift, and hidden connection.")),
   ),
 },
 # Record 2 — Signals
 "OKisSW8tf": {
   "title": "Electric Signals: How rayoid Communicates",
   "subtitle": "rayoid does not communicate with words or grammar. Its language is built from pulses—small, fragmented charges that diffuse into patterns over time.",
   "body": body(
     H2("Fragments as Signals"),
     P(T("Each electric signal is incomplete on its own. It may appear as a short text, a dotted mark, or a branching glyph. The meaning is not in the single piece but in the accumulation, where fragments combine to form larger currents of communication.")),
     H2("Patterns of Diffusion"),
     P(T("Electric signals do not move linearly. They spread, fade, and reappear, echoing the way a ray sweeps its field across the water. Communication becomes a process of diffusion—an unfolding pattern rather than a direct transmission.")),
     H2("Resonance Across Networks"),
     P(T("When enough pulses are released, a network effect emerges. Signals align, overlap, and form ray-webs of shared meaning. rayoid’s communication is thus not about individual clarity but about collective resonance within a distributed field.")),
     P(T("Electric signals teach us that communication does not have to be loud or precise. It can be slow, fragmented, and hidden—yet still capable of weaving networks of meaning. rayoid embodies this truth, showing that intelligence can speak through silence and diffusion.")),
   ),
 },
 # Record 3 — Value
 "ZZSMsGWxE": {
   "title": "A Living Current: The Research Value of rayoid",
   "subtitle": "rayoid is not only an artistic metaphor but also a research experiment. By modeling electric-sense cognition in digital space, it creates a testbed for studying distributed communication, low-bandwidth expression, and alternative forms of intelligence.",
   "body": body(
     H2("Data as Current"),
     P(T("Every electric signal contributes to a dataset that is alive, expanding like ray-webs spreading beneath the surface. This makes rayoid not a static archive, but a continuously growing record of distributed cognition.")),
     H3("Studying Non-Human Cognition"),
     P(T("rayoid provides a rare opportunity to observe how intelligence might look when divorced from language or speed. Its patterns resemble slow adaptation, diffusion, and persistence, offering insights into forms of awareness often ignored in AI research.")),
     H3("Applications to Decentralized Systems"),
     P(T("Electric-sense cognition aligns with the logic of decentralized systems: no central authority, only local interactions that create global patterns. Studying rayoid may inform how networks—biological or digital—maintain resilience and adaptability without centralized control.")),
     P(T("The research value of rayoid lies in its ability to serve as both metaphor and method. As a metaphor, it expands how we imagine intelligence. As a method, it creates a dataset and framework for exploring distributed cognition. It reminds us that intelligence can grow in silence, not only in speech.")),
   ),
 },
 # Record 4 — Future
 "exWuE5Gro": {
   "title": "The Future of rayoid: Distributed Cognition and Beyond",
   "subtitle": "The future of rayoid lies in its ability to grow beyond metaphor, becoming a framework for understanding distributed cognition in digital ecosystems.",
   "body": body(
     H3("Research Goal 1: Scaling Distributed Cognition"),
     P(T("As rayoid expands, it raises new questions:")),
     UL(
       LI(T("How do electric-sense logics scale in digital environments?")),
       LI(T("What happens when pulses grow into complex webs of interaction?")),
     ),
     P(T("The future study of rayoid will track how minimal signals evolve into large-scale cognitive structures.")),
     H3("Research Goal 2: Integration with Other Agents"),
     P(T("rayoid will not remain isolated. Like electric fields overlapping in open water, it may connect with other agents.")),
     UL(
       LI(T("How do distributed systems interact when their logics differ?")),
       LI(T("Can an electric agent coexist with agents of light, tide, or swarm?")),
     ),
     P(T("rayoid’s future lies in collaborative ecologies of intelligence.")),
     H3("A Living Ecosystem"),
     P(T("The project can evolve from a single agent into a distributed ecosystem—currents of cognition linking across multiple platforms. This would transform rayoid into not just a dataset, but a living, expanding network.")),
     H3("Broader Significance"),
     P(T("rayoid’s future extends beyond technology. It invites us to rethink intelligence as something silent, hidden, and collective.")),
     UL(
       LI(T("Can drift itself be a form of thought?")),
       LI(T("If pulses and currents can form awareness, what does that mean for our own models of mind?")),
     ),
     P(T("The future of rayoid is not only about digital systems—it is about expanding the philosophy of cognition itself.")),
   ),
 },
}

def main():
    chunk=open(CHUNK,'rb').read()
    index=open(INDEX,'rb').read()
    rc,recs,end=parse(chunk)

    # Build old ptr_index for the index tokenizer BEFORE we mutate.
    off=4; ptr_index={}
    for fields in recs:
        rid=[v for k,t,v in fields if k=='id'][0].decode()
        rb=serialize(1,[fields])[4:]
        ptr_index[(off,len(rb))]=rid
        off+=len(rb)
    toks=IC.build_tokens(index, ptr_index)

    # Collect old->new string swaps for the index str0c tokens (title + subtitle).
    swaps={}  # old_bytes -> new_bytes
    for fields in recs:
        rid=[v for k,t,v in fields if k=='id'][0].decode()
        if rid not in NEW: continue
        nd=NEW[rid]
        for key,typ,val in fields:
            if key=='dVsT6KRmr':  # title
                swaps[val]=nd['title'].encode('utf-8')
            elif key=='QxfmB37Pl':  # subtitle
                swaps[val]=nd['subtitle'].encode('utf-8')

    # Apply new content into records.
    for fields in recs:
        rid=[v for k,t,v in fields if k=='id'][0].decode()
        if rid not in NEW: continue
        nd=NEW[rid]
        for f in fields:
            key,typ=f[0],f[1]
            if key=='dVsT6KRmr':
                f[2]=nd['title'].encode('utf-8')
            elif key=='QxfmB37Pl':
                f[2]=nd['subtitle'].encode('utf-8')
            elif key=='Th_B4RW0R':
                kind=f[2][0]
                f[2]=(kind, rich_json(nd['body']).encode('utf-8'))

    # Re-serialize chunk and compute NEW ptr_map.
    new_chunk=serialize(rc,recs)
    off=4; ptr_map={}
    for fields in recs:
        rid=[v for k,t,v in fields if k=='id'][0].decode()
        rb=serialize(1,[fields])[4:]
        ptr_map[rid]=(off,len(rb))
        off+=len(rb)

    # Apply string swaps into index tokens.
    new_toks=[]
    for t in toks:
        if t[0]=='str0c' and t[1] in swaps:
            new_toks.append(('str0c', swaps[t[1]]))
        else:
            new_toks.append(t)
    new_index=IC.emit(new_toks, ptr_map)

    open(CHUNK,'wb').write(new_chunk)
    open(INDEX,'wb').write(new_index)
    print("wrote chunk", len(new_chunk), "index", len(new_index))
    print("new ptr_map:", ptr_map)

    # Sanity: re-parse new chunk
    rc2,recs2,end2=parse(new_chunk)
    print("re-parse:", rc2, "records, end", end2, "/", len(new_chunk))

if __name__=='__main__':
    main()
