
for parts in [line.strip().split(",")  for line in open("INDEX_20210917.txt","r").readlines()]:
    print(f"insert into pricedata (tickerid, dateid, openbid, openask, closedbid, closedask, volume) values('{parts[0]}',{parts[1]},{parts[2]},{parts[3]},{parts[4]},{parts[5]},{parts[6]})")

