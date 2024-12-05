import subprocess
import time
from multiprocessing import Process

# URL des flux M3U8
flux_a_restream1 = "https://audio.myradio.fr/stream1.m3u8"
flux_a_restream2 = "https://audio.myradio.fr/stream2.m3u8"

# Informations serveur Icecast
ICECAST_HOST = 'your_server_ip' #ex: 192.208.25.1
ICECAST_PORT = your_port #ex: 2211
ICECAST_USER = 'source' #par defaut
ICECAST_PASSWORD = 'yourpassword'
icecast1 = '/mountpoint1' #ex: /redzing-radio-nice
icecast2 = '/mountpoint1' #ex: /redzing-radio-frejus

def stream_ice1():
    ffmpeg_command = [
        'ffmpeg',
        '-re',
        '-i', flux_a_restream1,
        '-acodec', 'libmp3lame',
        '-ab', '112k',  # Débit audio
        '-f', 'mp3',
        '-max_delay', '0',
        '-flush_packets', '1',
        '-avoid_negative_ts', 'make_zero',
        '-probesize', '32',
        '-analyzeduration', '0',
        '-v', 'error',
        f'icecast://{ICECAST_USER}:{ICECAST_PASSWORD}@{ICECAST_HOST}:{ICECAST_PORT}{icecast1}'
    ]
    
    try:
        process = subprocess.Popen(ffmpeg_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        if process.returncode != 0:
            print(f"Erreur dans le processus FFmpeg : {stderr.decode()}")
            if "No data found" in stderr.decode() or "Error" in stderr.decode():
                print("Flux échoué, pas de son pour ce flux.")
        else:
            print(f"Stream en cours...")
    except Exception as e:
        print(f"Erreur d'exécution : {e}")

def stream_ice2():
    ffmpeg_command = [
        'ffmpeg',
        '-re',
        '-i', flux_a_restream2,
        '-acodec', 'libmp3lame',
        '-ab', '112k',  # Débit audio
        '-f', 'mp3',
        '-max_delay', '0',
        '-flush_packets', '1',
        '-avoid_negative_ts', 'make_zero',
        '-probesize', '32',
        '-analyzeduration', '0',
        '-v', 'error',
        f'icecast://{ICECAST_USER}:{ICECAST_PASSWORD}@{ICECAST_HOST}:{ICECAST_PORT}{icecast2}'
    ]
    
    try:
        process = subprocess.Popen(ffmpeg_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        if process.returncode != 0:
            print(f"Erreur dans le processus FFmpeg : {stderr.decode()}")
            if "No data found" in stderr.decode() or "Error" in stderr.decode():
                print("Flux échoué, pas de son pour ce flux.")
        else:
            print(f"Stream en cours...")
    except Exception as e:
        print(f"Erreur d'exécution : {e}")



def start_all_streams():
    processes = []
    
    for func in [stream_ice1, stream_ice2]:
        p = Process(target=func)
        p.start()
        processes.append(p)
    
    for p in processes:
        p.join()

if __name__ == "__main__":
    start_all_streams()
