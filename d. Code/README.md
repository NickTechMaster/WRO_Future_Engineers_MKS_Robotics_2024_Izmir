In diesem Ordner findet man die Programierung des Roboterautos


Wir haben zwei verschiedene Raspberrypis also haben wir insgesamt vier scripte zwei für das Eröffnungsrennen und zwei für das Hindernisrennen

f = fahrender Raspberrypi
k = Kamera Raspberrypi

Programmierung Eröffnungsrennen

Beim diesjährigen Eröffnungsrennen verwenden wir die Grundidee vom letzten Jahr. Während der Fahrt misst der Roboter kontinuierlich die Werte der Ultraschallsensoren, die vorne, links und rechts angeordnet sind. Basierend auf den Werten des linken und rechten Sensors berechnet der Roboter den Mittelpunkt und steuert das autonome Auto proportional, um es bestmöglich in die Mitte zurückzubringen. Das bedeutet, je weiter das Auto von der Mitte entfernt ist, desto stärker lenkt es, um diese Mitte wieder zu erreichen.

Ein Beispiel: Der linke Ultraschallsensor zeigt einen Wert von 10, der rechte Ultraschallsensor einen Wert von 50. Hier zeigt der linke Sensor eine sehr kurze Entfernung, was bedeutet, dass sich das Auto ziemlich weit links an der Bande befindet. Wenn wir nun die Summe der beiden Werte nehmen, erhalten wir die Zahl 60. Die Hälfte davon ist 30. Wenn beide Sensoren den Wert 30 ausgeben, wissen wir, dass der Roboter genau in der Mitte ist. Um diese Mitte zu erreichen, berechnen wir den Prozentsatz und lenken entsprechend.

Da dieser Prozess sehr schnell und häufig wiederholt wird, kann es manchmal zu einem leichten Schwanken kommen, das aber vom Auto ausgeglichen wird. Um am Ende der 3 Runden perfekt anzuhalten, erhöht das Auto eine Variable, wenn es eine Kurve fährt. Wir erkennen eine Kurve, wenn der Farbsensor orange oder blau erkennt. Der obere Raspberrypi der diese Daten empfängt sendet diese dann an den fahrenden Raspberry pi dieser zählt dann 12 Kurven und danch fährt er noch bis der vordere Ultrschall einen gewissen Abstand hat, und dann bleibt er stehen.

Programmierung Hindernisrennen

Beim Hindernisrennen nutzen wir die Programmierung vom Eröffnungsrennen als Grundlage, da wir auch hier autonom fahren müssen. Nur wenn die Kamera einen bunten Stein erkennt, sendet der obere Raspberrypi ein Signal an den fahrenden Raspberrypi dieser führt dann ein demenstsprechendes Ausweichmannöver aus. Bei roten Steinen fahren wir rechts herum, bei grünen Steinen links herum. Desweiteren erkennen wir über den Farbsensor Kurven, dort führen wir dann nämlich ein Ausrichtungsmannöver aus. Für die Farberkennung der Klötze verwenden wir Filter/Masken, um nur die Farben zu sehen und andere Fehler, die die Kamera erkennen könnte, auszublenden. Dort erkennen wir dann Kontouren. Zum Einstellen der Farbwerte der Masken haben wir uns ein extra script mit Schiebereglern geschrieben.
