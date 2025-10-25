from django.core.management.base import BaseCommand
import pandas as pd
from ipl_app.models import Match, Delivery

class Command(BaseCommand):
    help = "Load IPL dataset into the database"

    def handle(self, *args, **kwargs):
        matches = pd.read_csv('matches.csv')
        deliveries = pd.read_csv('deliveries.csv')

        for _, row in matches.iterrows():
            Match.objects.create(
                season=row['season'],
                city=row['city'],
                date=row['date'],
                team1=row['team1'],
                team2=row['team2'],
                toss_winner=row['toss_winner'],
                toss_decision=row['toss_decision'],
                result=row['result'],
                dl_applied=row['dl_applied'],
                winner=row['winner'],
                win_by_runs=row['win_by_runs'],
                win_by_wickets=row['win_by_wickets'],
                player_of_match=row['player_of_match'],
                venue=row['venue'],
                umpire1=row['umpire1'],
                umpire2=row['umpire2']
            )

        for _, row in deliveries.iterrows():
            Delivery.objects.create(
                match_id=row['match_id'],
                inning=row['inning'],
                batting_team=row['batting_team'],
                bowling_team=row['bowling_team'],
                over=row['over'],
                ball=row['ball'],
                batsman=row['batsman'],
                bowler=row['bowler'],
                wide_runs=row['wide_runs'],
                bye_runs=row['bye_runs'],
                legbye_runs=row['legbye_runs'],
                noball_runs=row['noball_runs'],
                penalty_runs=row['penalty_runs'],
                batsman_runs=row['batsman_runs'],
                extra_runs=row['extra_runs'],
                total_runs=row['total_runs'],
                player_dismissed=row['player_dismissed'],
                dismissal_kind=row['dismissal_kind'],
                fielder=row['fielder']
            )

        self.stdout.write(self.style.SUCCESS("Data loaded successfully!"))
