from django.http import HttpResponse
import json, requests


def index(request):
    print("Olamundo")
    return HttpResponse("Hello, world. You're at the app index.")

def detail_one_player(request, player_id):
    response = requests.get("https://api.opendota.com/api/players/" + str(player_id) + "/matches")
    dados = json.loads(response.content)
    print(dados)
    return HttpResponse(dados)
    # return HttpResponse("You're looking at player %s." % player_id)


def detail_two_players(request, player1_id, player2_id):
    res1 = requests.get("https://api.opendota.com/api/players/" + str(player1_id) + "/matches")
    res2 = requests.get("https://api.opendota.com/api/players/" + str(player2_id) + "/matches")
    matches1 = json.loads(res1.content)
    matches2 = json.loads(res2.content)
    print(len(matches1))
    print(len(matches2))
    conj = dict() 
    for x in matches1:
        match_id = x['match_id']
        conj[match_id] = x
    
    tog1 = []
    tog2 = []

    for y in matches2:
        match_id = y['match_id']
        if match_id in conj:
            tog1.append(conj[match_id])
            tog2.append(y)

    return HttpResponse(tog1)
    # return HttpResponse("You're looking at players %s and %s." % (player1_id, player2_id) )