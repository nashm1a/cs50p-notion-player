import re
import os
import sys

def main():
    print("--- Notion Music Player ---")
    title = input("Enter Playlist Title (e.g., I. NIGHT DRIVE): ")
    if not validate_title(title):
        sys.exit("Invalid title format.")

    bg_input = input("Enter GIF Background (URL or local path like assets/bg.gif): ")
    if not validate_image_source(bg_input):
        sys.exit("Invalid GIF file or URL.")

    tracks = []
    print("\nAdd Tracks (enter blank title when done):")
    while True:
        t_title = input(" Track Title: ")
        if not t_title.strip():
            break
        t_artist = input(" Track Artist: ")
        t_url = input(" Audio URL / Path (.mp3): ")
        tracks.append(format_track_data(t_title, t_artist, t_url))

    if not tracks:
        sys.exit("No tracks provided. Exiting.")

    html_code = build_html_file(title, bg_input, tracks)
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_code)
    print(f"\nSuccess! Built 'index.html' with {len(tracks)} track(s).")

def validate_title(title):
    """Validates that title is not empty and fits roman numeral/uppercase style."""
    pattern = r"^[A-Za-z0-9\.\s\-_]{1,50}$"
    return bool(re.match(pattern,title.strip()))

def validate_image_source(source):
    """Validates if 'source' parameter is a valid URL OR an existing local image/GIF file."""
    source = source.strip()
    
    # Check 1: Is 'source' a valid web URL?
    url_pattern = r"^https?://[^\s/$.?#].[^\s]*$"
    if re.match(url_pattern, source):
        return True
        
    # Check 2: Is 'source' an existing local file ending in .gif, .png, or .jpg?
    if os.path.exists(source) and source.lower().endswith(('.gif', '.png', '.jpg', '.jpeg')):
        return True
        
    return False

def format_track_data(title, artist, audio_url):
    """Formats raw track details into a new dictionary."""
    return {
        "title": title.strip().title(),
        "artist": artist.strip().title(),
        "audio_url": audio_url.strip()
    }

def build_html_file(title, bg_source, tracks):
    """Generates a standalone HTML string with embedded CSS/JS for Notion."""

    js_tracks = []
    for t in tracks:
        js_tracks.append(f'{{ title: "{t["title"]}", artist: "{t["artist"]}", src: "{t["audio_url"]}" }}')
    js_tracks_str = ",\n       ".join(js_tracks)

    html_content = f"""<!DOCTYPE html>
    <html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            background: url('{bg_source}') no-repeat center center fixed;
            background-size: cover;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            height: 100vh;
            display: flex;
            align-items: flex-end;
            justify-content: center;
            padding-bottom: 24px;
            overflow: hidden;
        }}
        .controls-bar {{
            background: rgba(18, 18, 18, 0.75);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.12);
            border-radius: 30px;
            padding: 12px 24px;
            display: flex;
            align-items: center;
            gap: 16px;
            color: #e0e0e0;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5);
        }}
        button {{
            background: none;
            border: none;
            color: #ffffff;
            cursor: pointer;
            font-size: 16px;
            transition: transform 0.1s ease;
        }}
        button:hover {{ transform: scale(1.15); }}
        .track-info {{
            display: flex;
            flex-direction: column;
            font-size: 0.85rem;
        }}
        .track-title {{ font-weight: 600; color: #fff; }}
        .track-artist {{ font-size: 0.75rem; color: #a0a0a0; }}
    </style>
</head>
<body>

    <div class="controls-bar">
        <button id="prev-btn">⏮</button>
        <button id="play-btn">▶</button>
        <button id="next-btn">⏭</button>
        <div class="track-info">
            <span id="track-title" class="track-title">Loading...</span>
            <span id="track-artist" class="track-artist"></span>
        </div>
    </div>

    <audio id="audio-player"></audio>

    <script>
        const playlist = [
            {js_tracks_str}
        ];
        let currentIndex = 0;
        const player = document.getElementById('audio-player');
        const playBtn = document.getElementById('play-btn');
        const prevBtn = document.getElementById('prev-btn');
        const nextBtn = document.getElementById('next-btn');
        const titleEl = document.getElementById('track-title');
        const artistEl = document.getElementById('track-artist');

        function loadTrack(index) {{
            const track = playlist[index];
            titleEl.textContent = track.title;
            artistEl.textContent = track.artist;
            player.src = track.src;
        }}

        playBtn.addEventListener('click', () => {{
            if (player.paused) {{
                player.play();
                playBtn.textContent = '⏸';
            }} else {{
                player.pause();
                playBtn.textContent = '▶';
            }}
        }});

        nextBtn.addEventListener('click', () => {{
            currentIndex = (currentIndex + 1) % playlist.length;
            loadTrack(currentIndex);
            player.play();
            playBtn.textContent = '⏸';
        }});

        prevBtn.addEventListener('click', () => {{
            currentIndex = (currentIndex - 1 + playlist.length) % playlist.length;
            loadTrack(currentIndex);
            player.play();
            playBtn.textContent = '⏸';
        }});

        // Initialize first track
        loadTrack(currentIndex);
    </script>
</body>
</html>"""
    return html_content

if __name__ == "__main__":
    main()