import sys
import time
import libtorrent as lt
from flask import Flask, request
import requests
import re
import json
from flask import Flask,redirect
import threading
videoFile = "c:/Users/龔鈺翔/Documents/BT stream/tmp/a"
workingPath = "c:/Users/龔鈺翔/Documents/BT stream/tmp"
fs = lt.file_storage()
lt.add_files(fs, videoFile)
t = lt.create_torrent(fs)
t.add_tracker("udp://tracker.publicbt.com:80")
t.add_tracker("udp://open.stealth.si:80")
t.add_tracker("udp://tracker.opentrackr.org:1337")
t.add_tracker("udp://tracker.leechers-paradise.org:6969")
t.add_tracker("udp://tracker.coppersurfer.tk:6969")
t.add_tracker("udp://140.115.152.14:2255")
t.add_tracker("http://54.39.98.124:80/announce")
t.add_tracker("udp://p4p.arenabg.com:1337/announce")

t.set_creator("My Torrent")
t.set_comment("Test")
lt.set_piece_hashes(t, workingPath)
torrent = t.generate()

f = open(workingPath+"/"+"mytorrent.torrent", "wb")
f.write(lt.bencode(torrent))
f.close()

#ps = lt.proxy_settings()
#ps.type = lt.proxy_type.http
#ps.hostname = "hostname.de"
#ps.port = 1003

ses = lt.session()
ses.listen_on(6881, 6891)
#ses.set_proxy(ps)
#ses.set_web_seed_proxy(ps)

handle = ses.add_torrent({'ti': lt.torrent_info(torrent), 'save_path': workingPath,})
def server():
    '''
   fs = lt.file_storage()
    lt.add_files(fs, videoFile)
    t = lt.create_torrent(fs)
    t.add_tracker("udp://tracker.publicbt.com:80")
    t.add_tracker("udp://open.stealth.si:80")
    t.add_tracker("udp://tracker.opentrackr.org:1337")
    t.add_tracker("udp://tracker.leechers-paradise.org:6969")
    t.add_tracker("udp://tracker.coppersurfer.tk:6969")
    t.add_tracker("udp://140.115.152.14:2255")
    t.add_tracker("http://54.39.98.124:80/announce")
    t.add_tracker("udp://p4p.arenabg.com:1337/announce")

    t.set_creator("My Torrent")
    t.set_comment("Test")
    lt.set_piece_hashes(t, workingPath)
    torrent = t.generate()

    f = open(workingPath+"/"+"mytorrent.torrent", "wb")
    f.write(lt.bencode(torrent))
    f.close()

#ps = lt.proxy_settings()
#ps.type = lt.proxy_type.http
#ps.hostname = "hostname.de"
#ps.port = 1003

    ses = lt.session()
    ses.listen_on(6881, 6891)
#ses.set_proxy(ps)
#ses.set_web_seed_proxy(ps)

    handle = ses.add_torrent({'ti': lt.torrent_info(torrent), 'save_path': workingPath,})
#handle.is_seed(1)
#h=lt.add_magnet_uri(ses,lt.make_magnet_uri(lt.torrent_info(torrent)),{'save_path':workingPath,'seed_mode':True})
    print(lt.make_magnet_uri(lt.torrent_info(torrent)))
    #z=input('press anything to go')
        
    print(handle.is_seed()) 
    '''
    while 1:
    #print('1')
        try:
            s = handle.status()
            state_str = ['queued', 'checking', 'downloading metadata', \
            'downloading', 'finished', 'seeding', 'allocating', 'checking fastresume']

            print('\r%.2f%% complete (down: %.1f kb/s up: %.1f kB/s peers: %d) %s' % \
            (s.progress * 100, s.download_rate / 1000, s.upload_rate / 1000, s.num_peers, state_str[s.state]))
            sys.stdout.flush()

            time.sleep(1)
        except KeyboardInterrupt:
            break

app = Flask(__name__)
@app.route('/', methods=['POST','GET'])
def result():
    print(request.values['type']) # should display 'bar'   
    if(request.values['type']=="music"):
        print("ok")
        #videoFile = "c:/Users/龔鈺翔/Documents/BT stream/tmp/a"
        #workingPath = "c:/Users/龔鈺翔/Documents/BT stream/tmp"
        #mainPath = "c:/Users/龔鈺翔/Documents/BT stream/tmp"

        fs = lt.file_storage()
        lt.add_files(fs, videoFile)
        t = lt.create_torrent(fs)
        t.add_tracker("udp://tracker.publicbt.com:80")
        t.add_tracker("udp://open.stealth.si:80")
        t.add_tracker("udp://tracker.opentrackr.org:1337")
        t.add_tracker("udp://tracker.leechers-paradise.org:6969")
        t.add_tracker("udp://tracker.coppersurfer.tk:6969")
        t.add_tracker("udp://140.115.152.14:2255")
        t.add_tracker("http://54.39.98.124:80/announce")
        t.add_tracker("udp://p4p.arenabg.com:1337/announce")

        t.set_creator("My Torrent")
        t.set_comment("Test")
        lt.set_piece_hashes(t, workingPath)
        torrent = t.generate()

        f = open(workingPath+"/"+"mytorrent.torrent", "wb")
        f.write(lt.bencode(torrent))
        f.close()

