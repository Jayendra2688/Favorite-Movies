import requests

# api_key="d366a11d349469acb489a388416ed43d"
# api_access_token = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJkMzY2YTExZDM0OTQ2OWFjYjQ4OWEzODg0MTZlZDQzZCIsIm5iZiI6MTcyMzUyNjIwNi44MTE4NTIsInN1YiI6IjY2YjYwZDdmNDI1ZTE3YzUzZjAxNWQ4MCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.lGuUUOxCHrTJECWWcmwQCmpvA8PtuUd2ewJ71TZyJZM"
#
# url =  "https://api.themoviedb.org/3/search/movie"
#
# headers = {"accept": "application/json"}
#
#
# params = {
#     "query":"Inception",
#     "api_key":api_key,
# }
#
# response = requests.get(url,headers=headers,params=params)
#
# print(response.text)

omdb_url = "https://www.omdbapi.com/"

omdb_api_key ="ffa5a3d8"

movie = input("the movie name?")
params = {
    "apikey":omdb_api_key,
    "t":movie,
}

result = requests.get(omdb_url,params=params)

print(result.text)