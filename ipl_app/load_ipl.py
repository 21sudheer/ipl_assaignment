
import pandas as pd
from django.core.management.base import BaseCommand
from ipl_app.models import Match, Delivery
from django.db import transaction

class Command(BaseCommand):
    help = "Load IPL matches and deliveries CSV data"

    def add_arguments(self, parser):
        parser.add_argument('--matches', default='matches.csv')
        parser.add_argument('--deliveries', default='deliveries.csv')

    def handle(self, *args, **options):
        matches_df = pd.read_csv(options['matches'])
        deliveries_df = pd.read_csv(options['deliveries'])

        with transaction.atomic():
            Match.objects.all().delete()
            Delivery.objects.all().delete()

            matches_objs = [
                Match(
                    id=int(r['id']),
                    season=int(r['season']),
                    city=r.get('city') if pd.notna(r.get('city')) else None,
                    date=r.get('date'),
                    team1=r.get('team1'),
                    team2=r.get('team2'),
                    toss_winner=r.get('toss_winner'),
                    toss_decision=r.get('toss_decision'),
                    result=r.get('result'),
                    winner=r.get('winner') if pd.notna(r.get('winner')) else None,
                    win_by_runs=int(r.get('win_by_runs') or 0),
                    win_by_wickets=int(r.get('win_by_wickets') or 0),
                    player_of_match=r.get('player_of_match') if pd.notna(r.get('player_of_match')) else None,
                    venue=r.get('venue')
                )
                for _, r in matches_df.iterrows()
            ]
            Match.objects.bulk_create(matches_objs, batch_size=500)

            deliveries_objs = [
                Delivery(
                    match_id=int(r['match_id']),
                    inning=int(r['inning']),
                    batting_team=r.get('batting_team'),
                    bowling_team=r.get('bowling_team'),
                    over=int(r['over']),
                    ball=int(r['ball']),
                    batsman=r.get('batsman'),
                    non_striker=r.get('non_striker'),
                    bowler=r.get('bowler'),
                    is_super_over=bool(r.get('is_super_over')),
                    wide_runs=int(r.get('wide_runs') or 0),
                    bye_runs=int(r.get('bye_runs') or 0),
                    legbye_runs=int(r.get('legbye_runs') or 0),
                    noball_runs=int(r.get('noball_runs') or 0),
                    batsman_runs=int(r.get('batsman_runs') or 0),
                    extra_runs=int(r.get('extra_runs') or 0),
                    total_runs=int(r.get('total_runs') or 0),
                    player_dismissed=r.get('player_dismissed') if pd.notna(r.get('player_dismissed')) else None,
                    dismissal_kind=r.get('dismissal_kind') if pd.notna(r.get('dismissal_kind')) else None,
                    fielder=r.get('fielder') if pd.notna(r.get('fielder')) else None
                )
                for _, r in deliveries_df.iterrows()
            ]
            Delivery.objects.bulk_create(deliveries_objs, batch_size=1000)

        self.stdout.write(self.style.SUCCESS("Data loaded successfully"))
