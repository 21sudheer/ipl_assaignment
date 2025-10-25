from django.db.models import Count, Sum, F
from django.http import JsonResponse
from django.shortcuts import render
from .models import Match, Delivery

# 1️⃣ Matches per year
def matches_per_year(request):
    data = Match.objects.values('season').annotate(matches=Count('id')).order_by('season')
    return JsonResponse(list(data), safe=False)

# 2️⃣ Matches won per team per year
def matches_won_per_team(request):
    data = (
        Match.objects.exclude(winner__isnull=True)
        .values('season', 'winner')
        .annotate(wins=Count('winner'))
        .order_by('season')
    )
    return JsonResponse(list(data), safe=False)


# 3️⃣ Extra runs conceded per team (year)
def extra_runs(request, year):
    matches = Match.objects.filter(season=year)
    data = (
        Delivery.objects.filter(match__in=matches)
        .values('bowling_team')
        .annotate(extra_runs=Sum('extra_runs'))
        .order_by('-extra_runs')
    )
    return JsonResponse(list(data), safe=False)

# 4️⃣ Top economical bowlers (year)
def economical_bowlers(request, year):
    matches = Match.objects.filter(season=year)
    data = (
        Delivery.objects.filter(match__in=matches)
        .values('bowler')
        .annotate(
            total_runs=Sum('total_runs'),
            balls=Count('ball')
        )
    )
    result = []
    for row in data:
        economy = (row['total_runs'] / row['balls']) * 6
        result.append({'bowler': row['bowler'], 'economy': round(economy, 2)})
    sorted_result = sorted(result, key=lambda x: x['economy'])[:10]
    return JsonResponse(sorted_result, safe=False)

# 5️⃣ Matches played vs won (year)
def matches_played_vs_won(request, year):
    matches = Match.objects.filter(season=year)
    played = (
        matches.values('team1')
        .annotate(total=Count('team1'))
        .union(matches.values('team2').annotate(total=Count('team2')))
    )
    won = matches.values('winner').annotate(total_won=Count('winner'))
    return JsonResponse({'played': list(played), 'won': list(won)}, safe=False)

# Landing Page
def dashboard(request):
    return render(request, 'dashboard.html')
