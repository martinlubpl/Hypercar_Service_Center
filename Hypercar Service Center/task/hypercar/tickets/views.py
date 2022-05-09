from django.views import View
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from collections import deque

ticket_nr = 0
processed_ticket = 0
# queues for different services
change_oil = deque()
inflate_tires = deque()
diagnostic = deque()
full_queue = {'change_oil': change_oil,
              'inflate_tires': inflate_tires,
              'diagnostic': diagnostic}


class WelcomeView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('<h2>Welcome to the Hypercar Service!</h2>')


class MenuView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'tickets/menu.html')


class TicketView(View):

    def get(self, request, ticket_type):
        # global full_queue
        global ticket_nr

        ticket_nr += 1
        wait_change_oil = 2 * len(full_queue['change_oil'])
        wait_inflate_tires = 5 * len(full_queue['inflate_tires'])
        wait_diagnostics = 30 * len(full_queue['diagnostic'])
        wait_time = 0
        if ticket_type == 'change_oil':
            wait_time = wait_change_oil
        elif ticket_type == 'inflate_tires':
            wait_time = wait_inflate_tires + wait_change_oil
        elif ticket_type == 'diagnostic':
            wait_time = wait_diagnostics + wait_inflate_tires + wait_change_oil
        full_queue[ticket_type].appendleft(ticket_nr)
        # print(full_queue)
        return render(request, 'tickets/ticket.html',
                      {'ticket_nr': ticket_nr,
                       'wait_time': wait_time})


class ProcessView(View):
    def get(self, request, *args, **kwargs):
        oil_len = len(full_queue['change_oil'])
        tires_len = len(full_queue['inflate_tires'])
        diag_len = len(full_queue['diagnostic'])
        return render(request, 'tickets/process.html',
                      context={'oil_len': oil_len,
                               'tires_len': tires_len,
                               'diag_len': diag_len
                               })

    def post(self, request, *args, **kwargs):
        global processed_ticket
        if len(full_queue['change_oil']) > 0:
            processed_ticket = full_queue['change_oil'].pop()
        elif len(full_queue['inflate_tires']) > 0:
            processed_ticket = full_queue['inflate_tires'].pop()
        elif len(full_queue['diagnostic']) > 0:
            processed_ticket = full_queue['diagnostic'].pop()
        else:
            processed_ticket = 0
        return redirect('/next')


class NextView(View):
    def get(self, request, *args, **kwargs):
        global processed_ticket
        return render(request, 'tickets/next.html',
                      context={'processed_ticket': processed_ticket})
