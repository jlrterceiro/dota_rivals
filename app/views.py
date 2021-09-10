from django.http import HttpResponse
import json, requests

from django.template import loader
from django.shortcuts import render


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
    player1 = json.loads(requests.get("https://api.opendota.com/api/players/" + str(player1_id)).content)
    player2 = json.loads(requests.get("https://api.opendota.com/api/players/" + str(player2_id)).content)
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

    partidasSeparados = []


    for y in matches2:
        match_id = y['match_id']
        if match_id in conj:
            tog1.append(conj[match_id])
            tog2.append(y)

    qtJuntos = 0
    qtSeparados = 0

    vitoriaJuntos = 0
    vitoriaSeparados = 0

    for i in range(len(tog1)): 
        m1 = tog1[i]
        m2 = tog2[i]
        lado1 = 'radiant' if m1['player_slot'] <= 127 else 'dire'
        lado2 = 'radiant' if m2['player_slot'] <= 127 else 'dire'
        timeVencedor = 'radiant' if m1['radiant_win'] == True else 'dire'
        if lado1 == lado2:
            qtJuntos = qtJuntos + 1
            if lado1 == timeVencedor :
                vitoriaJuntos = vitoriaJuntos + 1
        else:
            qtSeparados = qtSeparados + 1
            if lado1 == timeVencedor :
                vitoriaSeparados = vitoriaSeparados + 1
            partidasSeparados.append(m1)

    print(qtJuntos)
    print(qtSeparados)
    print(vitoriaJuntos)
    print(vitoriaSeparados)

    context = {
        'player1': player1,
        'player2': player2,
        'total_juntos': qtJuntos,
        'total_separados': qtSeparados,
        'vitorias_juntos': vitoriaJuntos,
        'vitorias_separados': vitoriaSeparados,
        'derrotas_juntos': qtJuntos-vitoriaJuntos,
        'derrotas_separados': qtSeparados-vitoriaSeparados,
        'lista_partidas_separados': partidasSeparados,
        'lista_partidas': tog1,
    }

    template = loader.get_template('app/index.html')
    

    return render(request, 'app/index.html', context)
    # return HttpResponse("You're looking at players %s and %s." % (player1_id, player2_id) )