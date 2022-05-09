from django.views import View
from django.http.response import HttpResponse
from django.shortcuts import render
from collections import deque

ticket_nr = 0


class WelcomeView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('<h2>Welcome to the Hypercar Service!</h2>')


class MenuView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'tickets/menu.html')


class TicketView(View):
    # queues for different services
    change_oil = deque()
    inflate_tires = deque()
    diagnostic = deque()
    full_queue = {'change_oil': change_oil,
                  'inflate_tires': inflate_tires,
                  'diagnostic': diagnostic}

    def get(self, request, ticket_type):
        # global full_queue
        global ticket_nr

        ticket_nr += 1
        wait_change_oil = 2 * len(self.full_queue['change_oil'])
        wait_inflate_tires = 5 * len(self.full_queue['inflate_tires'])
        wait_diagnostics = 30 * len(self.full_queue['diagnostic'])
        wait_time = 0
        if ticket_type == 'change_oil':
            wait_time = wait_change_oil
        elif ticket_type == 'inflate_tires':
            wait_time = wait_inflate_tires + wait_change_oil
        elif ticket_type == 'diagnostic':
            wait_time = wait_diagnostics + wait_inflate_tires + wait_change_oil
        self.full_queue[ticket_type].append(ticket_nr)
        return render(request, 'tickets/ticket.html',
                      {'ticket_nr': ticket_nr,
                       'wait_time': wait_time})
