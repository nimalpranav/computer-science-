from django.shortcuts import render

def classroom(request, room_name):
    return render(request, "classroom/room.html", {"room_name": room_name})
