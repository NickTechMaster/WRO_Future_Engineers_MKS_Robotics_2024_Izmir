Motorisierung

Beim letztjährigen Future Engineers Wettbewerb haben wir auf Fischertechnik-Teile gesetzt. Dieses Jahr wollten wir das ändern. Stattdessen haben wir im Deutschlandfinale ein komplett selbstgebautes Auto verwendet, das wir größtenteils auch im Vorentscheid eingesetzt haben. Dafür haben wir als Grundlage ein Funduino-Kit genutzt, das speziell für Future Engineers entwickelt wurde. Von diesem Kit haben wir jedoch nur die Grundplatten, die Distanzhülsen und die Lenkung verwendet. In der Bauanleitung (e. Bauanleitung) findet man die genauen Maße und Abmessungen der Platten, Schrauben und aller weiteren Komponenten.

Lenkung

Für die Lenkung nutzen wir einen 20-kg-Servolenkungsmotor. Dieser Motor liegt quer auf unserer Grundplatte. Vom Gewinde des Servos führt eine kleine Stange, die mit Schrauben befestigt ist, zur eigentlichen Lenkachse. Diese Lenkachse verbindet die beiden Vorderräder miteinander. Wenn der Servo in eine Richtung lenkt, wird die Lenkachse als Ganzes verschoben und somit auch die Räder.

Antriebsmotor

Als Antriebsmotor verwenden wir einen herkömmlichen Motor, der über die Motorsteuerung "L298N" betrieben wird. An diese Motorsteuerung werden direkt 18 V vom Akku angeschlossen. Der Motor wird dann von dem Motortreiber mit Strom versorgt. Von der Motorsteuerung gehen noch drei Kabel ab, die wir zur Steuerung des Motors nutzen und die direkt in den "Fahr-Raspberry Pi" führen. Um beide Räder gleichzeitig antreiben zu können, verwenden wir eine Zahnradübersetzung, die die Motorumdrehungen auf ein Zahnrad überträgt, das fest an der Antriebsachse angebracht ist. Die Antriebsachse ist in der Mitte getrennt, jedoch sind die beiden Enden mit einer Verbindungshülse verbunden. Dadurch kann ein Rad frei drehen. Beim Vorentscheid hatten wir nämlich das Problem, dass unser Auto aufgrund von Kraftproblemen blockiert hat. Deshalb kann jetzt ein Rad frei drehen, wodurch dieser Fehler weniger häufig auftritt.
