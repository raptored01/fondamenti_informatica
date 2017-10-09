import random

descrizione = """
Gioco dei fiammiferi:
Ci sono un certo numero di fiammiferi sul tavolo che sceglierai
all'inizio del gioco.
Giocherai contro una stupida AI.
Queste sono le regole:
- si gioca a turni
- si può prendere un numero di fiammiferi da 1 a 3
- perde chi raccoglie l'ultimo fiammifero
"""

world_matches = 0


class Player:

    def __init__(self, name):
        self.name = name

    def play(self):

        global world_matches

        pick = 0
        while pick not in [1, 2, 3]:

            try:
                pick = int(input("Quanti fiammiferi vuoi prendere? (1-3): "))
            except ValueError:
                print("Inserisci un NUMERO da 1 a 3!")
                continue

            if pick not in [1, 2, 3]:
                print("Scegli un numero da 1 a 3!")
            elif pick > world_matches:
                print("Non puoi prendere più fiammiferi di quanti rimasti!")
            elif pick == world_matches:
                print("Ma che fai!?")
            else:
                print(f"{self.name} prende {pick} fiammiferi")
                world_matches -= pick
                if world_matches == 1:
                    return self.name
                else:
                    return False


class PlayerCPU(Player):

    def play(self):

        global world_matches
        # strategia: bisogna mandare l'avversario con un numero di fiammiferi n
        # tale per cui n - 1 % 4 = 0

        """
        Spiegazione:
        Ragionando alla rovescia, si ricava che il giocatore che rimane
        con fiammiferi <= 4 vince sempre. Ciò vuol dire che il giocatore
        che avrà 5 fiammiferi perderà di sicuro, perché non potrà non mettere
        l'altro giocatore in condizione di avere <= 4 fiammiferi.
        Quindi, il giocatore che si troverà con 6, 7 o 8 fiammiferi non dovrà
        far altro che prenderne n tale che f - n = 5.
        Così, anche il giocatore con 9 fiammiferi è destinato a perdere perché
        non potrà non mettere l'altro giocatore in condizione di avere 6, 7 o 8
        fiammiferi.
        Si può continuare a ritroso e ci si renderà presto conto che i numeri
        'perdenti' sono quelli tali per cui n - 1 % 4 = 0, quindi la nostra 'AI'
        dovrà scegliere la propria mossa in modo da lasciare all'altro giocatore
        un numero perdente di fiammiferi.
        E se l'altro giocatore è bravo e ci frega, scegliamo a caso e speriamo che sbagli!
        """

        while True:

            if (world_matches-1) % 4 == 0:
                # siamo fregati, a meno che l'avversario non conosca la logica
                pick = random.choice([1, 2, 3])

            elif world_matches <= 4: # non sarà mai 1 perché quando è 1 termina il gioco
                # se il numero dei fiammiferi è minore o uguale a 4 allora basta
                # prendere un numero di fiammiferi n tale che world_matches - n = 1
                pick = world_matches - 1
            else:
                # lo so, è brutto e ottimizzabile, ma sono le 10.30 di sera
                for n in [1, 2, 3]:
                    if (world_matches - n - 1) % 4 == 0:
                        pick = n
                        break

            # controllo per il primo if, perché sono troppo pigro per semplificarlo
            # o scriverlo meglio
            if pick < world_matches:
                print(f"{self.name} prende {pick} fiammiferi")
                world_matches -= pick
                if world_matches == 1:
                    return self.name
                else:
                    return False


class Master:
    players = []

    def game_loop(self):
        vincitore = False
        while not vincitore:
            for p in self.players:
                print(f"\nCi sono ancora {world_matches} fiammiferi\n")
                vincitore = p.play()
                if vincitore:
                    break
        print(f"\nÈ rimasto uno solo fiammifero, Vince {vincitore}!")


if __name__ == "__main__":

    play_again = True

    print(descrizione)

    human_player = Player(input("Come ti chiami?  "))

    while play_again:
        cpu_player = PlayerCPU("Stupid AI")
        world_matches = int(input("Con quanti fiammiferi vuoi giocare?  "))
        master = Master()
        if random.choice([0, 1]):    # scegliamo a caso chi inizia a giocare
            master.players = [human_player, cpu_player]
        else:
            master.players = [cpu_player, human_player]

        print(f"\nInizia a giocare {master.players[0].name}")

        master.game_loop()

        play_again = input("\nVuoi fare un'altra partita? ")
        if play_again.lower() in ["s", "sì", "si", "yes", "y", "yeah", "yup", "ok"]:
            play_again = True
        elif play_again.lower() in ["no", "nay", "n", "nope"]:
            play_again = False
        else:
            play_again = False
            print("Lo prendo per un no!")
    print("Ciao!")
