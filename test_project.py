from project import validate_title, validate_image_source, format_track_data

def test_validate_title():
    assert validate_title("I. NIGHT DRIVE") == True
    assert validate_title("DARK_AESTHETIC_01") == True
    assert validate_title("") == False

def test_validate_image_source():
    assert validate_image_source("https://example.com/background.gif") == True
    assert validate_image_source("not_a_url_or_file") == False

def test_format_track_data():
    result = format_track_data("  night drive  ","  artist name  ","  https://audio.mp3  ")
    assert result["title"] == "Night Drive"
    assert result["artist"] == "Artist Name"
    assert result["audio_url"] == "https://audio.mp3"