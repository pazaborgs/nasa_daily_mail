from main import get_nasa_data, get_art_data

# Testando as funções

# --- NASA ---

print("Testando a API da NASA com dados de exemplo... \n")

fake_data = {
    "copyright": "Vimeo User",
    "date": "2023-10-10",
    "explanation": "This is a video of a black hole.",
    "media_type": "video",
    "service_version": "v1",
    "thumbnail_url": "https://img.youtube.com/vi/dQw4w9WgXcQ/maxresdefault.jpg",
    "title": "Black Hole Animation",
    "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
}
nasa_result = get_nasa_data(mock_data=fake_data)
print(nasa_result)

# --- Art Institute of Chicago ---

print("\n Testando o Art Institue of Chicago... \n")
art_result = get_art_data()
print(art_result)