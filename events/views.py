from django.contrib import messages
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect

from actions.models import Action
from .models import Event, Account, Comment


# Create your views here.
def events_list(request):
    events = Event.objects.all().order_by('date').filter(is_deleted=False)
    return render(request,
                  "events/posts/list.html",
                  {"events": events}
                  )


def sort_list(request, option):
    events = Event.objects.all().order_by(option).filter(is_deleted=False)
    return render(request,
                  "events/posts/list.html",
                  {"events": events}
                  )


def event_detail(request, event_id):
    event = Event.objects.get(pk=event_id)
    all_comments = Comment.objects.all().order_by('-time')
    comments = []
    for comment in all_comments:
        if comment.event_id == event.id:
            comments.append(comment)
    return render(request,
                  'events/posts/item_detail.html',
                  {'event': event, 'comments': comments}
                  )


def home_page(request):
    event = Event.objects.get(pk=1)
    actions = Action.objects.all().order_by('-created')[:8]
    return render(request,
                  "events/homes/home_page.html",
                  {'event': event, 'actions': actions}
                  )


def search_result(request):
    return render(request,
                  "events/homes/search_result.html"
                  )


def feed_page(request):
    users = Account.objects.all()
    return render(request,
                  "events/posts/feeds-additional_page.html",
                  {"users": users}
                  )


def add_event(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        location = request.POST.get('location')
        date = request.POST.get('date')
        time = request.POST.get('time')
        description = request.POST.get('description')
        user = User.objects.get(username=request.session.get('username'))
        new_event = Event(
            title=title,
            location=location,
            date=date,
            time=time,
            description=description,
            organizer=request.session.get('username'),
            user=user

        )
        new_event.save()
        # log the action
        action = Action(
            user=user,
            verb="created the new event",
            target=new_event
        )
        action.save()
        messages.add_message(request, messages.SUCCESS, "You successfully added a new event: %s" % new_event.title)
        return redirect('events:event_detail', new_event.id)
    else:
        return render(request, 'events/posts/add_new_event.html')


def edit_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    if request.method == 'POST':
        title = request.POST.get('title')
        if event.title != title:
            title_change_action = Action(
                user=event.user,
                verb="edited the event title",
                target=event
            )
            title_change_action.save()

        description = request.POST.get('description')
        if event.description != description:
            description_change_action = Action(
                user=event.user,
                verb="edited the event description",
                target=event
            )
            description_change_action.save()

        event.location = request.POST.get('location')
        event.date = request.POST.get('date')
        event.time = request.POST.get('time')
        event.title = title
        event.description = description
        event.save()
        messages.add_message(request, messages.INFO, "You successfully edit the event: %s" % event.title)
        return redirect('events:event_detail', event_id)
    else:
        return render(request,
                      "events/posts/add_new_event.html", {'event': event})


def event_button_interaction(request):
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
    if is_ajax and request.method == "POST":
        event_id = request.POST.get('event_id')
        button_name = request.POST.get('button_name')
        try:
            event = Event.objects.get(pk=event_id)
            if button_name == 'shareButton':
                event.share_number = event.share_number + 1
            else:
                event.like_number = event.like_number + 1
            event.save()
            return JsonResponse(
                {'success': 'success', 'button_name': button_name, 'like_number': event.like_number,
                 'share_number': event.share_number},
                status=200)
        except Event.DoesNotExist:
            return JsonResponse({'error': 'No Event found with that id.'}, status=200)
    else:
        return JsonResponse({'error': 'Invalid Ajax Request'}, status=400)


def delete_event(request):
    if request.method == 'POST':
        event_id = request.POST.get('event_id')
        event = Event.objects.get(pk=event_id)
        event.is_deleted = True
        event.save()
        delete_event_action = Action(
            user=event.user,
            verb="delete the event",
            target=event
        )
        delete_event_action.save()
        messages.add_message(request, messages.WARNING, "You successfully delete the event: %s" % event.title)
        redirect('events:events_list')
    return redirect('events:events_list')


def user_info_interaction(request):
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
    if is_ajax and request.method == "POST":
        user_id = request.POST.get('user_id')
        print(user_id)
        try:
            user = Account.objects.get(pk=user_id)
            return JsonResponse(
                {'success': 'success', 'name': user.title, 'age': user.age,
                 'gender': user.gender, 'group': user.group, 'intro': user.intro},
                status=200)
        except Account.DoesNotExist:
            return JsonResponse({'error': 'No User profile found with that id.'}, status=200)
    else:
        return JsonResponse({'error': 'Invalid Ajax Request'}, status=400)


def event_register_interaction(request):
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
    if is_ajax and request.method == "POST":
        event_id = request.POST.get('event_id')
        button_text = request.POST.get('button_text')
        try:
            event = Event.objects.get(pk=event_id)
            if button_text == "Register":
                event.attendees += 1
                button_name = "Unregister"
            else:
                event.attendees -= 1
                button_name = "Register"
            event.save()
            return JsonResponse(
                {'success': 'success', 'attendees': event.attendees, 'button_name': button_name},
                status=200)
        except Event.DoesNotExist:
            return JsonResponse({'error': 'No Event found with that id.'}, status=200)
    else:
        return JsonResponse({'error': 'Invalid Ajax Request'}, status=400)