#ps = lt.proxy_settings()
#ps.type = lt.proxy_type.http
#ps.hostname = "hostname.de"
#ps.port = 1003

        ses = lt.session()
        ses.listen_on(6881, 6891)
#ses.set_proxy(ps)
#ses.set_web_seed_proxy(ps)

        handle = ses.add_torrent({'ti': lt.torrent_info(torrent), 'save_path': workingPath,})
#handle.is_seed(1)
#h=lt.add_magnet_uri(ses,lt.make_magnet_uri(lt.torrent_info(torrent)),{'save_path':workingPath,'seed_mode':True})
        print(lt.make_magnet_uri(lt.torrent_info(torrent)))
    #z=input('press anything to go')
        
        print(handle.is_seed()) 
        thread1=threading.Thread(target=server)
        thread1.setDaemon(True)
        thread1.start()
        return lt.make_magnet_uri(lt.torrent_info(torrent))

        
    else:
        print("request.values['type']")
        return"error"

app.run(port=80)



















#/作者介紹.mp4
videoFile = "c:/Users/龔鈺翔/Documents/BT stream/tmp/a"
workingPath = "c:/Users/龔鈺翔/Documents/BT stream/tmp"
mainPath = "c:/Users/龔鈺翔/Documents/BT stream/tmp"

fs = lt.file_storage()
lt.add_files(fs, videoFile)
t = lt.create_torrent(fs)
t.add_tracker("udp://tracker.publicbt.com:80")
t.add_tracker("udp://open.stealth.si:80")
t.add_tracker("udp://tracker.opentrackr.org:1337")
t.add_tracker("udp://tracker.leechers-paradise.org:6969")
t.add_tracker("udp://tracker.coppersurfer.tk:6969")
t.add_tracker("udp://140.115.152.14:2255")
t.add_tracker("http://54.39.98.124:80/announce")
t.add_tracker("udp://p4p.arenabg.com:1337/announce")

t.set_creator("My Torrent")
t.set_comment("Test")
lt.set_piece_hashes(t, workingPath)
torrent = t.generate()

f = open(workingPath+"/"+"mytorrent.torrent", "wb")
f.write(lt.bencode(torrent))
f.close()

#ps = lt.proxy_settings()
#ps.type = lt.proxy_type.http
#ps.hostname = "hostname.de"
#ps.port = 1003

ses = lt.session()
ses.listen_on(6881, 6891)
#ses.set_proxy(ps)
#ses.set_web_seed_proxy(ps)

handle = ses.add_torrent({'ti': lt.torrent_info(torrent), 'save_path': workingPath,})
#handle.is_seed(1)
#h=lt.add_magnet_uri(ses,lt.make_magnet_uri(lt.torrent_info(torrent)),{'save_path':workingPath,'seed_mode':True})
print(lt.make_magnet_uri(lt.torrent_info(torrent)))
z=input('press anything to go')

print(handle.is_seed())
while 1:
    #print('1')
    try:
        s = handle.status()
        state_str = ['queued', 'checking', 'downloading metadata', \
                'downloading', 'finished', 'seeding', 'allocating', 'checking fastresume']

        print('\r%.2f%% complete (down: %.1f kb/s up: %.1f kB/s peers: %d) %s' % \
        (s.progress * 100, s.download_rate / 1000, s.upload_rate / 1000, s.num_peers, state_str[s.state]))
        sys.stdout.flush()

        time.sleep(1)
    except KeyboardInterrupt:
        break






'''
import libtorrent as lt
import sys, time


videoFile = "C:\\Users\\龔鈺翔\\Documents\\BT stream\\tmp\\作者介紹.mp4"
workingPath = "C:\\Users\\龔鈺翔\\Documents\\BT stream\\tmp"

#Create torrent

f = lt.file_storage()
lt.add_files(f, videoFile)
t = lt.create_torrent(f)
t.add_node("router.utorrent.com", 6881)
t.add_node("dht.transmissionbt.com", 6881)
lt.set_piece_hashes(t, workingPath)
torrent = t.generate()
f = open("C:\\Users\\龔鈺翔\\Documents\\BT stream\\tmp\\1.torrent", "wb")
f.write(lt.bencode(torrent))
f.close()

#Seeding

PORT_RANGE = (6881,6891)
s = lt.session()
s.listen_on(PORT_RANGE[0],PORT_RANGE[1])
s.add_dht_router('router.utorrent.com',6881)
s.start_dht()
print ("DHT start: ", s.is_dht_running())
print ("DHT state: ", s.dht_state())


params = {
            'save_path': workingPath,
            'storage_mode': lt.storage_mode_t.storage_mode_sparse,
            'ti': lt.torrent_info(torrent),
            
            
            
        }
h = s.add_torrent(params)
#h.seed_mode(1)
print("Total size: " + str(h.status().total_wanted))
print("Name: " + h.name())
while True:
    s = h.status()
    msg = '\r%.2f%% complete (down: %.1f kb/s up: %.1f kB/s peers: %d) %s'
    print(msg % (s.progress * 100, s.download_rate / 1000, s.upload_rate / 1000, s.num_peers, s.state))
    sys.stdout.flush()
    time.sleep(1)


#'paused': False,
#'upload_mode':True,
#'super_seeding':True

'''