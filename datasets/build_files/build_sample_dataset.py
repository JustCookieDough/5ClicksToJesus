"""
builds a sample dataset consisting of all pages less than a given distance away from a target id (usually jesus).
"""


from io import FileIO

def build_sample(in_file: FileIO, out_file: FileIO, depth: int, target: int) -> None:
    print("starting build")
    i = 1
    search_ids = {target}
    out_dict = {}

    while i <= depth:  
        print(f"building depth {i}")
        # start at top of file and make a new set
        in_file.seek(0)
        found_ids = set()
        
        for line in in_file:
            verts = [int(s) for s in str(line, "utf-8").strip().split(' ')]
            if verts[1] in search_ids and verts[0] not in out_dict:  # if links to an id in search_ids and isnt in dict
                out_dict[verts[0]] = verts[1]
                found_ids.add(verts[0])         # saving this twice is stupid but also is the only way i can think of rn
        
        print(f"done! found {len(found_ids)} pages distance {i} away from target!\n")
        search_ids = found_ids
        i += 1

    print("done searching! writing file...")    
    for k in out_dict:
        out_file.write(f"{k} {out_dict[k]}\n")
    print("done! enjoy your sample!")