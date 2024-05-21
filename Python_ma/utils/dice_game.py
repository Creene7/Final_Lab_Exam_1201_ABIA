import os
from utils.user_manager import UserManager
from utils.score import Score
import random
from datetime import datetime
class DiceGame:
    def __init__(self):
        self.user_manager = UserManager()
        self.scores = []
        self.current_user = None
        self.load_scores()

    def load_scores(self):
        if not os.path.exists('data'):
            os.makedirs('data')
        if not os.path.exists('data/rankings.txt'):
            open('data/rankings.txt', 'w').close()
        else:
            with open('data/rankings.txt', 'r') as file:
                for line in file:
                    username, game_id, points, wins = line.strip().split(',')
                    self.scores.append(Score(username, game_id, int(points), int(wins)))

    def save_scores(self):
        self.scores.sort(key=lambda x: x.points, reverse=True)
        with open('data/rankings.txt', 'w') as file:
            for score in self.scores[:10]:
                file.write(f"{score.username},{score.game_id},{score.points},{score.wins}\n")

    def play_game(self):
        points = 0
        stages_won = 0
        game_id = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        while True:
            stage_points = 0
            user_wins = 0
            computer_wins = 0

            for _ in range(3):
                user_roll = random.randint(1, 6)
                computer_roll = random.randint(1, 6)
                if user_roll > computer_roll:
                    user_wins += 1
                elif computer_roll > user_roll:
                    computer_wins += 1

            if user_wins > computer_wins:
                stages_won += 1
                stage_points = 3 + user_wins
                points += stage_points
                print(f"You won the stage! Total points: {points}, Stages won: {stages_won}")
                choice = input("Do you want to continue to the next stage? (1 for Yes, 0 for No): ").strip()
                if choice == '0':
                    break
                elif choice != '1':
                    print("Invalid choice. Please try again.")
            else:
                print("Game over. You didn’t win any stages.")
                break
        
        if stages_won > 0:
            self.scores.append(Score(self.current_user.username, game_id, points, stages_won))
            self.save_scores()

    def show_top_scores(self):
        self.scores.sort(key=lambda x: x.points, reverse=True)
        if not self.scores:
            print("No scores to display yet.")
            return
        for score in self.scores[:10]:
            print(f"Username: {score.username}, Game ID: {score.game_id}, Points: {score.points}, Wins: {score.wins}")

    def logout(self):
        self.current_user = None

    def menu(self):
        while True:
            if self.current_user:
                print(f"Logged in as {self.current_user.username}")
                print("1. Play Game")
                print("2. View Top Scores")
                print("3. Logout")
                print("4. Exit")
                choice = input("Enter your choice: ").strip()
                if choice == '1':
                    self.play_game()
                elif choice == '2':
                    self.show_top_scores()
                elif choice == '3':
                    self.logout()
                elif choice == '4':
                    break
                else:
                    print("Invalid choice. Please try again.")
            elif not self.current_user:
                print("1. Register")
                print("2. Login")
                print("3. Exit")
                choice = input("Enter your choice: ").strip()
                if choice == '1':
                    self.user_manager.register()
                elif choice == '2':
                    self.current_user = self.user_manager.login()
                elif choice == '3':
                    break
                else:
                    print("Invalid choice. Please try again.")
            else:
                print('Error')

