#!/usr/bin/env python3
"""Snapshot Solana mint data and DEX markets, and page through mint-address signatures.
Python 3 standard library only. NOT a complete history of trades or holders.
"""
import argparse, datetime, json, os, pathlib, time, urllib.request, urllib.error

MINTS = {
 "get-money": "7Y8shnrkN9sKySNmUFCVG8FwQk9829ncozJ2AjaEnREV",
 "purple-squirrel": "6z9oBZ84zSx2uPvPofyaAABmBaWUk1BmDkMQryiYorzk",
}
RPC = "https://api.mainnet-beta.solana.com"

def fetch(url, data=None):
    body = None if data is None else json.dumps(data).encode()
    headers = {"User-Agent":"Lantern-Solana-Research/0.1","Accept":"application/json"}
    if body: headers["Content-Type"]="application/json"
    for attempt in range(4):
        try:
            with urllib.request.urlopen(urllib.request.Request(url,data=body,headers=headers), timeout=30) as response:
                return json.load(response)
        except (OSError, ValueError) as e:
            if attempt == 3: raise
            print("retry:",e)
            time.sleep(2 ** (attempt+1))

def rpc(url, method, params):
    result = fetch(url, {"jsonrpc":"2.0","id":1,"method":method,"params":params})
    if result.get("error"): raise RuntimeError(str(result["error"]))
    return result.get("result")

def save(path, obj):
    path.parent.mkdir(parents=True,exist_ok=True)
    tmp = path.with_suffix(path.suffix+".tmp")
    tmp.write_text(json.dumps(obj,indent=2)+"\n",encoding="utf-8")
    tmp.replace(path)

def run(name,mint,args):
    root=pathlib.Path(args.output)/name
    stamp=datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    snapshot={"timestamp_utc":stamp,"label":name,"mint":mint,"rpc":{},"dex":{},"errors":[]}
    for method,params in [
        ("getAccountInfo",[mint,{"encoding":"jsonParsed"}]),
        ("getTokenSupply",[mint]),
        ("getTokenLargestAccounts",[mint]),
    ]:
        try: snapshot["rpc"][method]=rpc(args.rpc,method,params)
        except Exception as e: snapshot["errors"].append(method+": "+str(e))
        time.sleep(args.delay)
    for label,path in [("pairs",f"/token-pairs/v1/solana/{mint}"),
                       ("orders",f"/orders/v1/solana/{mint}")]:
        try: snapshot["dex"][label]=fetch("https://api.dexscreener.com"+path)
        except Exception as e: snapshot["errors"].append(label+": "+str(e))
    save(root/"snapshots"/(stamp+".json"),snapshot)
    save(root/"latest.json",snapshot)
    print(name,"snapshot saved, errors:",snapshot["errors"])
    if not args.pages: return
    statepath=root/"mint_signature_cursor.json"
    if args.restart:
        statepath.unlink(missing_ok=True)
        (root/"mint_signatures.jsonl").unlink(missing_ok=True)
    state=json.loads(statepath.read_text()) if statepath.exists() else {"before":None,"complete":False,"count":0}
    for page in range(args.pages):
        if state["complete"]: break
        options={"limit":args.page_size,"commitment":"finalized"}
        if state["before"]: options["before"]=state["before"]
        try: rows=rpc(args.rpc,"getSignaturesForAddress",[mint,options])
        except Exception as e:
            print("Signature query stopped:",e)
            break
        if not rows:
            state["complete"]=True
            save(statepath,state)
            break
        # Cursor only advanced after append. This is resumable, but a crash between
        # writing data and cursor may cause duplicates; de-duplicate by signature.
        with (root/"mint_signatures.jsonl").open("a",encoding="utf-8") as f:
            for row in rows: f.write(json.dumps(row,separators=(",",":"))+"\n")
            f.flush()
            os.fsync(f.fileno())
        state["before"]=rows[-1]["signature"]
        state["count"]+=len(rows)
        state["complete"]=len(rows)<args.page_size
        save(statepath,state)
        print(" ",name,"mint signatures:",state["count"])
        time.sleep(args.delay)

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--output",default="solana-data")
    p.add_argument("--rpc",default=os.getenv("SOLANA_RPC_URL",RPC))
    p.add_argument("--token",action="append",choices=list(MINTS),help="default: both")
    p.add_argument("--pages",type=int,default=1,help="signature pages per run, 0 to skip")
    p.add_argument("--page-size",type=int,default=100,help="up to 1000")
    p.add_argument("--delay",type=float,default=1.0)
    p.add_argument("--restart",action="store_true",help="restart mint signature pagination")
    args=p.parse_args()
    if args.pages<0 or not 1<=args.page_size<=1000 or args.delay<0: p.error("invalid rate settings")
    for name in args.token or MINTS:
        run(name,MINTS[name],args)
if __name__=="__main__": main()
