from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q, Count
from django.utils import timezone
from .models import Event, Participant, Category
from .forms import EventModelForm, ParticipantModelForm, CategoryModelForm

# CRUD Operations
def create_events(request):
    event_form = EventModelForm()
    participant_form = ParticipantModelForm()

    if request.method == "POST":
        event_form = EventModelForm(request.POST)
        participant_form = ParticipantModelForm(request.POST)
        if event_form.is_valid() and participant_form.is_valid():
            event = event_form.save(commit=False)
            event.save()
            participant = participant_form.save()
            event.participants.add(participant)
            participant.save()
            # messages.success(request, "Event and participant added successfully!")
            return redirect('event-home')

    context = {
        "event_form": event_form,
        "participant_form": participant_form,
    }
    return render(request, 'event-form.html', context)
def update_events(request, id):
    event = Event.objects.get(id= id)
    event_form = EventModelForm(instance = event)

    first_participant = event.participants.first()
    participant_form = ParticipantModelForm(instance = first_participant)

    if request.method == "POST":
        event_form = EventModelForm(request.POST, instance = event)
        if first_participant:
            participant_form = ParticipantModelForm(request.POST, instance = first_participant)
        else:
            participant_form = ParticipantModelForm(request.POST)
        if event_form.is_valid() and participant_form.is_valid():
            event = event_form.save(commit=False)
            event.save()
            participant = participant_form.save()
            event.participants.add(participant)
            participant.save()
            # messages.success(request, "Event and participant updated successfully!")
            return redirect('create-event')

    context = {
        "event_form": event_form,
        "participant_form": participant_form,
    }
    return render(request, 'event-form.html', context)

def delete_event(request, id):
    if request.method =="POST":
        event = Event.objects.get(id = id)
        event.delete()
        # messages.success(request, "Event Deleted Successfully")
        return redirect('event-dashboard')



def event_dashboard(request):
    today = timezone.now().date()
    events = Event.objects.select_related('category').prefetch_related('participants')

    search_query = request.GET.get('q')
    category_filter = request.GET.get('category')
    date_start = request.GET.get('date_start')
    date_end = request.GET.get('date_end')

    if search_query:
        events = events.filter(Q(name__icontains=search_query) | Q(location__icontains=search_query))
    
    if category_filter:
        events = events.filter(category__id=category_filter)
    
    if date_start and date_end:
        events = events.filter(date__range=[date_start, date_end])
    total_participant = Participant.objects.filter(events__isnull=False).distinct().count()
    upcoming_events_count = events.filter(date__gt=today).count()
    past_events_count = events.filter(date__lt=today).count()
    
    context = {
        'total_event': events.count(),
        'total_participant': total_participant,
        'upcoming_events_count': upcoming_events_count,
        'past_events_count': past_events_count,
        'today_events': events.filter(date=today),
        'all_events': events.order_by('-date'),
        'categories': Category.objects.all(),
        'today': today
    }
    return render(request, 'events/dashboard.html', context)

def event_home(request):
    today = timezone.now().date()
    events = Event.objects.select_related('category').prefetch_related('participants')
    upcoming_events = Event.objects.filter(date__gte=today).order_by('date')[:10]
    return render(request, 'events/event-home.html', {'events': events, 'upcoming_events': upcoming_events})

def event_detail(request, pk):
    event = get_object_or_404(Event.objects.prefetch_related('participants'), pk=pk)
    return render(request, 'events/event-detail.html', {'event': event})

def search_events(request):
    search_query = request.GET.get('q', '')
    events = Event.objects.filter(Q(name__icontains=search_query) | Q(location__icontains=search_query))
    return render(request, 'events/search-results.html', {'events': events})