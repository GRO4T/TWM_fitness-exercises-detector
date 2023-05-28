model0.tf - model wytrenowany jedynie na zbiorach curl i armraise
zbiór danych:
193 klipy * liczba klatek per klip -> train, test split
skuteczność train: 98
skuteczność test: 99
wniosek: Wysoka skuteczność wynika zapewne z tego, że dane nie były podzielone
na poziomie poszczególnych klipów, a na poziomie klatek. Sprawia to, że dane testowe
znalazły się niejako w zbiorze treningowym. Mimo tego model w warunkach rzeczywistych
dziła całkiem dobrze. Ma problem przede wszystkim w pozycji, w której jesteśmy wyprostowani.
Najpewniej przydałyby się jakieś przykłady tła, czyli nagrania ludzi niewykonujących żadnych ćwiczeń.

model1.tf - podział danych na poziomie klipów
skuteczność train: 98
skuteczność test: 95

