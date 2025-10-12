import subprocess

def watch_anime(animetitle):
    """Opens a web browser to search for an anime with Vietnamese subtitles."""
    #print("enjoy your anime!")
    #time.sleep(1)
    subprocess.run([f'ani-cli {animetitle} '], shell=True)