import requests
token='EAALa1uQGPg8BAIwAyFNAWSMzslR8Vu2qnkHmZBNOkYojzAsfb9ZBlmclE8SHvRCD5dSeijBGYZCxpfhuglLaZCbusczNiZAS9QMoh7MbeJRveYDrZBZATTuTh6tCL3xjLZA1Us7LhR5jZCKF0vwIStJr3ZAfFnm6rd0lXZBYL8Mk38q5ahFaar2aZC0M'
res = requests.get("https://graph.facebook.com/3714938138601087?fields=first_name,last_name,profile_pic&access_token={}".format(token))
print(res.json())