from celery import shared_task
from .models import Tournament


@shared_task
def generate_pairings_task(tournament_id):
    try:
        tournament = Tournament.objects.get(id=tournament_id)
        pairings = tournament.generate_pairings()
        for player1, player2 in pairings:
            tournament.matches.create(
                player1=player1, player2=player2, round=tournament.current_round
            )
        tournament.current_round += 1
        tournament.save()
    except Tournament.DoesNotExist:
        print(f"Tournament with id {tournament_id} not found")
