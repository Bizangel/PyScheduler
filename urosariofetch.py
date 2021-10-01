import requests
'''
Objective is to use requests, and fetch from server:
- Name:
ex: Memes
- Credits:
ex: 3
- teacher:
  Top Memer

list of blockstrings
- Blockstring:
ex: Friday: 1:00PM-3:00PM
'''


def UrosarioFetch(classid, group, extras, display, window):
    token = {'authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOlsiYXBpUmVzdFJlc291cmNlSWQiXSwidXNlcl9uYW1lIjoiZkBnbWFpbC5jb20iLCJhdXRob3JpdGllcyI6WyJTVEFOREFSRF9VU0VSIl0sImp0aSI6ImVlMDc1NWMzLWRhYTUtNDQ2OS1iYTBkLWE5NDZlNzU1NzM5YyIsImNsaWVudF9pZCI6ImFwaVJlc3RDbGllbnRJZCIsInNjb3BlIjpbInJlYWQiLCJ3cml0ZSJdfQ.RqqlkOmETxx7XcUly7hmgDUXWVhDHCTt6VgtBPgqkZ8'}

    baseapi = 'https://guiaacademicabackend.azurewebsites.net/api/asignaturaDetalle?codigo={0}&opcionDetalle=DetalleAsignatura&tipoConsulta=usuario'.format(
        classid)

    activity_req = baseapi+'&opcionDetalle=DetalleActividad'
    base_req = baseapi+'&opcionDetalle=DetalleAsignatura'

    if display is not None:
        display.set('Fetching Class Activities...')
        window.update()

    activity_res = requests.get(activity_req, headers=token)

    if display is not None:
        display.set('Fetching Class Info...')
        window.update()

    base_res = requests.get(base_req, headers=token)
    activitylist = activity_res.json()['data']
    
    print(base_res.json())
    name = base_res.json()['data'][0]['nombre']
    cred = base_res.json()['data'][0]['creditos']

    main_activity = activitylist[0]['codActividad']

    activitycodes = []
    if len(activitylist) > 1:
        # fetch others
        for activity in activitylist:
            activitycodes.append(activity['codActividad'])

        extracodes = activitycodes[1:]  # remove main

    if display is not None:
        display.set('Fetching Groups...')
        window.update()

    group_req = baseapi + '&opcionDetalle=DetalleGrupo&codActividad={0}'.format(main_activity)
    group_res = requests.get(group_req, headers=token)

    groupcodes = []
    for groupdict in group_res.json()['data']:
        groupcodes.append(groupdict['codGrupo'])

    if display is not None:
        display.set('Fetching Groups Date...')
        window.update()

    fetchgroup = groupcodes[group-1]
    fechas_req = baseapi + \
        '&opcionDetalle=DetalleFecha&codActividad={0}&codGrupo={1}'.format(
            main_activity, fetchgroup)
    fechas_res = requests.get(fechas_req, headers=token)

    fechaini = fechas_res.json()['data'][0]['fechaInicio']
    fechafin = fechas_res.json()['data'][0]['fechaFin']

    horario_req = baseapi + '&opcionDetalle=DetalleHorario&codActividad={0}&codGrupo={1}&fechaIni={2}&fechaFin={3}'.format(
        main_activity, fetchgroup, fechaini, fechafin)
    horario_res = requests.get(horario_req, headers=token)

    if display is not None:
        display.set('Fetching Class Schedule...')
        window.update()

    teacher = horario_res.json()['data'][0]['profesor']

    blockdays = []
    blockstarts = []
    blockends = []
    for blockdict in horario_res.json()['data']:
        blockdays.append(blockdict['dia'])
        blockstarts.append(blockdict['horaInicio'])
        blockends.append(blockdict['horaFin'])

    blockstrings = []
    for i in range(len(blockdays)):
        blockstrings.append(blockdays[i] + ' ' + blockstarts[i] + '-' + blockends[i])

    ''' --- IF EXTRAS --- IF EXTRAS --- IF EXTRAS --- IF EXTRAS --- '''
    if extras:
        if display is not None:
            display.set('Fetching Extra Activities Info...')
            window.update()

        for main_activity in extracodes:
            group_req = baseapi + \
                '&opcionDetalle=DetalleGrupo&codActividad={0}'.format(main_activity)
            group_res = requests.get(group_req, headers=token)

            groupcodes = []
            for groupdict in group_res.json()['data']:
                groupcodes.append(groupdict['codGrupo'])

            fetchgroup = groupcodes[group-1]
            fechas_req = baseapi + \
                '&opcionDetalle=DetalleFecha&codActividad={0}&codGrupo={1}'.format(
                    main_activity, fetchgroup)
            fechas_res = requests.get(fechas_req, headers=token)

            fechaini = fechas_res.json()['data'][0]['fechaInicio']
            fechafin = fechas_res.json()['data'][0]['fechaFin']

            horario_req = baseapi + '&opcionDetalle=DetalleHorario&codActividad={0}&codGrupo={1}&fechaIni={2}&fechaFin={3}'.format(
                main_activity, fetchgroup, fechaini, fechafin)
            horario_res = requests.get(horario_req, headers=token)

            blockdays = []
            blockstarts = []
            blockends = []
            for blockdict in horario_res.json()['data']:
                blockdays.append(blockdict['dia'])
                blockstarts.append(blockdict['horaInicio'])
                blockends.append(blockdict['horaFin'])

            for i in range(len(blockdays)):
                blockstrings.append(blockdays[i] + ' ' + blockstarts[i] + '-' + blockends[i])

    if display is not None:
        display.set('Done!')
        window.update()

    return name, teacher, cred, blockstrings


# codigo = 11010040
# grupo = 1

# name, teacher, cred, blockstrings = UrosarioFetch(codigo, grupo, True, None, None)

# print('Name: ', name)
# print('Teacher: ', teacher)
# print('Credits:', cred)

# for block in blockstrings:
    # print(block)
