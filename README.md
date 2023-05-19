# RSWTA_house_budget

Tresc zadania:
Aplikacja pozwalajaca na zapamietywanie wydatków i przychodów oraz ich prezentacje w formie czytelnych zestawien i wykresow.
Podstawowe funkcje aplikacji: wprowadzanie wydatków/przychodów i przypisywanie ich do definiowanych przez uzytkownika kategorii, filtrowanie wpisów
i tworzenie z nich uzytecznych zestawien w formie tabeli i/lub wykresów 
Aplikacja powinna pozwalać na obsługę wielu portfeli, każdy z własnym zestawem kategorii i użytkownikami uprawnionymi do wykonywania wpisów.
projekt dla grupy maksymalnie 3-osobowej.

# How to run it?
-----------
1. clone repo `git clone git@github.com:mateuszhorczak/RSWTA_house_budget.git`
2. run `docker compose up`
3. build `docker-compose up --build`
4. check your container-id `docker ps`
5. run bash `docker exec -it [container-id] bash`
6. do migrate `python manage.py migrate`