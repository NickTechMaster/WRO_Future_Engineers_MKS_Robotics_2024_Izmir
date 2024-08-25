Energie

Unser Auto wird mit einem handelsüblichen 18V-Bosch-Akku betrieben. Dieser Akku wird in einen Akku-Slot eingeschoben. Von dort aus führt eine Verbindung zum Spannungswandler. Der Wandler wandelt die Spannung auf 5V um, die wir für die Raspberry Pis benötigen. Zusätzlich verwenden wir eine Motorsteuerung, die direkt mit 18V versorgt wird. Es ist erwähnenswert, dass die Ultraschallsensoren mit 5V betrieben werden, während andere Sensoren wie zum Beispiel der Farbsensor mit 3,3V arbeiten.

Sensoren

In unserem Auto sind eine Vielzahl von Sensoren verbaut. Zum einen haben wir vier HCSR-04-Ultraschallsensoren integriert, die zur Erkennung der Fahrbahn und zur Berechnung der Lenkung verwendet werden. Des Weiteren haben wir einen Farbsensor installiert, der orangene und blaue Linien erkennt und somit die Runden zählt, damit wir nach drei Runden erfolgreich stoppen können. Zudem löst er beim Hindernisrennen ein Manöver in jeder Kurve aus, damit wir uns in der Kurve ausrichten können. Ganz oben befindet sich außerdem eine Kamera. Es handelt sich um eine USB-Webcam von Logitech (Brio 500), die für die Hinderniserkennung verwendet wird.
